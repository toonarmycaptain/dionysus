# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Improved test coverage.

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
