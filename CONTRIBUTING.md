\[This document is a work in progress.]

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

This project is open source, primarily aimed at teachers. 
This project is designed primarily for teachers to present assessment results/snapshots of a classes' grades 
to students in graphical form, using student created avatars instead of names.

#### Table Of Contents
[Code of Conduct](#code-of-conduct)

[Codestyle](#codestyle)

[Documentation](#documentation)

[PR notes](#pr-notes)

## Code of Conduct
The main thing here is *be nice*, be considerate to others. This includes writing clear, documented code!

Please include clear commit/PR comments, reference issues etc - this is helpful for anyone trying to follow along.

Please keep PRs to one issue as much as possible! Multiple PRs for separate issues is fine and keeps things simple. 

If you want to suggest or implement new features - email, open an issue, make a PR! Anything that's useful without cluttering
the UI too much is welcome.

## Codestyle

Conform to [PEP8](https://www.python.org/dev/peps/pep-0008/) as much as possible/sensible. 

Clear, well documented code is the goal. 

Document. 

Use [type hints](https://docs.python.org/3/library/typing.html). This can be invaluable for avoiding/finding bugs!

## Documentation

So far documentation conforms roughly to a reST/Sphinx style, which happens to also be the default for PyCharm:

```python
def my_function(param0: type, param1: str, param2: dict):
    """
    This is a reST style. 
    Miss a line between docstring text and parameters/return/exceptions.
    If there are multiple parameters, multiple potential errors raise/handled, it can be clearer
    to separate the grouped category, much like in Google's style guide. 

    :param param0: type explanation
    :param param1: str this is explanation for first param
    :param param2: dict this is another parameter  # given 3 params, might be clearer with newline here.
    :returns: this is a description of what is returned
    :raises keyError: raises an exception
    """
```

## PR notes

-   Make PRs to development branch, or appropriate feature branch if it exists (if you'd like to collaborate on a 
new feature or issue, leave a comment and a branch can be created).

-   Some of the code review tools (particularly Codacy) flag good code as issues (eg `assert` used in tests,
 correctly formatted f-strings). Please leave a comment about any issues the reviewers flag that you believe are 
 are false flags, so that they can be ignored in those integrations. Legitimate issues, please amend the PR to fix them!

-   Small commits with well described commit messages, and single issue PRs are preferable to monolithic commits that add 
several features and address multiple issues - it's far easier to review, fix/modify if necessary, and merge simple PRs 
than complex ones!

-   Tests for new or modified features are requested with the PR, but not required.
  
  