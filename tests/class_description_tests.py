import unittest

from fluenttest import ClassTester, the_class


class TheClassFunction(unittest.TestCase):

    def should_be_extensible(self):
        describer = the_class(dict, matcher_class=_ExtendedClassTester)
        assert isinstance(describer, _ExtendedClassTester)


class ImplementMethods(unittest.TestCase):

    def setUp(self):
        self.describer = the_class(dict)

    def should_return_True_for_existing_method(self):
        assert self.describer.implements_method('setdefault')

    def should_return_False_for_missing_methods(self):
        assert not self.describer.implements_method('missing_method')


class IsSubclassOf(unittest.TestCase):

    def setUp(self):
        self.describer = the_class(_ClassUnderTest)

    def should_return_True_for_parent_class(self):
        assert self.describer.is_subclass_of(_ParentClass)

    def should_accept_class_as_fully_qualified_path_name(self):
        assert self.describer.is_subclass_of(
            'tests.class_description_tests._GrandparentClass')


class HasAttribute(unittest.TestCase):

    def setUp(self):
        self.describer = the_class(_ClassUnderTest)

    def should_return_True_for_class_attribute(self):
        assert self.describer.has_attribute('class_attribute')

    def should_can_check_attribute_type(self):
        assert self.describer.has_attribute('class_attribute', typed=basestring)


######################################################################
## Test Data

class _GrandparentClass(object):
    pass


class _ParentClass(_GrandparentClass):
    pass


class _ClassUnderTest(_ParentClass):

    class_attribute = 'string value'

    @classmethod
    def a_class_method(cls):
        pass


class _ExtendedClassTester(ClassTester):
    pass