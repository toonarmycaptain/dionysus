"""Test create_chart_UI"""

from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from dionysus_app.UI_menus.chart_generator.create_chart_UI import (save_chart_dialogue,
                                                                   )


class TestSaveChartDialogue(TestCase):
    def setUp(self):
        self.test_default_chart_name = 'test_chart_name'
        self.test_class_save_folder_path_str = 'test_path'
        self.test_class_save_folder_path = Path(self.test_class_save_folder_path_str)

        self.test_user_selected_path_str = 'my_save_chart_path'

    @patch('dionysus_app.UI_menus.chart_generator.create_chart_UI.save_as_dialogue')
    def test_save_chart_dialogue_str_path(self, mocked_save_as_dialogue):
        mocked_save_as_dialogue.return_value = self.test_user_selected_path_str

        assert save_chart_dialogue(self.test_default_chart_name,
                                   self.test_class_save_folder_path_str
                                   ) == self.test_user_selected_path_str

        mocked_save_as_dialogue.assert_called_once_with(title_str='Save chart image as:',
                                                        filetypes=[('.png', '*.png'), ("all files", "*.*")],
                                                        suggested_filename=self.test_default_chart_name,
                                                        start_dir=self.test_class_save_folder_path_str
                                                        )

    @patch('dionysus_app.UI_menus.chart_generator.create_chart_UI.save_as_dialogue')
    def test_save_chart_dialogue_path_path(self, mocked_save_as_dialogue):
        mocked_save_as_dialogue.return_value = self.test_user_selected_path_str

        assert save_chart_dialogue(self.test_default_chart_name,
                                   self.test_class_save_folder_path
                                   ) == self.test_user_selected_path_str

        mocked_save_as_dialogue.assert_called_once_with(title_str='Save chart image as:',
                                                        filetypes=[('.png', '*.png'), ("all files", "*.*")],
                                                        suggested_filename=self.test_default_chart_name,
                                                        start_dir=self.test_class_save_folder_path_str
                                                        )
