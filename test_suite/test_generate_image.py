import os

from unittest import TestCase

from dionysus_app.chart_generator.generate_image import validate_avatar
from dionysus_app.chart_generator.generate_image import DEFAULT_AVATAR_PATH


class TestValidateAvatar(TestCase):
    def setUp(self):
        self.good_path = 'just_sleeping.png'
        with open(self.good_path, 'w+') as good_file:
                        pass

    def test_load_existent_image(self):
        assert validate_avatar(self.good_path) == self.good_path

    def test_load_nonexistent_image(self):
        assert validate_avatar('definitely_dead.png') == DEFAULT_AVATAR_PATH

    def tearDown(self):
        os.remove(self.good_path)
