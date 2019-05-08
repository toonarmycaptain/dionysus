import argparse
import json
import sys
import time

from pathlib import Path

from dionysus_app.class_ import Class
from dionysus_app.class_functions import write_classlist_to_file
from dionysus_app.data_folder import DataFolder
from dionysus_app.file_functions import load_from_json_file
from dionysus_app.student import Student
from dionysus_app.UI_menus.UI_functions import select_file_dialogue

CLASSLIST_DATA_PATH = DataFolder.generate_rel_path(DataFolder.CLASS_DATA.value)


def main():
    """
    Process arguments, run script based on args.

    :return: None
    """
    run_args = parse_args(sys.argv[1:])

    run_script(run_args)


def parse_args(args: list):
    """
    Takes list of args passed to script.

    :param args: list
    :return: argparse.Namespace
    """
    parser = argparse.ArgumentParser(description='Transform old data to new format.')
    mutex_group = parser.add_mutually_exclusive_group()
    mutex_group.add_argument('--filepath',
                             '--f', type=str, help='Input single file')
    mutex_group.add_argument('--all_class_data_files',
                             '-A', action="store_true",
                             help='Attempts to transform all .cld files in class_data.')

    return parser.parse_args(args)


def run_script(args: argparse.Namespace):
    """
    Use args passed to script to execute chosen mode.
    No args: run GUI to select and process single file.
    -A/--all_class_data_files: Process all the data files in class_data.
    --f/--filepath: Process single file at path given to arg.
                    Usage: --f=path_to_file

    NB if --f/--filepath= is passed without a filename, but with the = sign,
    the resulting string in args.filepath is '' and is False, spawning the GUI
    dialogue branch.

    :param args: argparse.Namespace
    :return: None
    """
    print(f'args={args}')
    print(f'args.filepath={args.filepath}')
    if args.all_class_data_files:
        transform_all_old_data_files()

    elif args.filepath:
        transform_old_cld_file(Path(args.filepath))

    else:
        file_from_gui_dialogue()


def transform_all_old_data_files():
    """
    Transform data files matching old format to new format.

    :return: None
    """
    for old_class_data_file in CLASSLIST_DATA_PATH.glob('**/*.cld'):
        transform_old_cld_file(Path(old_class_data_file))

    # NB can add operation to call on chart data files too if this is desired.


def transform_old_cld_file(filepath: Path):
    """
    Transform .cld file to new format.

    NB If file is in the wrong location, or not in class data at all, a folder
    with the class name will be created in class_data.

    :param filepath: Path
    :return: None
    """
    if not filepath.exists():
        print(f'File {filepath} does not exist.')
        return

    try:
        old_class_data = load_from_json_file(filepath)
    # Handle corrupt or mal-formatted JSON files.
    except json.decoder.JSONDecodeError:
        print(f'Something went wrong with decoding {filepath}:\n'
              f'The file might be corrupted or is not a supported format.')
        return

    if data_is_new_format(old_class_data):
        print(f'It looks like {filepath.name} is already in the new format.')
        return

    class_name = filepath.stem
    new_class = transform_data(class_name, old_class_data)

    new_class_data_path_name = write_classlist_to_file(new_class)

    print(f'Transformed {new_class.name} data file to new data format in {new_class_data_path_name}')


def data_is_new_format(old_class_data: dict):
    """
    Test if json dict data is in current format to avoid mangling good data.

    :param old_class_data: dict
    :return: Bool
    """
    if 'students' in old_class_data.keys() and 'name' in old_class_data.keys():
        return True
    return False


def transform_data(class_name: str, old_class_data: dict):
    """
    Take class name (eg from old style cld filename), and loaded json dict,
    transform into a new-style Class object.

    :param class_name: str
    :param old_class_data: dict
    :return: Class object
    """
    new_students = []
    for student_name in old_class_data:
        if old_class_data[student_name][0] is None:
            new_students.append(Student(name=student_name))
        else:
            new_students.append(Student(name=student_name,
                                        avatar_filename=old_class_data[student_name][0]),
                                )
    new_class = Class(name=class_name, students=new_students)
    return new_class


def file_from_gui_dialogue():
    """
    Spawn a GUI file selection dialogue, and transform the selected file into
    the new data format.

    :return: None
    """
    filepath = get_data_file()
    if filepath:
        transform_old_cld_file(filepath)
    if not filepath:
        print('No file selected.')


def get_data_file():
    """
    Prompt user to select a file from a GUI file selection dialogue.

    :return: Path or None
    """
    selected_filename = select_file_dialogue(title_str='Select file to transform:',
                                             filetypes=[('.cld', '*.cld'), ("all files", "*.*")],
                                             start_dir=CLASSLIST_DATA_PATH,
                                             )

    if selected_filename is None:
        return None
    return selected_filename


if __name__ == '__main__':
    main()
    time.sleep(5)
