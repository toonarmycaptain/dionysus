"""Tests for dionysus_app.chart_generator.process_chart_data.py"""
from unittest import TestCase
from dionysus_app.chart_generator.process_chart_data import assign_avatars_to_bands, assign_avatar_coords, generate_avatar_coords


class TestProcessChartData(TestCase):
    def setUp(self):
        self.test_score_avatar_dict = {1: ['foo', 'spam', 'dead', 'parrot'],
                                       5: ['halibut', 'patties'],
                                       8: ['original', 'recipe', 'chicken'],
                                       9: ['foo', 'spam', 'dead', 'parrot'],
                                       11: ['halibut', 'patties'],
                                       }

    def test_assign_avatars_to_bands(self):
        test_assign_avatars_to_bands_result = {0: ['foo', 'spam', 'dead', 'parrot', 'halibut', 'patties'],
                                               10: ['original', 'recipe', 'chicken', 'foo', 'spam', 'dead',
                                                    'parrot', 'halibut', 'patties'],
                                               20: [],
                                               30: [],
                                               40: [],
                                               50: [],
                                               60: [],
                                               70: [],
                                               80: [],
                                               90: [],
                                               100: [],
                                               }

        assert assign_avatars_to_bands(self.test_score_avatar_dict) == test_assign_avatars_to_bands_result

    def test_assign_avatar_coords(self):
        test_assign_avatar_coords_result = {'foo': [(0.0, 5), (10.0, 35)],
                                            'spam': [(0.0, 15), (10.0, 45)],
                                            'dead': [(0.0, 25), (10.0, 55)],
                                            'parrot': [(0.0, 35), (10.0, 65)],
                                            'halibut': [(0.0, 45), (10.0, 75)],
                                            'patties': [(0.0, 55), (10.0, 85)],
                                            'original': [(10.0, 5)],
                                            'recipe': [(10.0, 15)],
                                            'chicken': [(10.0, 25)]
                                            }
        assert assign_avatar_coords(assign_avatars_to_bands(self.test_score_avatar_dict)) == test_assign_avatar_coords_result

    def test_generate_avatar_coords(self):
        test_generate_avatar_coords_result = {'foo': [(0.0, 5), (10.0, 35)],
                                              'spam': [(0.0, 15), (10.0, 45)],
                                              'dead': [(0.0, 25), (10.0, 55)],
                                              'parrot': [(0.0, 35), (10.0, 65)],
                                              'halibut': [(0.0, 45), (10.0, 75)],
                                              'patties': [(0.0, 55), (10.0, 85)],
                                              'original': [(10.0, 5)],
                                              'recipe': [(10.0, 15)],
                                              'chicken': [(10.0, 25)],
                                              }

        assert generate_avatar_coords(self.test_score_avatar_dict) == test_generate_avatar_coords_result
