"""Test app_main."""
import sys

import pytest

import app_main

from app_main import quit_app, run_app

from test_suite.test_persistence.test_database import empty_generic_database  # Fixture


class TestQuitApp:
    def test_quit_app(self, monkeypatch, empty_generic_database):
        clear_temp_mock, DATABASE_close_mock, exit_mock = {'called': False}, {'called': False}, {'called': False}

        def mocked_clear_temp():
            clear_temp_mock['called'] = True

        def mocked_DATABASE_close():
            DATABASE_close_mock['called'] = True

        def mocked_sys_exit():
            exit_mock['called'] = True

        mocked_DATABASE = empty_generic_database
        mocked_DATABASE.close = mocked_DATABASE_close

        monkeypatch.setattr(app_main, 'clear_temp', mocked_clear_temp)
        monkeypatch.setattr(app_main.definitions, 'DATABASE', mocked_DATABASE)
        monkeypatch.setattr(app_main.sys, 'exit', mocked_sys_exit)
        with pytest.raises(SystemExit):
            assert quit_app() is 0
            assert all([DATABASE_close_mock['called'], exit_mock['called'], clear_temp_mock['called']])


class TestRunApp:
    def test_run_app_sets_cwd_correctly(self, monkeypatch):
        os_chdir_mock, app_init_mock = {'called': False}, {'called': False}
        load_chart_save_folder_mock, load_database_mock = {'called': False}, {'called': False}
        run_main_menu_mock, quit_app_mock = {'called': False}, {'called': False}

        def mocked_os_chdir(path):
            if path is not sys.path[0]:
                raise ValueError('run_app did not change cwd to dir containing app_main.')
            os_chdir_mock['called'] = True

        def mocked_app_init():
            app_init_mock['called'] = True

        def mocked_load_chart_save_folder():
            load_chart_save_folder_mock['called'] = True

        def mocked_load_database():
            load_database_mock['called'] = True

        def mocked_run_main_menu():
            run_main_menu_mock['called'] = True

        def mocked_quit_app():
            quit_app_mock['called'] = True

        monkeypatch.setattr(app_main.os, 'chdir', mocked_os_chdir)
        monkeypatch.setattr(app_main, 'app_init', mocked_app_init)
        monkeypatch.setattr(app_main, 'load_chart_save_folder', mocked_load_chart_save_folder)
        monkeypatch.setattr(app_main, 'load_database', mocked_load_database)
        monkeypatch.setattr(app_main, 'run_main_menu', mocked_run_main_menu)
        monkeypatch.setattr(app_main, 'quit_app', mocked_quit_app)

        assert run_app() is None

        assert all([os_chdir_mock['called'],
                    app_init_mock['called'],
                    load_chart_save_folder_mock['called'],
                    load_database_mock['called'],
                    run_main_menu_mock['called'],
                    quit_app_mock['called']
                    ])
