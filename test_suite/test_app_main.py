"""Test app_main."""
import sys

import app_main

from app_main import quit_app, run_app


class TestQuitApp:
    def test_quit_app(self, monkeypatch):
        check_registry_on_exit_mock, exit_mock = {'called': False}, {'called': False}

        def mocked_check_registry_on_exit():
            check_registry_on_exit_mock['called'] = True

        def mocked_sys_exit():
            exit_mock['called'] = True

        monkeypatch.setattr(app_main, 'check_registry_on_exit', mocked_check_registry_on_exit)
        monkeypatch.setattr(app_main.sys, 'exit', mocked_sys_exit)

        assert quit_app() is None
        assert exit_mock['called'] and check_registry_on_exit_mock['called']


class TestRunApp:
    def test_run_app_sets_cwd_correctly(self, monkeypatch):
        os_chdir_mock, app_init_mock = {'called': False}, {'called': False}
        cache_class_registry_mock, load_chart_save_folder_mock = {'called': False}, {'called': False}
        run_main_menu_mock, quit_app_mock = {'called': False}, {'called': False}

        def mocked_os_chdir(path):
            if path is not sys.path[0]:
                raise ValueError('run_app did not change cwd to dir containing app_main.')
            os_chdir_mock['called'] = True

        def mocked_app_init():
            app_init_mock['called'] = True

        def mocked_cache_class_registry():
            cache_class_registry_mock['called'] = True

        def mocked_load_chart_save_folder():
            load_chart_save_folder_mock['called'] = True

        def mocked_run_main_menu():
            run_main_menu_mock['called'] = True

        def mocked_quit_app():
            quit_app_mock['called'] = True

        monkeypatch.setattr(app_main.os, 'chdir', mocked_os_chdir)
        monkeypatch.setattr(app_main, 'app_init', mocked_app_init)
        monkeypatch.setattr(app_main, 'cache_class_registry', mocked_cache_class_registry)
        monkeypatch.setattr(app_main, 'load_chart_save_folder', mocked_load_chart_save_folder)
        monkeypatch.setattr(app_main, 'run_main_menu', mocked_run_main_menu)
        monkeypatch.setattr(app_main, 'quit_app', mocked_quit_app)

        assert run_app() is None

        assert all([os_chdir_mock['called'], app_init_mock['called'], cache_class_registry_mock['called'],
                    load_chart_save_folder_mock['called'], run_main_menu_mock['called'], quit_app_mock['called']])
