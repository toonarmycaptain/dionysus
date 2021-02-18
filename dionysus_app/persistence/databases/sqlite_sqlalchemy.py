"""SQLAlchemy SQLite3 Database object ."""
from contextlib import contextmanager
from pathlib import Path
from typing import (Any,
                    ContextManager,
                    List,
                    Union,
                    )

from matplotlib import pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy import (BLOB,
                        Column,
                        ForeignKey,
                        Integer,
                        REAL,
                        String,
                        )
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (relationship,
                            sessionmaker,
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
        # check if db file exists/db has appropriate tables etc
        self._init_db()

    def get_classes(self) -> List[ClassIdentifier]:
        pass

    def class_name_exists(self, class_name: str) -> bool:
        pass

    def create_class(self, new_class: NewClass) -> None:
        pass

    def load_class(self, class_id: Any) -> Class:
        pass

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
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

        Base = declarative_base()

        class ClassTable(Base):
            __tablename__ = 'class'

            id = Column(Integer, primary_key=True)
            name = Column(String(255), nullable=False)

            def __repr__(self):
                ...
                return f"<User(id={self.id}, name={self.name}"

        class StudentTable(Base):
            __tablename__ = 'student'

            id = Column(Integer, primary_key=True)
            name = Column(String(255), nullable=False)
            class_id = Column(Integer, ForeignKey('class.id'))
            avatar_id = Column(Integer, ForeignKey('avatar.id'))

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
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
