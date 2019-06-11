# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Improved test coverage.
### Changed
- `select_student` now uses Class object, returns Student object.
- `file_functions` tests now all use new-style class data. 
### Depreciated
- Use of old-style data format in `testing_class_data` 
### Removed
- `class_functions.create_student_list_dict`

## [0.4.0-alpha] - 2019-05-22
### Added
- Class and Student objects.
- CLI script `data_version_conversion.py` to convert old data format to new.
    - Run without args spawns file selection GUI and converts selected file.
    - `-A`/`--all_class_data_files`: Process all the data files in class_data.
    - `--f`/`--filepath=path_to_file`: Process single file at path given to arg.
- Improved test coverage.
### Changed
- Changed data file data format reflecting serialised objects rather than dictionaries.
    - Core differences: 
        - the class' `name` is a key in the json dict
        - `students` is a key with a list of json-ified student objects
        - data (eg avatars) that is `None` is not saved to disk, but inferred on instantiation.
    - Reinstantiation to object rather than dict allows easy modification, additional attributes, change of data format or implementation of a database to be non-breaking changes.
- Changed implementation of `UI_functions.scrub_candiate_filename` to replace removed characters with `'_'` - this means 'Ni/' and 'Ni' will render non-identically as 'Ni_' and 'Ni'
- Factored out `create_app_data__init__` from `create_app_settings_file`.
- Changed target for pyup.io dependency updates to development branch.
- Updated dependencies.
- Progress conforming all path passing to use `Path` objects - in particular casting path str to `Path` before returning from GUI filedialogs. `load_chart_save_folder` now also returns `Path` object.
### Depreciated
- `class_functions.create_student_list_dict`: unused function loads class from disk to return an enumerated student list. Function is thus unnecessary when replaced by one-lined: `{numeral: student.name for numeral, student in enumerate(c.students, start=1)}`
### Fixed
- Rectified error where settings_dict was initialised with a string, not dict.

## [0.3.3-alpha] - 2019-03-04
### Added
- Added [codecov.io](https://codecov.io) coverage.
- Added/enable [Codeship](https://app.codeship.com) test build on Python 3.7.2 with manually-installed tkinter via `sudo apt-get install -y python3-tk`.
- Improved test coverage.
- Added `settings_functions_UI`.
- Implemented `create_chart_save_folder` - now creates new folder, moves existing folder.
### Changed
- Refactored `settings_menu` to match `main_menu` with a view to a future factoring out similar/common logic.
- Refactored settings_functions:
    - Factor out UI elements into `settings_functions_UI`.
    - Refactor folder move out of `create_chart_save_folder`. 
- `copy_file`, `move_file` now check to see if origin path exists, doing nothing if it does not.
- Update dependencies.

## [0.3.2-alpha] - 2019-02-15
### Added
- Improved test coverage.
### Changed
- Implementation of `take_student_scores`:
    - Move fetching of student data into `if` clause, fetch only if student has a score.
    - Simplify conditional to only filter out scores of `None` rather than chained conditional testing for values evaluating to `True` or `0`.
- Chart generation test scripts moved to dedicated folder in `test_suite`.
- Refactor application exit, `main_menu`:
    - Move `quit_app` to `app_main`, have `quit_app` call `check_registry_on_exit` before call to `sys.exit`.
    - Refactor `main_menu` and `take_main_menu_input` to use flag for exit call. `take_main_menu_input` returns `True` instead of `None` if use chooses to quit. 
- Simplify loop in `take_main_menu_input` preferring `if; if` over `if elif else`.
### Fixed
- `check_registry_on_exit` is now called on exit. Previously was called after `sys.exit` and not run. 

## [0.3.1-alpha] - 2019-02-06
### Added
- Improved test coverage.
- Add load_chart_data, load_json_from_file
- Add .bettercodehub.yml - prevent failed PR checks because of test code.
### Changed
- Refactor save_as_dialogue to prevent TypeError.
- Refactor load_class_data using load_from_json_file.
- Rename take_custom_chart_options to get_custom_chart_options to avoid name conflict. Calls UI function take_custom_chart_options.
### Fixed
- Fix bug where avatar for student with score of 0 not added to student_scores.
- Fix bug in save_as_dialogue that failed with TypeError when called without filetypes parameter or with default filetypes=None.
- Fix circleci not storing test metadata.

## [0.3.0-alpha] - 2019-01-23
### Added
- Improved test coverage.
- Add Contact note, saythanks.io badge to README.
- Add currently unimplemented select_student/take_student_selection functions mirroring similar class selection functionality.
- Select class/student dialogues will now take exact name of class/student (as well as integer per user direction), note this is to be considered an implementation detail, since a class with an integer name will only be selectable by entering that name if the integer is not displayed/larger that the number of options. 
### Changed
- Bugfixes
    - Fix path for default_avatar.
    - Fix cwd set in TestDataFolder.test_generate_data_path_defaults to draw from ROOT_DIR.
    - Fix bug - essentially blank (eg '_') chart name caused infinite loop. 
    - Add '.png' to save filename, as it is not otherwise appended.
- Major refactor of chart display and saving code.
    - Fixes major bugs where blank image would be saved, app would hang indefinitely.
    - Chart image now saves to app_data. Saved image is then displayed using Tkinter with a 'Save as' button. When this is pressed, image window disappears and os 'save as' dialogue is spawned, user can save where and as they choose.
    - Pillow is used to process the image, resize it for display.
- Refactor UI elements into dedicated functions and scripts in UI_menus.
- Add Pillow dependency, remove as yet unused numpy.
- Move converting int to str responsibility to UI functions taking input rather than doing so in function creating enumerated dict.


## [0.2.0-alpha] - 2018-12-31
### Added
- Save chart dialogue.
    - OS native 'save as' dialogue.
    - Starting default folder to class folder in dionysus charts ie dionysus_charts/class_name.
    - Default filename provided is sanitised user supplied chart name.
    - User can save chart in user selected location with user supplied filename.
    - Copy of image also saved in app_data/class_data/class_name/chart_data along with the chart data. 
- User defined location for dionysus_charts folder.  
    - Prompt to set location on startup, default location in application parent directory if user declines to set location.
    - Charts for each class will by default save in sub-folders for each class in dionysus_charts folder.
    - OS native prompt for location selection. 
- Add user settings, settings menu.
    - User can configure, reconfigure dionysus_charts save folder location.  
      Changing location moves current folder and contents.
- Add "not implemented" message when "Edit a classlist" is selected from main menu.    
- CI/Testing
    - Travis CI
        - Use Xenial distribution for Python 3.7 to build on Travis.
    - circleci
        - Add Python 3.7 testing via [circleci](https://codeclimate.com/github/toonarmycaptain/dionysus). 
        - circleci badge added to README.
    - Code Climate
        - Connect dionysus to [Code Climate](https://codeclimate.com/github/toonarmycaptain/dionysus)
        - Add Code Climate Maintainability badge to README.
    - Codebeat
        - Add [Codebeat](https://codebeat.co/projects/github-com-toonarmycaptain-dionysus-master) code quality checker.
        - Add .codebeatignore to ignore test code from code quality metrics    
    - Codeship
        - Add [Codeship CI](https://app.codeship.com/projects/320107), badge to README.
### Changed
- Charts save to correct location in dionysus_charts rather than in app_home folder.
- Reorganise menus/UI scripts into folder UI_menus.
- Moved app initialisation code to initialise_app.py.
       - data_folder_check moved here.
- REGISTRY variable moved to definitions.py.
- CI/Testing
    - Move testing/development dependencies to requirements_dev.txt.
    - Coveralls
        - Correct coverage calculation to only include project code (not testing or python env code).
    - Travis CI
        - Install testing dependencies from requirements_dev.txt rather than manually. 
        - Require passing tests Python 3.7 on Linux for successful build.
 ### Removed
- app_data/image_data folder. 
    - Unnecessary as saving images to external folder, and to class_data/*/chart_data folder. 
- class_registry.py.
    - REGISTRY variable moved to definitions.py.

    
## [0.1.1-alpha] - 2018-12-12
### Added
- OS native file select dialogue 
    - Add `select_file_dialogue` GUI using Tkinter.
    - Implement GUI dialogue for avatar selection. Resolves #79.
    - Add this [CHANGELOG.md](https://github.com/toonarmycaptain/dionysus/blob/master/CHANGELOG.md).     
### Changed
- Avatar image file now copied to app-data folder.
    - Add `file_copy` function. 
    - Implement in `copy_avatar_to_app_data` func. Resolves #67.
### Fixed
- Fix bug student with no score passed to chart generator, causing error.
### Removed
- Removed TODO file depreciated in favour of using issues, implementing a CHANGELOG.md.

## [0.1.0-alpha.1] - 2018-12-10
### Added
- Add installation, version docs.
### Changed
- Minor UI refinements
    - Prompt to hit enter after entering student name.
    - May enter 'N' instead of 'None' to skip avatar entry.
    - Prompt to press enter after entering student scores.
- Docs, dev changes
    - Exclude test code from Codacy analysis.
    - Separate dev from prod dependency requirements, update CI config accordingly.
### Depreciated
- TODO file - underutilised/un-updated
    - Track TODOs/issues in [github repo Issues](https://github.com/toonarmycaptain/dionysus/issues/), [Projects](https://github.com/toonarmycaptain/dionysus/projects), and other plans in the [Wiki](https://github.com/toonarmycaptain/dionysus/wiki).
    - Changes will be tracked in this [CHANGELOG.md](https://github.com/toonarmycaptain/dionysus/blob/master/CHANGELOG.md).
    - Remove in next release.

## [0.1.0-alpha] - 2018-12-10
Initial alpha release! Dionysus will take class lists, and successfully produce charts with the default avatar.

### Known bugs/non-functional features:
- setup.py is boilerplate and untested.
- User supplied avatar does not copy to app data folder and thus does not work in app.
- No indication of chart save location and not saving in desired/intended location in app_data/image_data/
- Need to cut and paste/type user supplied avatar location is too awkward.
- Preview/display of created chart does not reflect generated image accurately.
