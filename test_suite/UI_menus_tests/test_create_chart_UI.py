"""Test create_chart_UI"""

from pathlib import Path

from dionysus_app.UI_menus.chart_generator import create_chart_UI
from dionysus_app.UI_menus.chart_generator.create_chart_UI import (save_chart_dialogue,
                                                                   )


class TestSaveChartDialogue:
    def test_save_chart_dialogue(self, monkeypatch):
        test_user_selected_path = Path('my_save_chart_path')
        test_default_chart_name = 'test_chart_name'
        test_class_save_folder_path = Path('test_path')

        def mocked_save_as_dialogue(title_str, filetypes, suggested_filename, start_dir):
            assert title_str == 'Save chart image as:'
            assert filetypes == [('.png', '*.png'), ("all files", "*.*")]
            assert suggested_filename == test_default_chart_name
            assert start_dir == str(test_class_save_folder_path)
            return test_user_selected_path

        monkeypatch.setattr(create_chart_UI, 'save_as_dialogue', mocked_save_as_dialogue)

        assert save_chart_dialogue(test_default_chart_name,
                                   test_class_save_folder_path
                                   ) == test_user_selected_path
