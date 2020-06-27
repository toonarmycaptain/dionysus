from pathlib import Path

import pytest

from dionysus_app.chart_generator import generate_image
from dionysus_app.chart_generator.generate_image import (add_avatar_to_plot,
                                                         add_avatars_to_plot,
                                                         generate_chart_image,
                                                         set_axis,
                                                         validate_avatar,
                                                         )
from test_suite.test_persistence.test_database import empty_generic_database  # Fixture.


class TestGenerateChartImage:
    def test_generate_chart_image(self, monkeypatch, empty_generic_database):
        called = {'set_axis_mock': False,
                  'generate_avatar_coords_mock': False,
                  'add_avatars_to_plot_mock': False,
                  'save_chart_image_mock': False
                  }

        test_database = empty_generic_database

        def mocked_save_chart_image(chart_data_dict, plt):
            assert (chart_data_dict, plt) == (test_chart_data_dict, mocked_plt)
            called['save_chart_image_mock'] = True
            return test_image_location

        test_database.save_chart_image = mocked_save_chart_image

        class MockPlt:
            def __init__(self):
                self.calls_to_mock_plt = {'figure': False,
                                          'subplot': False,
                                          'subplots_adjust': False}
                self.calls_to_mock_ax = {'grid': False}
                self.mock_ax = self.MockAx(self.calls_to_mock_ax)

            class MockAx:
                def __init__(self, calls_to_mock_ax):
                    self.calls_to_mock_ax = calls_to_mock_ax

                def grid(self, arg):
                    assert arg is False
                    self.calls_to_mock_ax['grid'] = True

            def figure(self, figsize):
                assert figsize == (16, 9)
                self.calls_to_mock_plt['figure'] = True

            def subplot(self, xlim, ylim):
                assert xlim, ylim == ((-0, 105), (-0, 100))
                self.calls_to_mock_plt['subplot'] = True
                return self.mock_ax

            def subplots_adjust(self, left, right, top, bottom, wspace, hspace):
                assert (left, right, top, bottom, wspace, hspace) == (0.05, 0.95, 0.9, 0.1, 0.01, 0.01)
                self.calls_to_mock_plt['subplots_adjust'] = True

        def mocked_set_axis():
            called['set_axis_mock'] = True

        def mocked_generate_avatar_coords(score_avatar_dict):
            assert score_avatar_dict == test_chart_data_dict['score-avatar_dict']
            called['generate_avatar_coords_mock'] = True
            return test_avatar_coord_dict

        def mocked_add_avatars_to_plot(ax, avatar_coord_dict):
            assert (ax, avatar_coord_dict) == (mocked_plt.mock_ax, test_avatar_coord_dict)
            called['add_avatars_to_plot_mock'] = True

        mocked_plt = MockPlt()

        monkeypatch.setattr(generate_image.definitions, 'DATABASE', test_database)
        monkeypatch.setattr(generate_image, 'plt', mocked_plt)
        monkeypatch.setattr(generate_image, 'set_axis', mocked_set_axis)
        monkeypatch.setattr(generate_image, 'generate_avatar_coords', mocked_generate_avatar_coords)
        monkeypatch.setattr(generate_image, 'add_avatars_to_plot', mocked_add_avatars_to_plot)

        test_chart_data_dict = {'score-avatar_dict': {1: ['foo', 'spam', 'dead', 'parrot'],
                                                      5: ['halibut', 'patties'],
                                                      8: ['original', 'recipe', 'chicken'],
                                                      9: ['foo', 'spam', 'dead', 'parrot'],
                                                      11: ['halibut', 'patties'],
                                                      }
                                }
        test_avatar_coord_dict = {'avatar_coord': 'dict'}
        test_image_location = 'some image location'

        assert generate_chart_image(test_chart_data_dict) == test_image_location

        assert all([called[func] for func in called])
        assert all([mocked_plt.calls_to_mock_plt[func] for func in mocked_plt.calls_to_mock_plt])
        assert all([mocked_plt.calls_to_mock_ax[func] for func in mocked_plt.calls_to_mock_ax])


class TestSetAxis:
    @pytest.mark.parametrize(
        'test_x_min, test_x_max, test_x_step, xticks_arg',
        [(0, 100, 10, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]),  # Defaults.
         (7, 343, 49, [7, 56, 105, 154, 203, 252, 301]),
         ])
    def test_set_axis(self, monkeypatch,
                      test_x_min, test_x_max, test_x_step, xticks_arg):
        test_xticks = [tick for tick in range(test_x_min, test_x_max + 1, test_x_step)]
        test_yticks = []

        class MockPlt:
            def __init__(self):
                self.calls_to_mock_plt = {'xticks': False,
                                          'yticks': False,
                                          }

            def xticks(self, arg):
                assert arg == test_xticks
                self.calls_to_mock_plt['xticks'] = True

            def yticks(self, arg):
                assert arg == test_yticks
                self.calls_to_mock_plt['yticks'] = True

        mocked_plt = MockPlt()

        monkeypatch.setattr(generate_image, 'plt', mocked_plt)

        assert set_axis(test_x_min, test_x_max, test_x_step) is None
        assert all([mocked_plt.calls_to_mock_plt[func] for func in mocked_plt.calls_to_mock_plt])


class TestAddAvatarToPlot:
    def test_add_avatar_to_plot(self, monkeypatch):
        called = {'mocked_validate_avatar': False}

        def mocked_validate_avatar(avatar_path):
            assert avatar_path is test_avatar_path
            called['mocked_validate_avatar'] = True
            return test_avatar_path

        class MockPlt:
            def __init__(self):
                self.calls_to_mock_plt = {'imread': False,
                                          'draw': False
                                          }

            def imread(self, arg):
                assert arg == str(test_avatar_path)
                self.calls_to_mock_plt['imread'] = True
                return test_avatar_image

            def draw(self):
                self.calls_to_mock_plt['draw'] = True

        class MockOffsetImage:
            def __init__(self, avatar_image, zoom):
                assert avatar_image == test_avatar_image
                self.avatar_image = avatar_image
                assert zoom == .4
                self.zoom = zoom

        class MockAx:
            def __init__(self):
                self.calls_to_mock_ax = {'add_artist': False}
                self.abs = []

            def add_artist(self, ab):
                assert ab.xy in test_xy_coords
                self.calls_to_mock_ax['add_artist'] = True
                self.abs.append(ab)

        class MockAnnotationBbox:
            def __init__(self, imagebox, xy):
                assert imagebox.avatar_image == test_avatar_image
                assert imagebox.zoom == .4
                self.imagebox = imagebox
                assert xy in test_xy_coords
                self.xy = xy

        test_ax = MockAx()
        test_avatar_path = Path('some/path')
        test_xy_coords = [(0, 10), (3, 50), (6, 99)]
        mocked_plt = MockPlt()
        test_avatar_image = 'avatar_image'

        monkeypatch.setattr(generate_image, 'validate_avatar', mocked_validate_avatar)
        monkeypatch.setattr(generate_image, 'plt', mocked_plt)
        monkeypatch.setattr(generate_image, 'OffsetImage', MockOffsetImage)
        monkeypatch.setattr(generate_image, 'AnnotationBbox', MockAnnotationBbox)

        assert add_avatar_to_plot(test_ax, test_avatar_path, test_xy_coords) is None

        assert [image.xy for image in test_ax.abs] == test_xy_coords

        assert all([called[func] for func in called])
        assert all([mocked_plt.calls_to_mock_plt[func] for func in mocked_plt.calls_to_mock_plt])
        assert all([test_ax.calls_to_mock_ax[func] for func in test_ax.calls_to_mock_ax])


class TestValidateAvatar:
    @pytest.mark.parametrize('avatar_path_exists', [True, False])
    def test_validate_avatar(self, monkeypatch, empty_generic_database,
                             avatar_path_exists):
        """Returns valid avatar path, else db.default_avatar_path."""
        test_database = empty_generic_database
        test_database.default_avatar_path = 'path to a default avatar'

        test_avatar_path = Path('Camelot, a silly place.')

        monkeypatch.setattr(generate_image, 'avatar_file_exists', lambda avatar_path: avatar_path_exists)
        monkeypatch.setattr(generate_image.definitions, 'DATABASE', test_database)

        assert validate_avatar(test_avatar_path) == (test_avatar_path if avatar_path_exists
                                                     else test_database.default_avatar_path)


class TestAddAvatarsToPlot:
    def test_add_avatars_to_plot(self, monkeypatch):
        test_ax = 'ax'
        test_avatar_coord_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}
        called_args = {}

        def mocked_add_avatar_to_plot(ax, avatar_path, xy_coords):
            assert ax == test_ax
            assert test_avatar_coord_dict[avatar_path] == xy_coords  # coorect args.
            called_args[avatar_path] = xy_coords

        monkeypatch.setattr(generate_image, 'add_avatar_to_plot', mocked_add_avatar_to_plot)

        assert add_avatars_to_plot(test_ax, test_avatar_coord_dict) is None
        assert called_args == test_avatar_coord_dict
