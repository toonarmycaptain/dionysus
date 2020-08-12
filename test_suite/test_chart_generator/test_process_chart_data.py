"""Tests for dionysus_app.chart_generator.process_chart_data.py"""
import pytest

from dionysus_app.chart_generator import process_chart_data
from dionysus_app.chart_generator.process_chart_data import (assign_avatars_to_bands,
                                                             assign_avatar_coords,
                                                             generate_avatar_coords,
                                                             )
from dionysus_app.class_ import Class
from dionysus_app.persistence.databases.json import JSONDatabase
from test_suite.test_persistence.test_database import empty_generic_database  # Fixture.
from test_suite.test_persistence.test_databases.test_json import empty_json_database  # Fixture.
from test_suite.test_persistence.test_databases.test_sqlite import empty_sqlite_database  # Fixture.
from test_suite.testing_class_data import test_full_class_data_set

test_score_students_dict = {1: ['foo', 'spam', 'dead', 'parrot'],
                            5: ['halibut', 'patties'],
                            8: ['original', 'recipe', 'chicken'],
                            9: ['foo', 'spam', 'dead', 'parrot'],
                            11: ['halibut', 'patties'],
                            }


class TestAssignAvatarsToBands:
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

        assert assign_avatars_to_bands(test_score_students_dict) == test_assign_avatars_to_bands_result


class TestAssignAvatarCoords:
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
        assert assign_avatar_coords(
            assign_avatars_to_bands(test_score_students_dict)) == test_assign_avatar_coords_result


class TestGenerateAvatarCoords:
    @pytest.mark.parametrize('database_backend', ['empty_generic_database',
                                                  'empty_json_database',
                                                  'empty_sqlite_database',
                                                  ])
    def test_generate_avatar_coords(self, request, monkeypatch,
                                    database_backend):
        test_database = request.getfixturevalue(database_backend)
        test_database.default_avatar_path = 'mocked_default_avatar_path'

        test_class = Class.from_dict(test_full_class_data_set['json_dict_rep'])
        student_score_entry_sequence = [0, 1, 3, None, 50, 99, 100, 1, 2, 3, 4, None, 6, 7, 8]

        # Mock out avatar_paths with readable strings.
        avatar_paths = [f'path to {student.avatar_id}' if student.avatar_id is not None
                        else test_database.default_avatar_path
                        for student in test_class.students]
        # Format those avatar_paths to remove students who did not submit a score:
        mocked_get_avatar_path_return_values = [avatar_paths[student_score_entry_sequence.index(score)]
                                                for score in student_score_entry_sequence
                                                if score is not None]
        avatar_path = (path for path in mocked_get_avatar_path_return_values)

        def mocked_get_avatar_path(avatar_id):
            """
            Strictly speaking does not need a mock, as should raise error, but
            re-mocking method for clarity.
            """
            if isinstance(test_database, JSONDatabase):
                raise NotImplementedError("Alternate method 'get_avatar_path_class_filename' "
                                          "should be called for JSON database.")
            return next(avatar_path)

        def mocked_get_avatar_path_class_filename(class_name, avatar_id):
            if not isinstance(test_database, JSONDatabase):
                raise NotImplementedError("'get_avatar_path_class_filename' "
                                          "only implemented for JSON database.")
            return next(avatar_path)

        test_database.get_avatar_path = mocked_get_avatar_path
        test_database.get_avatar_path_class_filename = mocked_get_avatar_path_class_filename

        monkeypatch.setattr(process_chart_data.definitions, 'DATABASE', test_database)

        test_student_scores_dict = {0: [test_class.students[0]],  # Cali
                                    1: [test_class.students[1],  # Monty
                                        test_class.students[7]],  # Regina
                                    3: [test_class.students[2],  # Abby
                                        test_class.students[9]],  # Alex
                                    # No score, not returned: None: [test_class.students[3],  # Zach
                                    #                                test_class.students[11]],  # Edgar
                                    50: [test_class.students[4]],  # Janell
                                    99: [test_class.students[5]],  # Matthew
                                    100: [test_class.students[6]],  # Olivia
                                    2: [test_class.students[8]],  # Ashley
                                    4: [test_class.students[10]],  # Melissa
                                    6: [test_class.students[12]],  # Danielle
                                    7: [test_class.students[13]],  # Kayla
                                    8: [test_class.students[14]],  # Jaleigh
                                    }

        test_generate_avatar_coords_result = {'mocked_default_avatar_path': [(0.0, 15),
                                                                             (0.0, 25),
                                                                             (0.0, 35),
                                                                             (0.0, 45),
                                                                             (0.0, 55),
                                                                             (0.0, 65),
                                                                             (10.0, 15),
                                                                             (10.0, 25),
                                                                             (50.0, 5),
                                                                             (100.0, 5)],
                                              'path to Ashley_avatar.png': [(100.0, 15)],
                                              'path to Cali_avatar.png': [(0.0, 5)],
                                              'path to Danielle.png': [(10.0, 5)]
                                              }

        assert generate_avatar_coords(test_student_scores_dict, test_class.id) == test_generate_avatar_coords_result
