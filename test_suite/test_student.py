"""Tests for Student class."""
import pytest

from dionysus_app.student import Student


@pytest.fixture()
def test_student_name_only():
    test_name = 'Arthur, King of the Britons'
    yield Student(test_name)


@pytest.fixture()
def test_student_with_avatar():
    test_name = 'Arthur, King of the Britons'
    test_avatar_id = 'Arthur'
    yield Student(name=test_name, avatar_id=test_avatar_id)


class TestStudentName:
    """
    Test Student name and path_safe_name properties.
    """

    def test_name_getter(self):
        test_name = 'Arthur, King of the Britons'
        assert Student(name='Arthur, King of the Britons').name == test_name

    def test_name_setter_unmocked(self, test_student_name_only):
        test_changed_name = 'Sir Lancelot: the not-so-brave'
        assert test_student_name_only.name != test_changed_name

        # Change name
        test_student_name_only.name = test_changed_name

        assert test_student_name_only.name == test_changed_name

    @pytest.mark.parametrize(
        'name_arg',
        [{'passing a dict': 'Some value'},  # dict
         ['passing', 'a', 'list'],  # list
         Student('Student object for name'),  # Student object
         ('passed', 'tuple',),  # tuple
         ])
    def test_non_str_name_raises_error(self, name_arg):
        """Test error is raised for each bad type, error msg contains type."""
        with pytest.raises(TypeError, match=str(type(name_arg))):
            Student(name=name_arg)


class TestStudentAvatar:
    def setup_method(self):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        self.test_name = 'Arthur, King of the Britons'
        self.test_avatar_id = 'camelot.jpg'

    def test_no_avatar_on_instantiation(self, test_student_name_only):
        assert test_student_name_only.avatar_id is None

    def test_change_avatar(self, test_student_name_only):
        assert test_student_name_only.avatar_id != self.test_avatar_id

        test_student_name_only.avatar_id = self.test_avatar_id

        assert isinstance(test_student_name_only.avatar_id, str)
        assert test_student_name_only.avatar_id == self.test_avatar_id

    def test_change_avatar_passing_path(self, test_student_name_only):
        assert test_student_name_only.avatar_id != self.test_avatar_id

        test_student_name_only.avatar_id = self.test_avatar_id

        assert isinstance(test_student_name_only.avatar_id, str)
        assert test_student_name_only.avatar_id == self.test_avatar_id

    # Test instantiate with avatar_id:

    def test_instantiate_with_avatar_id(self):
        test_instantiate_student_with_avatar = Student(self.test_name,
                                                       avatar_id=self.test_avatar_id)

        assert test_instantiate_student_with_avatar.avatar_id == self.test_avatar_id

        assert isinstance(test_instantiate_student_with_avatar.avatar_id, str)


class TestStudentJsonDict:
    @pytest.mark.parametrize(
        'student_object,output_json',
        [(Student('Sir Galahad'), {'name': 'Sir Galahad'}),  # name only
         (Student('Sir Lancelot: the Brave', avatar_id=None), {'name': 'Sir Lancelot: the Brave'}),
         (Student('Arther, King of the Britons', avatar_id='Holy_Grail.jpg'),
          {'name': 'Arther, King of the Britons', 'avatar_id': 'Holy_Grail.jpg'}
          ),
         (Student('Brian', avatar_id='a_naughty_boy.png'),
          {'name': 'Brian', 'avatar_id': 'a_naughty_boy.png'}),
         ])
    def test_json_dict(self, student_object, output_json):
        assert student_object.json_dict() == output_json


class TestStudentFromDict:
    @pytest.mark.parametrize('student_class_def', [Student])
    @pytest.mark.parametrize(
        'output_json_dict',
        [({'name': 'Sir Galahad'}),  # name only
         ({'name': 'Sir Lancelot: the Brave'}),
         ({'name': 'Arther, King of the Britons', 'avatar_id': 'Holy_Grail.jpg'}),
         ({'name': 'Brian', 'avatar_id': 'a_naughty_boy.png'}),
         ])
    def test_from_dict(self, student_class_def, output_json_dict):
        student_object = student_class_def.from_dict(output_json_dict)
        assert isinstance(student_object, student_class_def)
        # Verify instantiated object is equivalent by reserialising:
        assert student_object.json_dict() == output_json_dict

        # Test attributes
        assert student_object.name == output_json_dict['name']
        if output_json_dict.get('avatar_id') is not None:
            assert str(student_object.avatar_id) == output_json_dict['avatar_id']


class TestStudentRepr:
    @pytest.mark.parametrize('student_object',
                             [Student(name='I have no avatar!'),
                              Student(name='I have an avatar', avatar_id='my_avatar_id.png'),
                              ])
    def test_repr(self, student_object):
        assert repr(student_object) == (f'{student_object.__class__.__module__}'
                                        f'.{student_object.__class__.__name__}('
                                        f'name={student_object._name!r}, '
                                        f'avatar_id={student_object._avatar_id!r})')


class TestStudentStr:
    @pytest.mark.parametrize(
        'student_object,'
        'expected_str',
        [(Student(name='I have no avatar!'),
          f"Student {'I have no avatar!'}, with no avatar."),
         (Student(name='I have an avatar', avatar_id='path_to_my_avatar'),
          f"Student {'I have an avatar'}, with avatar {'path_to_my_avatar'}."),
         ])
    def test_str(self, student_object, expected_str, test_student_name_only, test_student_with_avatar):
        assert str(student_object) == expected_str
