"""Test app_main."""
import os

from unittest import TestCase
from unittest.mock import patch

from app_main import quit_app, run_app


class TestQuitApp(TestCase):
    @patch('app_main.sys.exit')
    @patch('app_main.check_registry_on_exit')
    def test_quit_app(self, mock_check_registry_on_exit, mock_exit_call):
        assert quit_app() is None
        mock_check_registry_on_exit.assert_called_once()
        mock_exit_call.assert_called_once()


class TestRunApp(TestCase):
    def setUp(self):
        self.initial_cwd = os.getcwd()  # For resetting after tests.
        self.app_main_cwd = os.path.abspath('.//')  # Current location of app_main.

    @patch('app_main.app_init')
    @patch('app_main.cache_class_registry')
    @patch('app_main.load_chart_save_folder')
    @patch('app_main.run_main_menu')
    @patch('app_main.quit_app')
    def test_run_app_sets_cwd_correctly(self,
                                        mocked_app_init,
                                        mocked_cache_class_registry,
                                        mocked_load_chart_save_folder,
                                        mocked_run_main_menu,
                                        mocked_quit_app,
                                        ):
        """
        Check that run_app sets cwd to location of app_main.
        At present this is the folder above test_suite where
        test_app_main.py is located, hence testing against '..//'.
        """

        assert run_app() is None

        assert os.getcwd() == self.app_main_cwd  # Ensure run_app changed cwd to location of app_main.

        mocked_app_init.assert_called_once_with()
        mocked_cache_class_registry.assert_called_once_with()
        mocked_load_chart_save_folder.assert_called_once_with()
        mocked_run_main_menu.assert_called_once_with()
        mocked_quit_app.assert_called_once_with()

    def tearDown(self):
        os.chdir(self.initial_cwd)  # Reset cwd if changed by tests.
