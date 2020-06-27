import argparse
import json
import sys
import time

from pathlib import Path
from typing import Optional

from dionysus_app.class_ import Class
from dionysus_app.file_functions import load_from_json_file
from dionysus_app.persistence.databases.json import JSONDatabase
from dionysus_app.student import Student
from dionysus_app.UI_menus.UI_functions import select_file_dialogue


def main() -> None:
    """
    Process arguments, run script based on args.

    :return: None
    """
    run_args = parse_args(sys.argv[1:])

    run_script(run_args)


def parse_args(args: list) -> argparse.Namespace:
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


def run_script(args: argparse.Namespace) -> None:
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
    json_database = JSONDatabase()
    print(f'args={args}')
    print(f'args.filepath={args.filepath}')
    if args.all_class_data_files:
        transform_all_old_data_files(json_database)

    elif args.filepath:
        transform_old_cld_file(json_database, Path(args.filepath))

    else:
        file_from_gui_dialogue(json_database)


def transform_all_old_data_files(json_database: JSONDatabase = None) -> None:
    """
    Transform data files matching old format to new format.
    Instantiates JSONDatabase with default args.

    :param json_database: JSONDatabase object
    :return: None
    """
    if not json_database:
        json_database = JSONDatabase()
    for old_class_data_file in json_database.class_data_path.glob('**/*.cld'):
        transform_old_cld_file(json_database, Path(old_class_data_file))

    # NB can add operation to call on chart data files too if this is desired.


def transform_old_cld_file(json_database: JSONDatabase, filepath: Path) -> None:
    """
    Transform .cld file to new format.

    Takes a database object.
    If none is passed, instantiates JSONDatabase with default args.

    NB If file is in the wrong location, or not in class data at all, a folder
    with the class name will be created in class_data.

    :param json_database: JSONDatabase object
    :param filepath: Path
    :return: None
    """
    if not json_database:
        json_database = JSONDatabase()

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

    # Write to file rather than modifying in-place database:
    json_database._write_classlist_to_file(new_class)

    new_filename = class_name + json_database.class_data_file_type
    new_class_data_path_name = json_database.class_data_path.joinpath(class_name, new_filename)

    print(f'Transformed {new_class.name} data file '
          f'to new data format in {new_class_data_path_name}')


def data_is_new_format(old_class_data: dict) -> bool:
    """
    Test if json dict data is in current format to avoid mangling good data.

    :param old_class_data: dict
    :return: Bool
    """
    return 'students' in old_class_data and 'name' in old_class_data


def transform_data(class_name: str, old_class_data: dict) -> Class:
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
                                        avatar_id=old_class_data[student_name][0]),
                                )
    return Class(name=class_name, students=new_students)


def file_from_gui_dialogue(json_database) -> None:
    """
    Spawn a GUI file selection dialogue, and transform the selected file into
    the new data format.

    :return: None
    """
    filepath = get_data_file(json_database)
    if filepath:
        transform_old_cld_file(json_database, filepath)
    if not filepath:
        print('No file selected.')


def get_data_file(json_database: JSONDatabase) -> Optional[Path]:
    """
    Prompt user to select a file from a GUI file selection dialogue.

    :return: Path or None
    """
    selected_filename = select_file_dialogue(title_str='Select file to transform:',
                                             filetypes=[('.cld', '*.cld'), ("all files", "*.*")],
                                             start_dir=json_database.class_data_path,
                                             )

    if selected_filename is None:
        return None
    return selected_filename


if __name__ == '__main__':
    main()
    time.sleep(5)
