"""Test settings functions.py"""

from unittest import TestCase
from unittest.mock import patch

from dionysus_app.settings_functions import (app_start_set_default_chart_save_location,
                                )


class TestAppStartSetDefaultChartSaveLocation(TestCase):
    def setUp(self):
        self.welcome_print_stmt = (
            'Welcome to dionysus.\n'
            'It looks like this is your first time running the program.\n\n'
            'Would you like to set a default location to save your charts?\n'
            'You can do this later or change your selection in Settings.\n'
            )

    @patch('dionysus_app.settings_functions.clear_screen')
    @patch('dionysus_app.settings_functions.set_default_chart_save_location')
    @patch('dionysus_app.settings_functions.user_decides_to_set_default_location')
    @patch('dionysus_app.settings_functions.print')
    def test_app_start_set_default_chart_save_location_user_set(
            self,
            mocked_print,
            mocked_user_decides_to_set_default_location,
            mocked_set_default_chart_save_location,
            mocked_clear_screen,
            ):
        mocked_user_decides_to_set_default_location.return_value = True

        assert app_start_set_default_chart_save_location() is None

        mocked_print.assert_called_once_with(self.welcome_print_stmt)
        mocked_user_decides_to_set_default_location.assert_called_once_with()
        mocked_set_default_chart_save_location.assert_called_once_with(
                user_set=mocked_user_decides_to_set_default_location.return_value)
        mocked_clear_screen.assert_called_once_with()

    @patch('dionysus_app.settings_functions.clear_screen')
    @patch('dionysus_app.settings_functions.set_default_chart_save_location')
    @patch('dionysus_app.settings_functions.user_decides_to_set_default_location')
    @patch('dionysus_app.settings_functions.print')
    def test_app_start_set_default_chart_save_location_app_set(
            self,
            mocked_print,
            mocked_user_decides_to_set_default_location,
            mocked_set_default_chart_save_location,
            mocked_clear_screen,
            ):
        mocked_user_decides_to_set_default_location.return_value = False

        assert app_start_set_default_chart_save_location() is None

        mocked_print.assert_called_once_with(self.welcome_print_stmt)
        mocked_user_decides_to_set_default_location.assert_called_once_with()
        mocked_set_default_chart_save_location.assert_called_once_with(
                user_set=mocked_user_decides_to_set_default_location.return_value)
        mocked_clear_screen.assert_called_once_with()


