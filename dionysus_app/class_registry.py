"""
Functions dealing with the class registry.
"""

from dionysus_app.data_folder import DataFolder

CLASS_REGISTRY_PATH = DataFolder.generate_rel_path(DataFolder.CLASS_REGISTRY.value)

def register_class(classlist_name):
    """
    Register class in class_registry file.
    Create if registry non-existent.

    :param classlist_name: str
    :return: None
    """
    with open(CLASS_REGISTRY_PATH, 'a+') as class_registry:  # open class registry, create if does not exist.
        class_registry.write(f'{classlist_name}\n')
