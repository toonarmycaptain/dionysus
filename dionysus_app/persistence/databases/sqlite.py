import sqlite3

from pathlib import Path
from typing import Any, List

import matplotlib.pyplot as plt

from dionysus_app.class_ import Class, NewClass
from dionysus_app.data_folder import DataFolder
from dionysus_app.student import Student
from dionysus_app.persistence.database import ClassIdentifier, Database


class SQLiteDatabase(Database):
    """
    SQLiteDatabase object.

    Database implemented using python SQLite3 module.

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
            key `date` - chart created date TODO: document

        Table: `score` - scores in charts
            key `id` - INTEGER primary key
            key `chart_id` - INTEGER `chart.id` score belongs to
            key `student_id` - INTEGER `student.id` score belongs to
            key `value` - REAL (ie float) the score

        Table: `avatar`
            key `id` - INTEGER primary key
            key `image` blob
    """

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
        """
        Return list of ClassIdentifiers for classes in the database.

        :return: List[ClassIdentifier]
        """
        with self._connection() as conn:
            # get list of tuple/list pairs of id, name
            classes = conn.cursor().execute("""SELECT id, name FROM class;""").fetchall()
            # convert to ClassIdentifiers
            return [ClassIdentifier(*class_data) for class_data in classes]

    def class_name_exists(self, class_name: str) -> bool:
        with self._connection() as conn:
            matching_class = conn.cursor().execute("""SELECT class.name FROM class 
                                                   WHERE name=? LIMIT 1""", (class_name,))
            # Will return either no class [] or [('class name',)] if matching class name found.
            return bool(matching_class.fetchone())

    def create_class(self, new_class: NewClass) -> None:
        """

        Moves avatars for each student to db, changes student.avatar_id
        to id of avatar image in db. If no avatar, this remains None/null,
        and that is stored as student's avatar_id in db.

        :param new_class:
        :return:
        """
        with self._connection() as conn:
            cursor = conn.cursor()
            # insert class into class
            cursor.execute("""INSERT INTO class(name) VALUES(?)""", (new_class.name,))
            # Add id to class:
            new_class.id = cursor.lastrowid
            for student in new_class:
                # insert student
                if student.avatar_id:
                    # Move avatar from temp to db:
                    avatar_blob = new_class.temp_avatars_dir.joinpath(student.avatar_id).read_bytes()
                    cursor.execute("""INSERT INTO avatar(image) VALUES(?)""", (avatar_blob,))
                    # Change avatar_id to id of avatar in db.
                    student.avatar_id = cursor.lastrowid
                cursor.execute(
                    """INSERT INTO student(name, class_id, avatar_id) VALUES(?,?,?)""",
                    (student.name, new_class.id, student.avatar_id))

                # Add id to student:
                student.id = cursor.lastrowid
            conn.commit()
        conn.close()

    def load_class(self, class_id: int) -> Class:
        with self._connection() as conn:
            # Get class from db, use 'loaded_class_id' to avoid name clash with class_id when loading student.
            loaded_class_id, class_name = conn.cursor().execute(
                """SELECT * FROM class WHERE class.id=?""", (class_id,)).fetchone()
            # Get student data for class:
            students_data = conn.cursor().execute(
                """SELECT * FROM student WHERE student.class_id=?""", (loaded_class_id,)).fetchall()
            # Instantiate student objects:
            students_list = [Student(id=id, name=name, class_id=class_id, avatar_id=avatar)
                             for student_id, name, class_id, avatar in students_data]
        conn.close()

        return Class(class_id=loaded_class_id, name=class_name, students=students_list)

    def update_class(self, class_to_write: Class) -> None:
        return NotImplementedError  # type: ignore

    def get_avatar_path(self, avatar_id: Any) -> Path:
        return NotImplementedError  # type: ignore

    def create_chart(self, chart_data_dict: dict) -> None:
        return NotImplementedError  # type: ignore

    def save_chart_image(self, chart_data_dict: dict, mpl_plt: plt) -> Path:
        return NotImplementedError  # type: ignore

    def close(self) -> None:
        return NotImplementedError  # type: ignore

    def _connection(self) -> sqlite3.Connection:

        connection = sqlite3.connect(self.database_path)
        # Ensure foreign key constraint enforcement.
        connection.cursor().execute("""PRAGMA foreign_keys=ON;""")
        # print("Connection to SQLite DB successful")
        return connection
        # handle case where connection fails?
        # or should it fail, since on disk db connection should not fail?

    def _init_db(self):
        """Create empty database.
        Function could have better name."""
        table_creation_functions = [self._create_table_class,
                                    self._create_table_student,
                                    self._create_table_chart,
                                    self._create_table_score,
                                    self._create_table_avatar,
                                    ]

        connection = self._connection()

        for create_table_query in table_creation_functions:
            connection.cursor().execute(create_table_query())
            connection.commit()
        connection.close()

    def _create_table_class(self) -> str:
        return """CREATE TABLE IF NOT EXISTS class(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        -- Ensure name is type text no longer than 255 characters: 
                        name TEXT NOT NULL CHECK(typeof("name") = 'text' AND
                                                 length("name") <= 255
                                                 )
                        );
                        """

    def _create_table_student(self) -> str:
        return """CREATE TABLE IF NOT EXISTS student(
                        -- primary key must be INTEGER not INT, NOT NULL is implicit, or error/autoincrement won't work.
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        name TEXT NOT NULL CHECK(typeof("name") = 'text' AND
                                                 length("name") <= 255
                                                 ),
                        class_id INTEGER,
                        avatar_id INTEGER,
                        FOREIGN KEY (class_id) REFERENCES class (id),
                        FOREIGN KEY(avatar_id) REFERENCES avatar(id)
                        );
                        """

    def _create_table_chart(self) -> str:
        return """CREATE TABLE IF NOT EXISTS chart(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL CHECK(typeof("name") = 'text' AND
                                                 length("name") <= 255
                                                 ),
                        date TEXT -- For now can be NULL, will be implemented later.
                        );
                        """

    def _create_table_score(self) -> str:
        return """CREATE TABLE IF NOT EXISTS score(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        chart_id INTEGER NOT NULL,
                        student_id INTEGER NOT NULL,
                        value REAL NOT NULL, --REAL is equivalent of float.
                        FOREIGN KEY(chart_id) REFERENCES chart(id),
                        FOREIGN KEY(student_id) REFERENCES student(id)
                        );
                        """

    def _create_table_avatar(self) -> str:
        return """CREATE TABLE IF NOT EXISTS avatar(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        image BLOB NOT NULL
                        );
                        """
