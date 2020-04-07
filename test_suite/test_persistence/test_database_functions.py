import pytest

from dionysus_app.app_data import settings
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
        # Monkeypatch database setting in settings, since it is imported within the function.
        monkeypatch.setattr(settings, 'dionysus_settings', {'database': mock_default_database_setting})
        monkeypatch.setattr(database_functions, 'database_backends', mock_database_backends)

        assert load_database() == mock_database_backends['test_database']()
