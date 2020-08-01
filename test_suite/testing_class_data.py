"""Test data sets for test_class_functions.py"""
from dionysus_app.persistence.database import ClassIdentifier
# Registry
testing_registry_list = ['First class', 'Second class', 'Third class']
testing_registry_enumerated_dict = {1: ClassIdentifier('First class', 'First class'),
                                    2: ClassIdentifier('Second class', 'Second class'),
                                    3: ClassIdentifier('Third class', 'Third class')}

testing_registry_data_set = {'registry_classlist': testing_registry_list,
                             'enumerated_dict': testing_registry_enumerated_dict
                             }


# new data storage formats

# Add attributes to test expected output.
test_class_name_only_name = "The_Knights_of_the_Round-table__we_don_t_say__Ni__"
# Essentially clean_for_filename("The Knights of the Round-table: we don't say 'Ni!'")

test_class_name_only_json_str_rep = ('{\n'
                                     + f'    "name": "{test_class_name_only_name}",\n'
                                     + f'    "students": {[]},\n'
                                     + f'    "id": "{test_class_name_only_name}"\n'
                                     + '}')

test_class_name_only_json_dict_rep = {'name': test_class_name_only_name,
                                      'students': [],
                                      'id': test_class_name_only_name

                                      }

test_class_name_only_data_set = {'name': test_class_name_only_name,
                                 'json_dict_rep': test_class_name_only_json_dict_rep,
                                 'json_str_rep': test_class_name_only_json_str_rep,
                                 # 'enumerated_dict': test_class_data_set_enumerated_dict,
                                 }

# A full class designed to test most/all potential permutations of data.

test_full_class_data_set_json_string = ('{\n'
                                        '    "name": "test_class",\n'
                                        '    "students": [\n'
                                        '        {\n'
                                        '            "name": "Cali",\n'
                                        '            "avatar_id": "Cali_avatar.png"\n'
                                        '        },\n'
                                        '        {\n'
                                        '            "name": "Monty"\n'
                                        '        },\n'
                                        '        {\n'
                                        '            "name": "Abby"\n'
                                        '        },\n'
                                        '        {\n'
                                        '            "name": "Zach",\n'
                                        '            "avatar_id": "Zach_avatar.png"\n'
                                        '        },\n'
                                        '        {\n'
                                        '            "name": "Janell"\n'
                                        '        },\n'
                                        '        {\n'
                                        '            "name": "Matthew"\n'
                                        '        },\n'
                                        '        {\n'
                                        '            "name": "Olivia"\n'
                                        '        },\n'
                                        '        {\n'
                                        '            "name": "Regina"\n'
                                        '        },\n'
                                        '        {\n'
                                        '            "name": "Ashley",\n'
                                        '            "avatar_id": "Ashley_avatar.png"\n'
                                        '        },\n'
                                        '        {\n'
                                        '            "name": "Alex"\n'
                                        '        },\n'
                                        '        {\n'
                                        '            "name": "Melissa"\n'
                                        '        },\n'
                                        '        {\n'
                                        '            "name": "Edgar"\n'
                                        '        },\n        {\n'
                                        '            "name": "Danielle",\n'
                                        '            "avatar_id": "Danielle.png"\n'
                                        '        },\n'
                                        '        {\n'
                                        '            "name": "Kayla"\n'
                                        '        },\n'
                                        '        {\n'
                                        '            "name": "Jaleigh"\n'
                                        '        }\n'
                                        '    ],\n'
                                     + f'    "id": "test_class"\n'
                                        '}'
                                        )

test_full_class_data_set_json_dict = {'name': 'test_class',
                                      'students': [{'name': 'Cali', 'avatar_id': 'Cali_avatar.png'},
                                                   {'name': 'Monty'},
                                                   {'name': 'Abby'},
                                                   {'name': 'Zach', 'avatar_id': 'Zach_avatar.png'},
                                                   {'name': 'Janell'},
                                                   {'name': 'Matthew'},
                                                   {'name': 'Olivia'},
                                                   {'name': 'Regina'},
                                                   {'name': 'Ashley', 'avatar_id': 'Ashley_avatar.png'},
                                                   {'name': 'Alex'},
                                                   {'name': 'Melissa'},
                                                   {'name': 'Edgar'},
                                                   {'name': 'Danielle', 'avatar_id': 'Danielle.png'},
                                                   {'name': 'Kayla'},
                                                   {'name': 'Jaleigh'}],
                                      'id': 'test_class'}

test_full_class_data_set_enumerated_dict = {1: 'Cali',
                                            2: 'Monty',
                                            3: 'Abby',
                                            4: 'Zach',
                                            5: 'Janell',
                                            6: 'Matthew',
                                            7: 'Olivia',
                                            8: 'Regina',
                                            9: 'Ashley',
                                            10: 'Alex',
                                            11: 'Melissa',
                                            12: 'Edgar',
                                            13: 'Danielle',
                                            14: 'Kayla',
                                            15: 'Jaleigh',
                                            }

test_full_class_data_set = {'json_str_rep': test_full_class_data_set_json_string,
                            'json_dict_rep': test_full_class_data_set_json_dict,
                            'enumerated_dict': test_full_class_data_set_enumerated_dict,
                            }

"""Depreciated old style class data sets"""
old_style_testing_class_data_set_json_string = '{\n    "Cali": [\n        "Cali_avatar.png"\n    ],\n    "Monty": ' \
                                     '[\n        null\n    ],\n    "Abby": [\n        null\n    ],' \
                                     '\n    "Zach": [\n        "Zach_avatar.png"\n    ],\n    "Janell": ' \
                                     '[\n        null\n    ],\n    "Matthew": [\n        null\n    ],' \
                                     '\n    "Olivia": [\n        null\n    ],\n    "Regina": [\n        ' \
                                     'null\n    ],\n    "Ashley": [\n        "Ashley_avatar.png"\n    ],' \
                                     '\n    "Alex": [\n        null\n    ],\n    "Melissa": [\n        ' \
                                     'null\n    ],\n    "Edgar": [\n        null\n    ],' \
                                     '\n    "Danielle": [\n        "Danielle.png"\n    ],\n    "Kayla": ' \
                                     '[\n        null\n    ],\n    "Jaleigh": [\n        null\n    ]\n}'

old_style_testing_class_data_set_loaded_dict = {'Cali': ['Cali_avatar.png'], 'Monty': [None], 'Abby': [None],
                                      'Zach': ['Zach_avatar.png'], 'Janell': [None], 'Matthew': [None],
                                      'Olivia': [None], 'Regina': [None], 'Ashley': ['Ashley_avatar.png'],
                                      'Alex': [None], 'Melissa': [None], 'Edgar': [None],
                                      'Danielle': ['Danielle.png'], 'Kayla': [None], 'Jaleigh': [None]
                                      }

old_style_testing_class_data_set_enumerated_dict = {1: 'Cali', 2: 'Monty', 3: 'Abby', 4: 'Zach', 5: 'Janell', 6: 'Matthew',
                                          7: 'Olivia', 8: 'Regina', 9: 'Ashley', 10: 'Alex', 11: 'Melissa', 12: 'Edgar',
                                          13: 'Danielle', 14: 'Kayla', 15: 'Jaleigh',
                                          }

old_style_testing_class_data_set = {
    'json_data_string': old_style_testing_class_data_set_json_string,
    'loaded_dict': old_style_testing_class_data_set_loaded_dict,
    'enumerated_dict': old_style_testing_class_data_set_enumerated_dict,
}

"""
test_display_student_selection_menu_enum_student_output equivalent to:

for key, class_name in testing_class_data_set_enumerated_dict.items():
    test_display_student_selection_menu_student_output.append(f'{key}. {class_name}')
"""
test_display_student_selection_menu_student_output = ['1. Cali', '2. Monty', '3. Abby', '4. Zach', '5. Janell',
                                                      '6. Matthew', '7. Olivia', '8. Regina', '9. Ashley',
                                                      '10. Alex', '11. Melissa', '12. Edgar', '13. Danielle',
                                                      '14. Kayla', '15. Jaleigh', ]