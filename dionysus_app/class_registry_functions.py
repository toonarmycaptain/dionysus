"""
Functions dealing with the class registry.
"""

import definitions

from dionysus_app.data_folder import DataFolder, CLASSLIST_DATA_FILE_TYPE

CLASSLIST_DATA_PATH = DataFolder.generate_rel_path(DataFolder.CLASS_DATA.value)
CLASS_REGISTRY_PATH = DataFolder.generate_rel_path(DataFolder.CLASS_REGISTRY.value)


def cache_class_registry():
    """
    Initialises CLASS_REGISTRY global variable and writes registry to
    disk.

    :return: list
    """

    registry = generate_registry_from_filesystem()
    write_registry_to_disk(registry)
    return registry  # return value unused on startup


def generate_registry_from_filesystem():
    """
    Searches class_data folder for .cld files and returns a list of the
    file names without the extension.

    :return: list
    """
    classlist_data_fullpaths = CLASSLIST_DATA_PATH.rglob(f'**/*{CLASSLIST_DATA_FILE_TYPE}')
    registry_list = [x.stem for x in classlist_data_fullpaths]
    return registry_list


def write_registry_to_disk(registry_list: list):
    """
    Write registry list from cache list to disk.

    :param registry_list: list
    :return: None
    """
    with open(CLASS_REGISTRY_PATH, 'w') as registry_file:
        for classlist_name in registry_list:
            registry_file.write(f'{classlist_name}\n')


def register_class(classlist_name):
    """
    Register class in class_registry file.
    Create if registry non-existent.

    :param classlist_name: str
    :return: None
    """
    definitions.REGISTRY.append(classlist_name)

    # open class registry, create if does not exist.
    with open(CLASS_REGISTRY_PATH, 'a+') as registry:
        registry.write(f'{classlist_name}\n')


def classlist_exists(classlist_name: str):
    """
    Checks if there an entry in CLASS_REGISTRY for the given
    classlist_name.

    :param classlist_name: str
    :return: bool
    """
    return classlist_name in definitions.REGISTRY


def check_registry_on_exit():
    if open(CLASS_REGISTRY_PATH, 'r').readlines() != definitions.REGISTRY:
        write_registry_to_disk(definitions.REGISTRY)


if __name__ == '__main__':
    pass
