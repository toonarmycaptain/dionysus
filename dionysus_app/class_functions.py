import os

CLASSLIST_PATH = 'dionysus_app/app_data/class_data/'

def create_classlist():

    classlist_name = take_classlist_name_input()

    with open(CLASSLIST_PATH + classlist_name + '.cld', 'w+') as classlist_file:
        student_names = ''
        while True:
            student_name = input("Enter student name, or 'end': ")
            if student_name.join(student_name.split()) == '':  # Do not allow blank input TODO: include dash, underscore
                print('Please enter a valid student name.')
                continue
            if student_name in student_names: # TODO search for it in class - if it exists, ask for more input
                print("This student is already a member of the class.")
                continue
            elif student_name.upper() =='END':
                break
            else:
                student_names += (student_name+'\n')
        print(f'\nClass: {classlist_name}')
        print(student_names)
        classlist_file.write(student_names)


def take_classlist_name_input():

    while True:
        classlist_name = input('Please enter a name for the class: ')
        classlist_name = classlist_name.replace(' ', '_')

        if classlist_name == '':  # blank input
            continue

        if classlist_exists(classlist_name):
            print('A class with this name already exists.')
            continue
        break
    return classlist_name




def classlist_exists(classlist_name):
    if os.path.exists(CLASSLIST_PATH + classlist_name + '.cld'):  # TODO: Make path point at data folder. .cld meaning. ClassListData
        return True




if __name__ == '__main__':
    create_classlist()
    # same for edit classlist except for with open(classlist_name + '.txt', 'r+') as classlist_file:
