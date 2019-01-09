import unittest


from dionysus_app.class_registry_functions import register_class


class TestLoadNonexistentRegistryWithNoClassData(unittest.TestCase):
    pass
    # setup:
    #     dummy CLASS_REGISTRY_PATH?
    #
    # confirm blank registry created on startup when no data exists
    # confirm empty cached registry dict/global


class TestLoadExistingRegistry(unittest.TestCase):
    pass
    # setup:
    #     dummy CLASS_REGISTRY_PATH?
    #     dummy class data (existent classes)
    #
    # confirm registry file created on startup
    # confirm registry dict/global created on startup
    # confirm created registry file has correct data
    # confirm created registry dict/global has correct data


class TestLoadNonexistentRegistryWithClassData:
    pass
    # setup:
    #     dummy CLASS_REGISTRY_PATH?
    #     dummy class data (existent classes)
    #
    # confirm registry file created on startup
    # confirm registry dict/global created on startup
    # confirm created registry file has correct data

class TestAddClassToNewRegistry(unittest.TestCase):
    pass
    # setup:
    #     dummy CLASS_REGISTRY_PATH?
    #     dummy classlist_name
    #
    # test add class to registry
    # confirm registry created
    # confirm classlist_name in cached registry dict
    # confirm classlist_name in registry file


class TestAddClassExistingRegistry(unittest.TestCase):
    pass
    # setup:
    #     dummy CLASS_REGISTRY_PATH?
    #     dummy existing class registry
    #     dummy classlist_name
    #
    # test add class to registry
    # confirm classlist_name in cached registry dict
    # confirm classlist_name in registry file
