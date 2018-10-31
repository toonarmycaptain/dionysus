import unittest

from dionysus_app.class_registry import register_class


class TestLoadNonexistentRegistry(unittest.TestCase):
    pass


class TestLoadExistingRegistry(unittest.TestCase):
    pass


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
