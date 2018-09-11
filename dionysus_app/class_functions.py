import os
import re

CLASSLIST_PATH = 'dionysus_app/app_data/class_data/'


def create_classlist():

    classlist_name = take_classlist_name_input()

    setup_class(classlist_name)

    create_classlist_data(classlist_name)


def create_classlist_data(classlist_name):
    with open(CLASSLIST_PATH + classlist_name + '.cld', 'w+') as classlist_file:
        class_data = ''
        while True:
            student_name = take_student_name_input(class_data)
            if student_name.upper() == 'END':
                break

            avatar_filename = take_student_avatar(student_name)
            # else:
            class_data += f'{student_name}, {avatar_filename}\n'  # consider using JSON? dictionaries?

        print(f'\nClass: {classlist_name}')
        print(class_data)
        classlist_file.write(class_data)  # consider using JSON?

        # test for empty classlist - delete/don't create files if list is empty?
        # if list is empty - warn list is empty before saving.


def take_student_name_input(class_data):
    while True:
        student_name = input("Enter student name, or 'end': ")
        if input_is_essentially_blank(student_name):  # Do not allow blank input TODO: include dash, underscore
            print('Please enter a valid student name.')
            continue

        if student_name in class_data:  # TODO: search for it in class - if it exists, ask for more input
            print("This student is already a member of the class.")
            continue
        return student_name


def take_student_avatar(student_name):
    while True:
        avatar_file = input(r'Please paste complete filepath and name eg C:\my_folder\my_avatar.jpg')
        if avatar_file_exists(avatar_file):
            break
        # else:
    cleaned_student_name = clean_for_filename(student_name)
    avatar_filename = f'{cleaned_student_name}.jpg'
    # process_student_avatar()
    # convert to jpg or whatever, copy image file to class_data avatar folder with filename that is student name
    return avatar_filename


def input_is_essentially_blank(questionable_string):
    if questionable_string == '':  # Why bother regex for the obvious
        return True
    meaningless_characters = r'/|\|#|_|{|}|[|]|(|)| |,'

    questionable_string = questionable_string.replace('.', '')  # because period matches while string
    cleaned_string = re.sub(meaningless_characters, '', questionable_string)  # TODO: currently errors
    return cleaned_string == ''


def clean_for_filename(some_string):
    cleaner_filename = scrub_candidate_filename(some_string)
    cleaned_filename = cleaner_filename.replace(' ', '_')  # no slashes either
    return cleaned_filename


def scrub_candidate_filename(dirty_string):
    characters_to_scrub = r'/|\|#|?|{|}|'  # need to include *,[,],|,(,) ? these cause regex problems
    cleaner_string = re.sub(characters_to_scrub, '', dirty_string)  # TODO: currently errors
    clean_string = cleaner_string.replace('|', '')
    return clean_string


def setup_class(classlist_name):  # TODO: change name because of class with python 'class' keyword?
    os.makedirs(f'{CLASSLIST_PATH}{classlist_name}_avatars')


def avatar_file_exists(avatar_file):
    if os.path.exists(avatar_file):
        return True


# TODO: reorder/rearrange functions


def take_classlist_name_input():

    while True:
        classlist_name = input('Please enter a name for the class: ')

        if input_is_essentially_blank(classlist_name):  # blank input
            continue

        classlist_name = clean_for_filename(classlist_name)
        if classlist_exists(classlist_name):
            print('A class with this name already exists.')
            continue
        break
    return classlist_name


def classlist_exists(classlist_name):
    if os.path.exists(CLASSLIST_PATH + classlist_name + '.cld'):
        return True  # TODO: Make path point at data folder. .cld meaning. ClassListData


if __name__ == '__main__':
    create_classlist()
    # same for edit classlist except for with open(classlist_name + '.txt', 'r+') as classlist_file:
