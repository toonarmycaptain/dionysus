# Instructions for bumping python versions

When bumping version, need to modify version specifiers in all of these files:

.github/workflows/CI.yml  # can leave still passing versions in, just add new ones.
appveyor.yml
pyproject.toml  # if bumping lowest version (left < supported at present while tests for lower versions are passing)

README.md - bump supported versions. 
