from dionysus_app.file_functions import convert_to_json


class TestConvertToJson:
    def test_convert_to_json(self):
        data_to_convert = {1: 'a', 'b': 2, 3: 'c', 'd': 4}
        json_converted_data = '{\n    "1": "a",\n    "b": 2,\n    "3": "c",\n    "d": 4\n}'

        assert convert_to_json(data_to_convert) == json_converted_data
