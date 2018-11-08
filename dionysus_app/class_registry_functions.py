"""
Functions dealing with the class registry.
"""

import class_registry

from dionysus_app.data_folder import DataFolder, CLASSLIST_DATA_FILE_TYPE

CLASSLIST_DATA_PATH = DataFolder.generate_rel_path(DataFolder.CLASS_DATA.value)
CLASS_REGISTRY_PATH = DataFolder.generate_rel_path(DataFolder.CLASS_REGISTRY.value)



def cache_class_registry():

    global CLASS_REGISTRY
    CLASS_REGISTRY = generate_registry_from_filesystem()
    write_registry_to_disk(CLASS_REGISTRY)

    return CLASS_REGISTRY  # return value unused on startup


def generate_registry_from_filesystem():
    classlist_data_fullpaths = CLASSLIST_DATA_PATH.rglob(f'**/*{CLASSLIST_DATA_FILE_TYPE}')
    registry_list = [x.stem for x in classlist_data_fullpaths]
    return registry_list


def write_registry_to_disk(registry_list: list):
    """
    Write registry list from cache list to disk.

    :param registry_list: list
    :return: None
    """
    with open(CLASS_REGISTRY_PATH, 'w') as class_registry:
        for classlist_name in registry_list:
            class_registry.write(f'{classlist_name}\n')


def register_class(classlist_name):
    """
    Register class in class_registry file.
    Create if registry non-existent.

    :param classlist_name: str
    :return: None
    """
    class_registry.REGISTRY.append(classlist_name)

    CLASS_REGISTRY.append(classlist_name)

    with open(CLASS_REGISTRY_PATH, 'a+') as class_registry:  # open class registry, create if does not exist.
        class_registry.write(f'{classlist_name}\n')


def classlist_exists(classlist_name):  # TODO: use class_registry list instead.
    """
    Checks if there an entry in CLASS_REGISTRY for the given classlist_name.

    :param classlist_name: str
    :return: bool
    """
    return classlist_name in class_registry.REGISTRY


def check_registry_on_exit():
    if open(CLASS_REGISTRY_PATH, 'r').readlines() != class_registry.REGISTRY:
        write_registry_to_disk(class_registry.REGISTRY)

if __name__ == '__main__':
    print(cache_class_registry())
