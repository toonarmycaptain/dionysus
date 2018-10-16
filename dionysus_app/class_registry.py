"""
Functions dealing with the class registry.
"""

from dionysus_app.data_folder import DataFolder

CLASS_REGISTRY_PATH = DataFolder.generate_rel_path(DataFolder.CLASS_REGISTRY.value)
CLASSLIST_DATA_FILE_TYPE = '.cld'

def cache_class_registry():
# TODO: if the file structure already exists, check for previously created classes
    # Check for a class_registry.index in app_data directory
    #     If list exists, compare with folders (? or .cld files ?) within class_data.
    #         Use pathlib.iterdir() - https://docs.python.org/3.4/library/pathlib.html#basic-use
    #                               - https://stackoverflow.com/a/44228436/7942600
    #     Else check for classes, create class_registry.
    cached_class_registry = generate_registry_from_filesystem()
    return cached_class_registry


    global CLASS_REGISTRY
    CLASS_REGISTRY = generate_registry_from_filesystem()

    return CLASS_REGISTRY  # return value unused on startup


def generate_registry_from_filesystem():

        registry_list =[x.stem for x in CLASSLIST_DATA_PATH.rglob(f'**/*{CLASSLIST_DATA_FILE_TYPE}')]
        return registry_list


def register_class(classlist_name):
    """
    Register class in class_registry file.
    Create if registry non-existent.

    :param classlist_name: str
    :return: None
    """
    with open(CLASS_REGISTRY_PATH, 'a+') as class_registry:  # open class registry, create if does not exist.
        class_registry.write(f'{classlist_name}\n')
