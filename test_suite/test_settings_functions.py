"""Test settings functions.py"""

from unittest import TestCase
from unittest.mock import patch

from dionysus_app.settings_functions import (app_start_set_default_chart_save_location,
                                             )


class TestAppStartSetDefaultChartSaveLocation(TestCase):
    @patch('dionysus_app.settings_functions.set_default_chart_save_location')
    @patch('dionysus_app.settings_functions.user_decides_to_set_default_location')
    def test_app_start_set_default_chart_save_location_user_set(
            self,
            mocked_user_decides_to_set_default_location,
            mocked_set_default_chart_save_location,
            ):
        mocked_user_decides_to_set_default_location.return_value = True

        assert app_start_set_default_chart_save_location() is None

        mocked_user_decides_to_set_default_location.assert_called_once_with()
        mocked_set_default_chart_save_location.assert_called_once_with(
                user_set=mocked_user_decides_to_set_default_location.return_value)

    @patch('dionysus_app.settings_functions.set_default_chart_save_location')
    @patch('dionysus_app.settings_functions.user_decides_to_set_default_location')
    def test_app_start_set_default_chart_save_location_app_set(
            self,
            mocked_user_decides_to_set_default_location,
            mocked_set_default_chart_save_location,
            ):
        mocked_user_decides_to_set_default_location.return_value = False

        assert app_start_set_default_chart_save_location() is None

        mocked_user_decides_to_set_default_location.assert_called_once_with()
        mocked_set_default_chart_save_location.assert_called_once_with(
                user_set=mocked_user_decides_to_set_default_location.return_value)
