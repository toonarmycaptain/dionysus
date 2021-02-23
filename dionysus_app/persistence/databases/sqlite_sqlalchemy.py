"""SQLAlchemy SQLite3 Database object ."""
from contextlib import contextmanager
from pathlib import Path
from typing import (Any,
                    ContextManager,
                    List,
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
from sqlalchemy.orm.decl_api import DeclarativeMeta

from dionysus_app.class_ import Class, NewClass
from dionysus_app.data_folder import DataFolder
from dionysus_app.student import Student
from dionysus_app.persistence.database import ClassIdentifier, Database


class SQLiteSQLAlchemyDatabase(Database):
    def __init__(self, default_avatar_path: Path = None,
                 database_path: Path = None,
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

    def get_classes(self) -> List[ClassIdentifier]:
        with self.session_scope() as session:
            return [ClassIdentifier(*class_data)
                    for class_data in session.query(self.Class.id, self.Class.name)]

    def class_name_exists(self, class_name: str) -> bool:
        with self.session_scope() as session:
            return (class_name,) in session.query(self.Class.name)
            # return [class_name for class_name in session.query(self.Class.name)]

    def create_class(self, new_class: NewClass) -> None:
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
                    session.flush()
                    student.avatar_id = added_avatar.id

                added_student = self.Student(name=student.name,
                                             class_id=new_class.id,
                                             avatar_id=student.avatar_id,
                                             )
                session.add(added_student)
                session.flush()
                # Add id to student:
                student.id = added_student.id

    def load_class(self, class_id: Any) -> Class:
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
            else:
                class_data = session.query(self.Class).filter(self.Class.id == class_id).first()
                students_list = []
                class_id, class_name = class_data.id, class_data.name

            return Class(class_id=class_id, name=class_name, students=students_list)

    def update_class(self, class_to_write: Class) -> None:
        pass

    def create_chart(self, chart_data_dict: dict) -> None:
        pass

    def save_chart_image(self, chart_data_dict: dict, mpl_plt: plt) -> Path:
        pass

    def close(self) -> None:
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
        self.engine = create_engine(f'sqlite:///{self.database_path}', echo=True)
        # Instantiate session maker and connect it to db
        self.make_session = sessionmaker()
        self.make_session.configure(bind=self.engine)
        Base: DeclarativeMeta = declarative_base()

        class ClassTable(Base):
            __tablename__ = 'class'

            id = Column(Integer, primary_key=True)
            name = Column(String(255), nullable=False)

            def __repr__(self):
                return f"<Class(id={self.id}, name={self.name})>"

        class StudentTable(Base):
            __tablename__ = 'student'

            id = Column(Integer, primary_key=True)
            name = Column(String(255), nullable=False)
            class_id = Column(Integer, ForeignKey('class.id'))
            avatar_id = Column(Integer, ForeignKey('avatar.id'))

            def __repr__(self):
                return f"<Student(id={self.id}, name={self.name}, class_id={self.class_id}, avatar_id={self.avatar_id})>"

        class ChartTable(Base):
            __tablename__ = 'chart'

            id = Column(Integer, primary_key=True)
            name = Column(String(255))
            image = Column(BLOB)
            date = Column(String)

        class ScoreTable(Base):
            __tablename__ = 'score'

            id = Column(Integer, primary_key=True)
            chart_id = Column(Integer, ForeignKey('chart.id'), nullable=False)
            student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
            value = Column(REAL, nullable=False)

        class AvatarTable(Base):
            __tablename__ = 'avatar'

            id = Column(Integer, primary_key=True)
            image = Column(BLOB, nullable=False)

        self.Class = ClassTable
        self.Student = StudentTable
        self.Chart = ChartTable
        self.Score = ScoreTable
        self.Avatar = AvatarTable

        # Create all uncreated tables
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session_scope(self) -> ContextManager[Session]:
        """
        Create a session to use as a context manager.

        Provide a transactional scope around a series of operations.

        Usage:
        with session_score() as session:
            # do transactions

        :param self:
        :return:
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
