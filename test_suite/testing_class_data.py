"""Test data sets for test_class_functions.py"""

testing_class_data_set_json_string = '{\n    "Cali": [\n        "Cali_avatar.png"\n    ],\n    "Monty": ' \
                                     '[\n        null\n    ],\n    "Abby": [\n        null\n    ],' \
                                     '\n    "Zach": [\n        "Zach_avatar.png"\n    ],\n    "Janell": ' \
                                     '[\n        null\n    ],\n    "Matthew": [\n        null\n    ],' \
                                     '\n    "Olivia": [\n        null\n    ],\n    "Regina": [\n        ' \
                                     'null\n    ],\n    "Ashley": [\n        "Ashley_avatar.png"\n    ],' \
                                     '\n    "Alex": [\n        null\n    ],\n    "Melissa": [\n        ' \
                                     'null\n    ],\n    "Edgar": [\n        null\n    ],' \
                                     '\n    "Danielle": [\n        "Danielle.png"\n    ],\n    "Kayla": ' \
                                     '[\n        null\n    ],\n    "Jaleigh": [\n        null\n    ]\n}'

testing_class_data_set_loaded_dict = {'Cali': ['Cali_avatar.png'], 'Monty': [None], 'Abby': [None],
                                      'Zach': ['Zach_avatar.png'], 'Janell': [None], 'Matthew': [None],
                                      'Olivia': [None], 'Regina': [None], 'Ashley': ['Ashley_avatar.png'],
                                      'Alex': [None], 'Melissa': [None], 'Edgar': [None],
                                      'Danielle': ['Danielle.png'], 'Kayla': [None], 'Jaleigh': [None]
                                      }

testing_class_data_set_enumerated_dict = {1: 'Cali', 2: 'Monty', 3: 'Abby', 4: 'Zach', 5: 'Janell', 6: 'Matthew',
                                          7: 'Olivia', 8: 'Regina', 9: 'Ashley', 10: 'Alex', 11: 'Melissa', 12: 'Edgar',
                                          13: 'Danielle', 14: 'Kayla', 15: 'Jaleigh'
                                          }

testing_class_data_set = {
    'json_data_string': testing_class_data_set_json_string,
    'loaded_dict': testing_class_data_set_loaded_dict,
    'enumerated_dict': testing_class_data_set_enumerated_dict,
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

# Registry
testing_registry_list = ['First class', 'Second class', 'Third class']
testing_registry_enumerated_dict = {1: 'First class', 2: 'Second class', 3: 'Third class'}

testing_registry_data_set = {'registry_classlist': testing_registry_list,
                             'enumerated_dict': testing_registry_enumerated_dict
                             }

"""
test_display_student_selection_menu_output equivalent to:

for key, class_name in testing_registry_enumerated_dict.items():
    test_display_class_selection_menu_output.append(f'{key}. {class_name}')
"""
test_display_class_selection_menu_output = ['1. First class', '2. Second class', '3. Third class']
