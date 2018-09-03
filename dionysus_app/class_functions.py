import os

def create_classlist():


    classlist_name = input('Please enter a name for the class: ')
    classlist_name = classlist_name.replace(' ', '_')
    while os.path.exists(classlist_name + '.cld'):  # TODO: Make path point at data folder. .cll meaning. classlist
        print('A class with this name already exists.')
        input('Please try another class name: ')

    with open(classlist_name + '.cld', 'w+') as classlist_file:  # TODO: Make path point at data folder.
        while True:
            student_name = input("Enter student name, or 'end': ")
            if False: # TODO search for it in class - if it exists, ask for more input
                print("This student is already a member of the class.")
                continue
            elif student_name.upper() =='END':
                break
            else:
                classlist_file.write(student_name+'\n')



if __name__ == '__main__'
    create_classlist()
    # same for edit classlist except for with open(classlist_name + '.txt', 'r+') as classlist_file:
