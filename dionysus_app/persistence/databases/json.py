""" JSON Database object """
from copy import deepcopy
from pathlib import Path
from typing import List, Optional

import matplotlib.pyplot as plt

import definitions

from dionysus_app.class_ import Class, NewClass
from dionysus_app.data_folder import DataFolder
from dionysus_app.file_functions import convert_to_json, move_file
from dionysus_app.persistence.database import ClassIdentifier, Database
from dionysus_app.persistence.databases.json_registry import Registry

DEFAULT_CLASSLIST_DATA_FILE_TYPE = '.cld'
DEFAULT_CHART_DATA_FILE_TYPE = '.cdf'


class JSONDatabase(Database):
    """
    JSONDatabase object
    ...


    Attributes
    ----------
    app_data_path : Path
        Path to application app_data dir.

    class_data_path : Path
        Path to application class_data dir.

    class_data_file_type : str
        File extension for class data files.

    default_chart_save_dir : Path
        Path to default user chart save directory.

    default_avatar_path : Path
        Path to the default avatar.

    chart_data_file_type : str

    _registry_path : Path
        Path to registry file.

    _registry : Registry
        Class Registry object for the database, manages list of classes.


    Methods
    _______
    get_classes():
        Return list of classes in the database.

    class_name_exists(class_id: str):
        Return bool if class name already exists in the database.

    create_class(new_class: NewClass):
        Take a Class object and create/write the class in the database.

    load_class(class_id: Any):
        Load a class from the database.

    update_class(class_to_write: Class):
        Update existing class record.

    get_avatar_path(self, avatar_id: Any):
        Not implemented for JSONDatabase.

    create_chart(chart_data_dict: dict):
        Save chart data to disk as JSON in class' chart_data folder.

    save_chart_image(chart_data_dict: dict, mpl_plt: plt):
        Save image, and return path file in application storage.

    get_avatar_path_class_filename(class_name: str, student_avatar: str):
        Get path to avatar image.

    close():
        Closeout database.

    """

    def __init__(self,
                 app_data_path: Path = None,
                 class_data_path: Path = None,
                 class_data_file_type: str = None,
                 chart_data_file_type: str = None,
                 default_chart_save_dir: Path = None,
                 default_avatar_path: Path = None,
                 registry_path: Path = None,
                 registry: Registry = None,
                 ):
        """
        Constructs the JSONDatabase object, with defaults for unprovided args.

        NB: default_chart_save_dir has type Optional[Path] because
            definitions.DEFAULT_CHART_SAVE_dir has type Optional[Path] as it
            is uninitialised as None.

        :param app_data_path: Path
        :param class_data_path: Path
        :param class_data_file_type: str
        :param chart_data_file_type: str
        :param default_chart_save_dir: Path
        :param registry_path: Path
        :param registry: Registry
        """
        super().__init__()
        self.app_data_path: Path = (app_data_path
                                    or DataFolder.generate_rel_path(DataFolder.APP_DATA.value))
        self.class_data_path: Path = class_data_path or self.app_data_path.joinpath('class_data')
        self.class_data_file_type: str = class_data_file_type or DEFAULT_CLASSLIST_DATA_FILE_TYPE
        self.default_chart_save_dir: Optional[Path] = (default_chart_save_dir
                                                       or definitions.DEFAULT_CHART_SAVE_DIR)
        self.default_avatar_path: Path = (
                default_avatar_path
                or DataFolder.generate_rel_path(DataFolder.DEFAULT_AVATAR.value))
        self.chart_data_file_type: str = chart_data_file_type or DEFAULT_CHART_DATA_FILE_TYPE
        # Create data paths:
        self.app_data_path.mkdir(parents=True, exist_ok=True)
        self.class_data_path.mkdir(parents=True, exist_ok=True)
        # Initialise class registry:
        self._registry_path: Path = (registry_path
                                     or self.app_data_path.joinpath('class_registry.index'))
        self._registry: Registry = (registry
                                    or Registry(app_data_path=self.app_data_path,
                                                class_data_path=self.class_data_path,
                                                registry_path=self._registry_path,
                                                class_data_file_type=self.class_data_file_type
                                                ))

    def get_classes(self) -> List[ClassIdentifier]:
        """
        Return list of classes in the database.
        Tuples of (class_name, class_name),, since class_id in JSON
        is the class' name.

        :return: List[Tuple[str, str]]
        """
        return [ClassIdentifier(class_name, class_name)
                for class_name in self._registry.list]

    def class_name_exists(self, class_name: str) -> bool:
        """
        Return bool if class name already exists in the database.

        :param class_name: str
        :return: bool
        """
        return self._registry.classlist_exists(class_name)

    def create_class(self, new_class: NewClass) -> None:
        """
        Take a Class object and create/write the class in the database.

        Creates class data in persistence.
        Calls setup_class to create any needed files, then writes data to file.

        :param new_class: Class object
        :return: None
        """
        self._setup_class(new_class.name)
        self._write_classlist_to_file(new_class)
        self._move_avatars_to_class_data(new_class)

    def load_class(self, class_id: str) -> Class:
        """
        Load a class from the database.

        Load class data from a class data ('.cld') file, return Class object.

        :param class_id: str - the class' name
        :return: Class object
        """
        class_data_filename = class_id + self.class_data_file_type
        classlist_data_path = self.class_data_path.joinpath(class_id, class_data_filename)

        return Class.from_file(classlist_data_path)

    def update_class(self, class_to_write: Class) -> None:
        """
        Update existing class record.

        :param class_to_write: Class object.
        :return: None
        """
        self._write_classlist_to_file(class_to_write)

    def get_avatar_path(self, avatar_id: int):
        raise NotImplementedError

    def create_chart(self, chart_data_dict: dict) -> None:
        """
            Save chart data to disk as JSON in class' chart_data folder.

            Filename is chart name sanitised to a suitable string.

            Pathlib Path objects are not json-serializable, so data dict is converted to
            a JSON-safe form before conversion to JSON

            Write classlist data to disk with format:
            chart_data_dict = {
                        'class_name': class_name,  str
                        'chart_name': chart_name,  str
                        'chart_default_filename': chart_default_filename,  str
                         # date? Not yet implemented.
                        'chart_params': chart_params,  dict
                            dict of chart parameters and settings
                        'score-avatar_dict': student_scores,  dict
                        }

            CAUTION: conversion to JSON will convert int/float keys in score_avatar_dict
            to strings, and keep them as strings when loading.
            This could be handled if necessary by running something like:
            original_score_avatar_dict = {
                float(score): avatar_list for score, avatar_list
                                in dejsonified_score_avatar_dict.items()}

            :param chart_data_dict: dict
            :return: None
            """
        file_chart_data_dict = deepcopy(chart_data_dict)  # Copy so as to not modify in-use dict.

        chart_filename = file_chart_data_dict['chart_default_filename']
        chart_data_file = chart_filename + self.chart_data_file_type
        chart_data_filepath = self.class_data_path.joinpath(
            file_chart_data_dict['class_name'], 'chart_data', chart_data_file)

        # Convert data_dict to JSON-safe form.
        json_safe_chart_data_dict = self._sanitise_avatar_path_objects(file_chart_data_dict)
        json_chart_data = convert_to_json(json_safe_chart_data_dict)

        with open(chart_data_filepath, 'w') as chart_data_file:
            chart_data_file.write(json_chart_data)

    def save_chart_image(self, chart_data_dict: dict, mpl_plt: plt) -> Path:
        """
        Save image, and return path file in application storage.

        Save to app_data/classname/chart_data with same filename as
        chart_name and chart_data_file name.

        NB User copy stored elsewhere.

        :param chart_data_dict: dict
        :param mpl_plt: plt - matplotlib.pyplot object
        :return: Path
        """
        class_name = chart_data_dict['class_name']
        default_chart_name = chart_data_dict['chart_default_filename']
        app_data_save_pathname = self.class_data_path.joinpath(class_name,
                                                               'chart_data',
                                                               f"{default_chart_name}.png")
        Path.mkdir(app_data_save_pathname.parent, parents=True, exist_ok=True)
        # Save in app_data/class_data/class_name/chart_data with chart_default_filename

        mpl_plt.savefig(app_data_save_pathname,
                        dpi=120)  # dpi - 120 comes to 1920*1080, 80 - 1280*720
        return app_data_save_pathname

    def get_avatar_path_class_filename(self, class_name: str,
                                       student_avatar_filename: str = None) -> Path:
        """
        Return abs path to student avatar, or to default avatar if None.

        Defaults to default avatar if none provided.

        :param class_name: str
        :param student_avatar_filename: str or None
        :return: Path object
        """
        if student_avatar_filename is None:
            return self.default_avatar_path
        return self._avatar_path_from_string(class_name, student_avatar_filename)

    def _avatar_path_from_string(self, class_name: str, avatar_filename: str) -> Path:
        """
        Return abs path to student avatar image.

        Take class name and student's avatar filename, return a Path
        object to the avatar image file.

        :param class_name: str
        :param avatar_filename: str
        :return: Path object
        """
        return self.class_data_path.joinpath(class_name, 'avatars', avatar_filename)

    def close(self) -> None:
        """
        Closeout database.

        Ensure correct registry on disk.

        :return: None
        """
        self._registry.check_registry_on_exit()

    def _setup_class(self, classlist_name: str) -> None:
        """
        Setup class data storage file structure.
        Register class in class_registry index

        :param classlist_name:
        :return: None
        """
        self._setup_class_data_storage(classlist_name)
        self._registry.register_class(classlist_name)

    def _setup_class_data_storage(self, classlist_name: str) -> None:
        """
        Setup data storage for new classes.

        Structure for data storage:
        app_data/
            class_data/
                class_name/  # dir for each class
                    chart_data/  # store chart data sets
                    avatars/  # store avatars for class

        Raises ValueError on uninitialised self.default_chart_save_dir value: value
        should be previously set in:
        run_app
            app_init
                app_config
                    app_start_set_default_chart_save_location


        :param classlist_name: str
        :return: None
        :raises ValueError: If default_chart_save_dir is None/uninitialised.
        """
        avatar_path = self.class_data_path.joinpath(classlist_name, 'avatars')
        chart_path = self.class_data_path.joinpath(classlist_name, 'chart_data')
        if self.default_chart_save_dir is None:
            raise ValueError("Uninitialised DEFAULT_CHART_SAVE_dir")
        user_chart_save_dir = self.default_chart_save_dir.joinpath(classlist_name)

        avatar_path.mkdir(exist_ok=True, parents=True)
        chart_path.mkdir(exist_ok=True, parents=True)
        user_chart_save_dir.mkdir(exist_ok=True, parents=True)

    def _write_classlist_to_file(self, current_class: Class) -> None:
        """
        Write classlist data to disk as JSON dict, according to Class object's
        Class.json_dict and Class.to_json_str methods.

        CAUTION: conversion to JSON will convert int/float keys to strings, and
        keep them as strings when loading.

        :param current_class: Class object
        :return: None
        """
        class_name = current_class.name
        data_filename = class_name + self.class_data_file_type
        classlist_data_path = self.class_data_path.joinpath(class_name, data_filename)

        json_class_data = current_class.to_json_str()

        # Make data path if it doesn't exist.
        classlist_data_path.parent.mkdir(parents=True, exist_ok=True)

        with open(classlist_data_path, 'w') as classlist_file:
            classlist_file.write(json_class_data)

    def _move_avatars_to_class_data(self, new_class: NewClass) -> None:
        """
        Move avatars from NewClass.temp_dir  to new class' avatars directory.

        :param new_class: NewClass
        :return: None
        """
        for avatar_file in [student.avatar_id for student in new_class.students
                            if student.avatar_id]:
            self._move_avatar_to_class_data(new_class, avatar_file)

    def _move_avatar_to_class_data(self, new_class: NewClass,
                                   avatar_filename: str) -> None:
        """
        Moves avatar from NewClass.temp_dir to new class' avatars dir.

        Will not repeat moves of same filename if image already exists in
        avatars directory, to avoid repeated overwrite with same file.

        :param new_class: NewClass
        :param avatar_filename: str
        :return: None
        """
        origin_path = new_class.temp_avatars_dir.joinpath(avatar_filename)
        destination_path = self.class_data_path.joinpath(new_class.name,
                                                         'avatars',
                                                         avatar_filename)
        if not destination_path.exists():  # Avatar not already in database/class data.
            move_file(origin_path, destination_path)

    def _sanitise_avatar_path_objects(self, data_dict: dict) -> dict:
        """
        Convert path objects in chart data_dict to strings.

        Necessary to convert dict to JSON string for saving to disk.

        chart_data_dict['score-avatar_dict'] is a dict with integer
        keys, lists of Path objects as values.

        Possible TODO: change to save student name as well as path to avatar used?

        :param data_dict: dict
        :return: dict
        """
        for score in list(data_dict['score-avatar_dict'].keys()):
            data_dict['score-avatar_dict'][score] = [str(avatar_Path) for avatar_Path
                                                     in data_dict['score-avatar_dict'][score]]
        return data_dict
