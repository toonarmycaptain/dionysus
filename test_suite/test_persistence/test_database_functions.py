import pytest

from unittest.mock import MagicMock, patch

from dionysus_app.persistence import database_functions
from dionysus_app.persistence.database_functions import load_database


class TestLoadDatabase:
    @pytest.mark.parametrize(
        'mock_default_database_setting, mock_database_backends',
        [('test_database', {'test_database': str}),  # str() used as throwaway func to return.
         pytest.param('what database?', {'not found': 'not a database object'}, marks=pytest.mark.xfail),
         ])
    def test_load_database(self, monkeypatch,
                           mock_default_database_setting, mock_database_backends):

        monkeypatch.setattr(database_functions, 'database_backends', mock_database_backends)
        # Mock out app_data/settings where it doesn't exist -> dir/package will not exist in testing.
        mocked_settings = MagicMock()
        mocked_settings.dionysus_settings = {'database': mock_default_database_setting}
        with patch.dict('sys.modules', {'dionysus_app.app_data.settings': mocked_settings}):
            assert load_database() == mock_database_backends['test_database']()


