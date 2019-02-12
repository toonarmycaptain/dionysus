from unittest import TestCase
from unittest.mock import patch

from dionysus_app.chart_generator.create_chart import get_custom_chart_options

class TestGetCustomChartOptions(TestCase):
    def setUp(self):
        self.test_default_params = {'default param': 'my default param value'}

    @patch('dionysus_app.chart_generator.create_chart.take_custom_chart_options')
    def test_get_custom_chart_options(self, mock_custom_chart_options):

        assert get_custom_chart_options(self.test_default_params) == self.test_default_params

        mock_custom_chart_options.assert_called_once()