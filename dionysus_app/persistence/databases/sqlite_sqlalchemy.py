"""SQLAlchemy SQLite3 Database object ."""
from contextlib import contextmanager
from io import BytesIO
from pathlib import Path
from typing import (Any,
                    Iterator,
                    Optional,
                    )

from matplotlib import pyplot as plt
from sqlalchemy import (BLOB,
                        Column,
                        create_engine,
                        ForeignKey,
                        Integer,
                        REAL,
                        String,
                        )
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (sessionmaker,
                            Session,
                            )

from dionysus_app.class_ import Class, NewClass
from dionysus_app.data_folder import DataFolder
from dionysus_app.student import Student
from dionysus_app.persistence.database import ClassIdentifier, Database

from sqlalchemy.orm.decl_api import DeclarativeMeta

Base: DeclarativeMeta = declarative_base()


class SQLiteSQLAlchemyDatabase(Database):
    """
        SQLiteSQLAlchemyDatabase object.

        Database implemented using SQLAlchemy wrapping python SQLite3 module.

        Schema:
            Table: `class`
                key `id` - INTEGER primary key
                key `name` TEXT <= 255 chars

            Table: `student`
                key `id` - INTEGER primary key
                key `name` - TEXT <= 255 chars
                key `class_id` - INTEGER student's class `class.id`
                key `avatar_id` - INTEGER student's avatar image `avatar.id`

            Table: `chart`
                key `id` - INTEGER primary key
                key `name` - TEXT <= 255 chars
                key `date` - chart created date TODO: implement/document

            Table: `score` - scores in charts
                key `id` - INTEGER primary key
                key `chart_id` - INTEGER `chart.id` score belongs to
                key `student_id` - INTEGER `student.id` score belongs to
                key `value` - REAL (ie float) the score

            Table: `avatar`
                key `id` - INTEGER primary key
                key `image` blob
        """

    def __init__(self, default_avatar_path: Path|None = None,
                 database_path: Path|None = None,
                 ):
        self.database_path: Path = (
                database_path
                or DataFolder.generate_rel_path(DataFolder.APP_DATA.value).joinpath('dionysus.db'))
        self.default_avatar_path: Path = (
                default_avatar_path
                or DataFolder.generate_rel_path(DataFolder.DEFAULT_AVATAR.value))
        self.engine: Engine
        self.make_session: sessionmaker

        # check if db file exists/db has appropriate tables etc
        self._init_db()

    def get_classes(self) -> list[ClassIdentifier]:
        """
        Return list of ClassIdentifiers for classes in the database.

        :return: list[ClassIdentifier]
        """
        with self.session_scope() as session:
            return [ClassIdentifier(*class_data)
                    for class_data in session.query(self.Class.id, self.Class.name)]

    def class_name_exists(self, class_name: str) -> bool:
        """
        :param class_name: str
        :return: bool
        """
        with self.session_scope() as session:
            return (class_name,) in session.query(self.Class.name)
            # return [class_name for class_name in session.query(self.Class.name)]

    def create_class(self, new_class: NewClass) -> None:
        """
        Create class data in database.

        Moves avatars for each student to db, changes student.avatar_id
        to id of avatar image in db. If no avatar, this remains None/null,
        and that is stored as student's avatar_id in db.

        :param new_class:
        :return: None
        """
        with self.session_scope() as session:
            added_class = self.Class(name=new_class.name)
            session.add(added_class)
            session.flush()  # Commit to get a class id
            new_class.id = added_class.id

            # Add students:
            for student in new_class:
                if student.avatar_id:
                    # Move avatar from temp to db:
                    avatar_blob = new_class.temp_avatars_dir.joinpath(
                        student.avatar_id).read_bytes()
                    added_avatar = self.Avatar(image=avatar_blob)
                    session.add(added_avatar)
                    session.flush()  # Must flush after each avatar to get the avatar id.
                    student.avatar_id = added_avatar.id

                added_student = self.Student(name=student.name,
                                             class_id=new_class.id,
                                             avatar_id=student.avatar_id,
                                             )
                session.add(added_student)
                session.flush()  # Must flush after each student to get the avatar id.
                # Add id to student:
                student.id = added_student.id

    def load_class(self, class_id: Any) -> Class:
        """
        Load class from database using primary key class.id.

        :param class_id:
        :return: Class
        """
        with self.session_scope() as session:
            class_data = session.query(self.Class, self.Student).filter(
                self.Class.id == self.Student.class_id).filter(
                self.Student.class_id == class_id).all()

            if class_data:
                class_id, class_name = class_data[0][0].id, class_data[0][0].name
                students_list = [Student(student_id=student.id,
                                         name=student.name,
                                         class_id=class_data.id,
                                         avatar_id=student.avatar_id,
                                         ) for class_data, student in class_data]
            else:  # Empty class
                empty_class = session.query(self.Class).filter(self.Class.id == class_id).one()
                students_list = []
                class_id, class_name = empty_class.id, empty_class.name

            return Class(class_id=class_id, name=class_name, students=students_list)

    def update_class(self, class_to_write: Class) -> None:
        """
        Currently unimplemented, as not currently used.

        :param class_to_write: Class
        :return: None
        """
        raise NotImplementedError  # type: ignore

    def get_avatar_path(self, avatar_id: Optional[int]) -> Path:
        """
        Return path to avatar from id.

        Return default avatar if no avatar id.
        Copy avatar image to temp dir using primary key avatar_id as the
        filename.

        Future iteration of chart generation code might facilitate
        returning a binary blob or file-like io.BytesIO object.

        :param avatar_id:
        :return: Path
        """
        if not avatar_id:
            return self.default_avatar_path
        with self.session_scope() as session:
            image_record = session.query(self.Avatar).filter(self.Avatar.id == avatar_id).one()
            image = image_record.image

        temp_image_path = Path(DataFolder.generate_rel_path(DataFolder.TEMP_DIR.value),
                               str(avatar_id))
        temp_image_path.write_bytes(image)
        return temp_image_path

    def create_chart(self, chart_data_dict: dict) -> None:
        """
        Save chart data to database.

        :param chart_data_dict:
        :return: None
        """
        with self.session_scope() as session:
            new_chart = self.Chart(name=chart_data_dict['chart_name'])
            session.add(new_chart)
            session.flush()  # Commit to get a class id
            chart_data_dict['chart_id'] = new_chart.id

            # Create scores in score table
            student_scores_data = []
            for score, students in chart_data_dict['score-students_dict'].items():
                student_scores_data += [self.Score(chart_id=new_chart.id,
                                                   student_id=student.id,
                                                   value=score) for student in students]

            session.add_all(student_scores_data)

    def save_chart_image(self, chart_data_dict: dict, mpl_plt: plt) -> Path:
        """
        Save image in db, and return path to file in temp storage.

        :param chart_data_dict: dict
        :param mpl_plt: matplotlib.pyplot
        :return: Path
        """
        # Get image data:
        image = BytesIO()
        mpl_plt.savefig(image,
                        format='png',
                        dpi=300)  # dpi - 120 comes to 1920*1080, 80 - 1280*720
        image.seek(0)  # Return pointer to start of binary stream.

        # Save image in db
        with self.session_scope() as session:
            chart = session.query(self.Chart).filter_by(id=chart_data_dict['chart_id']).one()
            chart.image = image.read()

            session.commit()
        image.seek(0)

        # Save file to temp and pass back Path
        temp_image_path = Path(DataFolder.generate_rel_path(DataFolder.TEMP_DIR.value),
                               f"{chart_data_dict['chart_name']}.png")
        temp_image_path.write_bytes(image.read())
        return temp_image_path

    def close(self) -> None:
        """
        No close actions needed for this database.

        :return: None
        """
        pass

    def _init_db(self) -> None:
        """
        Instantiates db engine, session manager, create all tables.

        NB For compatibility with existing SQLite db, uses BLOB type, for other
        db or without caring about compatibility, use LargeBinary type.
           Also for student scores, REAL type is used rather than float.

        :return: None
        """
        # Instantiate db engine
        self.engine = create_engine(f'sqlite:///{self.database_path}')  # , echo=True)
        # Instantiate session maker and connect it to db
        self.make_session = sessionmaker()
        self.make_session.configure(bind=self.engine)

        # Define tables
        Base = declarative_base()

        class ClassTable(Base):
            __tablename__ = 'class'

            def __init__(self, name):
                self.name = name

            id = Column(Integer, primary_key=True)
            name = Column(String(255), nullable=False)

            def __repr__(self):
                return f"<Class(id={self.id}, name={self.name})>"

        class StudentTable(Base):
            __tablename__ = 'student'

            def __init__(self, name, class_id, avatar_id=None):
                self.name = name
                self.class_id = class_id
                self.avatar_id = avatar_id

            id = Column(Integer, primary_key=True)
            name = Column(String(255), nullable=False)
            class_id = Column(Integer, ForeignKey('class.id'))
            avatar_id = Column(Integer, ForeignKey('avatar.id'))

            def __repr__(self):
                return (f"<Student("
                        f"id={self.id}, "
                        f"name={self.name}, "
                        f"class_id={self.class_id}, "
                        f"avatar_id={self.avatar_id}"
                        f")>")

        class ChartTable(Base):
            __tablename__ = 'chart'

            def __init__(self, name, image=None, date=None):
                self.name = name
                self.image = image

            id = Column(Integer, primary_key=True)
            name = Column(String(255))
            image = Column(BLOB)
            date = Column(String)

            def __repr__(self):
                return (f"<Chart("
                        f"id={self.id}, "
                        f"name={self.name}, "
                        f"image={self.image}, "
                        f"date={self.date}"
                        f")>")

        class ScoreTable(Base):
            __tablename__ = 'score'

            def __init__(self, chart_id, student_id, value):
                self.chart_id = chart_id
                self.student_id = student_id
                self.value = value

            id = Column(Integer, primary_key=True)
            chart_id = Column(Integer, ForeignKey('chart.id'), nullable=False)
            student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
            value = Column(REAL, nullable=False)

            def __repr__(self):
                return (f"<Score("
                        f"id={self.id}, "
                        f"chart_id={self.chart_id}, "
                        f"student_id={self.student_id}, "
                        f"value={self.value}"
                        f")>")

        class AvatarTable(Base):
            __tablename__ = 'avatar'

            def __init__(self, image):
                self.image = image

            id = Column(Integer, primary_key=True)
            image = Column(BLOB, nullable=False)

            def __repr__(self):
                return f"<Avatar(id={self.id}, image={self.image})>"

        self.Class = ClassTable
        self.Student = StudentTable
        self.Chart = ChartTable
        self.Score = ScoreTable
        self.Avatar = AvatarTable

        # Create all uncreated tables
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session_scope(self) -> Iterator[Session]:
        """
        Create a session to use as a context manager.

        Provide a transactional scope around a series of operations.

        Usage:
        with session_score() as session:
            # do transactions

        :return: Session context
        """
        session = self.make_session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
