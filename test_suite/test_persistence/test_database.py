""" Test Database abstract base class """
# Subclass and test that class errors when trying to instantiate subclass without implementing each function.
import abc

import pytest

from pathlib import Path
from typing import List

import matplotlib.pyplot as plt

from dionysus_app.class_ import Class, NewClass

from dionysus_app.persistence.database import (ABCMetaEnforcedAttrs,
                                               ClassIdentifier,
                                               Database,
                                               )


class EmptyGenericDatabase(Database):
    """
    Generic database object without defined methods.

    Required attribute default_avatar_path instantiated to None.

    Replace methods if behaviour is desired.
    """

    def __init__(self):
        super().__init__()
        self.default_avatar_path: Path = None

    def get_classes(self) -> List[ClassIdentifier]:
        raise NotImplementedError

    def class_name_exists(self, class_name: str) -> bool:
        raise NotImplementedError

    def create_class(self, new_class: NewClass) -> None:
        raise NotImplementedError

    def load_class(self, class_id: int) -> Class:
        raise NotImplementedError

    def update_class(self, class_to_write: Class) -> None:
        raise NotImplementedError

    def get_avatar_path(self, avatar_id: int):
        raise NotImplementedError

    def create_chart(self, chart_data_dict: dict) -> None:
        raise NotImplementedError

    def save_chart_image(self, chart_data_dict: dict, mpl_plt: plt) -> Path:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError


@pytest.fixture
def empty_generic_database():
    return EmptyGenericDatabase()


class TestDatabaseRequiredAttrs:
    @pytest.mark.parametrize('has_required_attrs', [True, False])
    def test_required_attrs_not_present_raising_error(self, has_required_attrs):
        """Do not instantiate subclass without required attrs."""

        class SubclassRequiresAttrs(abc.ABC, metaclass=ABCMetaEnforcedAttrs):
            required_attributes = ['some_required_attr']

        class Subclass(SubclassRequiresAttrs):
            def __init__(self):
                if has_required_attrs:
                    self.some_required_attr = 'present'

        if has_required_attrs:  # Ensure able to instantiate with required attrs:
            Subclass()
        if not has_required_attrs:
            with pytest.raises(TypeError):
                Subclass()
