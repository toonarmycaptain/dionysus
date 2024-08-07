"""SQLite3 Database object."""
import sqlite3

from io import BytesIO
from pathlib import Path
from typing import Optional

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

    def __init__(self,
                 default_avatar_path: Path|None = None,
                 database_path: Path|None = None,
                 ):
        self.database_path: Path = (
                database_path
                or DataFolder.generate_rel_path(DataFolder.APP_DATA.value).joinpath('dionysus.db'))
        self.default_avatar_path: Path = (
                default_avatar_path
                or DataFolder.generate_rel_path(DataFolder.DEFAULT_AVATAR.value))
        # check if db file exists/db has appropriate tables etc
        self._init_db()

    def get_classes(self) -> list[ClassIdentifier]:
        """
        Return list of ClassIdentifiers for classes in the database.

        :return: list[ClassIdentifier]
        """
        with self._connection() as conn:
            # get list of tuple/list pairs of id, name
            classes = conn.cursor().execute(
                """
                SELECT id,
                       name
                FROM class;
                """).fetchall()
            # convert to ClassIdentifiers
            return [ClassIdentifier(*class_data) for class_data in classes]

    def class_name_exists(self, class_name: str) -> bool:
        """
        :param class_name: str
        :return: bool
        """
        with self._connection() as conn:
            matching_class = conn.cursor().execute(
                """
                SELECT class.name
                FROM class
                WHERE name=?
                LIMIT 1;
                """, (class_name,))
            # Matching_class: no class [] or [('class name',)] if matching class name found.
            return bool(matching_class.fetchone())

    def create_class(self, new_class: NewClass) -> None:
        """
        Create class data in database.

        Moves avatars for each student to db, changes student.avatar_id
        to id of avatar image in db. If no avatar, this remains None/null,
        and that is stored as student's avatar_id in db.

        :param new_class:
        :return: None
        """
        with self._connection() as conn:
            cursor = conn.cursor()
            # insert class into class
            cursor.execute(
                """
                INSERT INTO class(name)
                VALUES(?);
                """, (new_class.name,))
            # Add id to class:
            new_class.id = cursor.lastrowid
            for student in new_class:
                # insert student
                if student.avatar_id:
                    # Move avatar from temp to db:
                    avatar_blob = new_class.temp_avatars_dir.joinpath(
                        student.avatar_id).read_bytes()
                    cursor.execute(
                        """
                        INSERT INTO avatar(image)
                        VALUES(?);
                        """, (avatar_blob,))
                    # Change avatar_id to id of avatar in db.
                    student.avatar_id = cursor.lastrowid
                cursor.execute(
                    """
                    INSERT INTO student(name, class_id, avatar_id)
                    VALUES(?,?,?);
                    """,
                    (student.name, new_class.id, student.avatar_id))

                # Add id to student:
                student.id = cursor.lastrowid
            conn.commit()
        conn.close()

    def load_class(self, class_id: int) -> Class:
        """
        Load class from database using primary key class.id.

        :param class_id:
        :return: Class
        """
        with self._connection() as conn:
            # Get class from db:
            class_data = conn.cursor().execute(
                """
                SELECT class.id,
                       class.name,
                       student.id,
                       student.name,
                       student.avatar_id
                FROM class
                INNER JOIN student
                ON class.id=student.class_id
                WHERE class.id=?;
                """, (class_id,)).fetchall()
            if class_data:
                # Class id, name from first student row returned.
                class_id, class_name = class_data[0][:2]
                # Instantiate student objects:
                students_list = [Student(student_id=student_id,
                                         name=student_name,
                                         class_id=class_id,
                                         avatar_id=avatar,
                                         )
                                 for class_id, class_name, student_id, student_name, avatar
                                 in class_data]

            # Handle empty class (no students = no rows returned:
            else:
                class_id, class_name = conn.cursor().execute(
                    """
                    SELECT class.id,
                           class.name
                    FROM class
                    WHERE class.id=?;
                    """, (class_id,)).fetchone()
                students_list = []
        conn.close()

        return Class(class_id=class_id, name=class_name, students=students_list)

    def update_class(self, class_to_write: Class) -> None:
        """
        Currently unimplemented, as not currently used.

        Initial quick implementation would overwrite all class' data in db,
        future iteration might need to be a diff and just write changed data.
        [Much more efficient for whole class with avatars.]
        Some changes might be able to be applied atomically by the change code,
        - eg a new/added avatar will be added/modified in the student/avatar
         table by the code that facilitates that, rather than by this function.

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
        conn = self._connection()
        image = conn.cursor().execute("""
                                      SELECT image
                                      FROM avatar
                                      WHERE avatar.id=?;
                                      """, (avatar_id,)).fetchone()[0]

        conn.close()
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
        with self._connection() as conn:
            cursor = conn.cursor()

            # Create chart in chart table
            cursor.execute(
                """
                INSERT INTO chart(name)
                VALUES(?);
                """, (chart_data_dict['chart_name'],))
            chart_id = chart_data_dict['chart_id'] = cursor.lastrowid
            # Create scores in score table
            student_scores_data = []
            for score, students in chart_data_dict['score-students_dict'].items():
                student_scores_data += [(chart_id, student.id, score) for student in students]
            cursor.executemany(
                """
                INSERT INTO score(chart_id, student_id, value)
                VALUES(?,?,?);
                """, student_scores_data)
            conn.commit()
        conn.close()

    def save_chart_image(self, chart_data_dict: dict,
                         mpl_plt: plt,  # type: ignore
                         ) -> Path:
        """
        Save image in db, and return path to file in temp storage.

        :param chart_data_dict: dict
        :param mpl_plt: matplotlib.pyplot
        :return: Path
        """
        # Get image data:
        image = BytesIO()
        mpl_plt.savefig(image,  # type: ignore[attr-defined]
                        format='png',
                        dpi=300)  # dpi - 120 comes to 1920*1080, 80 - 1280*720
        image.seek(0)  # Return pointer to start of binary stream.

        # Save image in db
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE chart
                SET image=?
                WHERE id=?;
                """, (image.read(), chart_data_dict['chart_id']))
            image.seek(0)
            conn.commit()
        conn.close()

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

    def _connection(self) -> sqlite3.Connection:
        """
        Return connection to database.

        Execute command enforcing foreign key support in SQLite.
        Errors connecting to on-disk db not handled. Errors indicate a
        real error, likely a corrupt/non-db file, or too many connections,
        and needs attention.

        :return: sqlite3.Connection
        """
        connection = sqlite3.connect(self.database_path)
        # Ensure foreign key constraint enforcement.
        connection.cursor().execute("""PRAGMA foreign_keys=ON;""")
        return connection

    def _init_db(self):
        """
        Create empty database.
        Function could have better name.

        :return: None
        """
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
        """
        Return sql statement to create class table in db.

        :return: str
        """
        return """CREATE TABLE IF NOT EXISTS class(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        -- Ensure name is type text no longer than 255 characters:
                        name TEXT NOT NULL CHECK(typeof("name") = 'text' AND
                                                 length("name") <= 255
                                                 )
                        );
                        """

    def _create_table_student(self) -> str:
        """
        Return sql statement to create student table in db.

        :return: str
        """
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
        """
        Return sql statement to create chart table in db.

        :return: str
        """
        return """CREATE TABLE IF NOT EXISTS chart(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL CHECK(typeof("name") = 'text' AND
                                                 length("name") <= 255
                                                 ),
                        image BLOB, -- NOT NULL, needs to be null, as chart data/image saved independently.
                        date TEXT -- For now can be NULL, will be implemented later.
                        );
                        """

    def _create_table_score(self) -> str:
        """
        Return sql statement to create score table in db.

        :return: str
        """
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
        """
        Return sql statement to create avatar table in db.

        :return: str
        """
        return """CREATE TABLE IF NOT EXISTS avatar(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        image BLOB NOT NULL
                        );
                        """
