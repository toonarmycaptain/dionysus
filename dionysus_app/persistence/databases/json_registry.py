from pathlib import Path
from typing import List, Optional

from dionysus_app.data_folder import DataFolder
from dionysus_app.persistence.databases import json as json_db


class Registry:
    """
    Class registry for a JSONDatabase object.
    ...

    Maintains list of (registered) classes in database. Will attempt to
    save this data to disk on object deletion.


    Attributes
    ----------
    registry_list : List[str]
        List of class name strings.

    app_data_path : Path
        Path to application app_data directory.

    class_data_path : Path
        Path to application class_data directory.

    class_data_file_type : str
        File extension for class data files.

    registry_path : Path
        Path to registry file.

    Methods
    -------
    cache_class_registry():
        Generate registry from disk, write to disk,
        return registry list.

    generate_registry_from_filesystem():
        Searches class_data data files, return list of class names.

    write_registry_to_disk(registry_list: list):
        Write cached registry list to disk.

    register_class(classlist_name: str):
        Register class in class_registry file.

    classlist_exists(classlist_name: str):
        Check for an entry in the registry for the given classlist_name.

    check_registry_on_exit():
        Writes registry to disk on exit if existing invalid/nonexistent.

    """

    def __init__(self,
                 registry_list: List[str] = None,
                 app_data_path: Path = None,
                 class_data_path: Path = None,
                 class_data_file_type: str = None,
                 registry_path: Path = None,
                 ) -> None:
        """
        Constructs Registry object, with defaults for unprovided args.
        
        :param registry_list: str
        :param app_data_path: Path
        :param class_data_path: Path
        :param class_data_file_type: str
        :param registry_path: Path
        :return: None
        """
        self.app_data_path: Path = app_data_path or DataFolder.generate_rel_path(
            DataFolder.APP_DATA.value)
        self.class_data_path: Path = class_data_path or self.app_data_path.joinpath('class_data')
        self.registry_path: Path = registry_path or self.app_data_path.joinpath('class_registry.index')
        self.class_data_file_type: str = class_data_file_type or json_db.DEFAULT_CLASSLIST_DATA_FILE_TYPE
        self.list: List[str] = registry_list or self.cache_class_registry()

    def cache_class_registry(self) -> List[str]:
        """
        Generate registry from disk, write to disk, return registry list.

        Generates registry using class files on disk in
        app_data/class_data, writing to disk, returning registry list.
        Typically used on app start to get registry list.

        :return: List[str]
        """

        registry = self.generate_registry_from_filesystem()
        self.write_registry_to_disk(registry)
        return registry  # return value unused on startup

    def generate_registry_from_filesystem(self) -> List[str]:
        """
        Searches class_data data files, return list of class names.

        Searches class_data directory for file with the
        class_data_file_type extension, returning a list of the file
        names without the extension.

        :return: list
        """
        classlist_data_fullpaths = self.class_data_path.rglob(f'**/*{self.class_data_file_type}')
        return [data_path.stem for data_path in classlist_data_fullpaths]

    def write_registry_to_disk(self, registry_list: list) -> None:
        """
        Write cached registry list to disk.

        :param registry_list: list
        :return: None
        """
        with open(self.registry_path, 'w') as registry_file:
            for classlist_name in registry_list:
                registry_file.write(f'{classlist_name}\n')

    def register_class(self, classlist_name: str) -> None:
        """
        Register class in class_registry file.

        Creates registry file if registry non-existent.

        :param classlist_name: str
        :return: None
        :raises ValueError: If registry is None/uninitialised.
        """
        if self.list is None:
            raise ValueError("RegistryError: Registry uninitialised.")

        self.list.append(classlist_name)

        # open class registry, create if does not exist.
        with open(self.registry_path, 'a+') as registry:
            registry.write(f'{classlist_name}\n')

    def classlist_exists(self, classlist_name: str) -> bool:
        """
        Check for an entry in the registry for the given classlist_name.

        :param classlist_name: str
        :return: bool
        :raises ValueError: If registry is None/uninitialised.
        """
        if self.list is None:
            raise ValueError("RegistryError: Registry uninitialised.")

        return classlist_name in self.list

    def check_registry_on_exit(self) -> None:
        """
        Writes registry to disk on exit if existing invalid/nonexistent.

        Writes registry to disk on exit if the existing file doesn't
        match cached, or the file does not exist.

        :return: None
        :raises ValueError: If registry is None/uninitialised.
        """
        if self.list is None:
            raise ValueError("RegistryError: Registry uninitialised.")
        # Load registry file, if it exists.
        try:
            disk_registry_str: Optional[str] = open(self.registry_path, 'r').read()
        except FileNotFoundError:
            disk_registry_str = None

        if disk_registry_str != ''.join(f'{class_name}\n' for class_name in self.list):
            self.write_registry_to_disk(self.list)

    def __del__(self) -> None:
        """
        Closeout object. Write registry to disk.

        Safeguard in case normal writing of data to disk does not take
        place.

        Check registry file and write current registry list to disk.
        :return: None
        """
        self.check_registry_on_exit()
