"""Test app_main."""

from unittest import TestCase, mock
from unittest.mock import patch

from app_main import quit_app


class TestQuitApp(TestCase):
    @patch('app_main.sys.exit')
    @patch('app_main.check_registry_on_exit')
    def test_quit_app(self, mock_check_registry_on_exit, mock_exit_call):
        assert quit_app() is None
        mock_check_registry_on_exit.assert_called_once()
        mock_exit_call.assert_called_once()
