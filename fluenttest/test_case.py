import mock


class TestCase(object):

    """Arrange, Act, Assert test case.

    Sub-classes implement test cases by *arranging* the environment in the
    :py:meth:`configure` class method, perform the *action* in the
    :py:func:`act` class method, and implement *assertions* as test methods.
    The individual assertion methods have to be written in such a way that
    the test runner in use finds them.

    .. py:attribute:: allowed_exceptions

        The exception or list of exceptions that the test case is interested in
        capturing.  An exception raised from :py:meth:`act` will be stored
        in :py:attr:`exception`.

    .. py:attribute:: exception

        The exception that was thrown during the action or ``None``.

    """

    allowed_exceptions = ()
    """Catch this set of exception classes."""

    @classmethod
    def setup_class(cls):
        """Arrange the environment and perform the action.

        This method ensures that :py:meth:`arrange` and :py:meth:`act` are
        invoked exactly once before the assertions are fired.  If you do find
        the need to extend this method, you should call this implementation
        as the last statement in your extension method as it will perform the
        action when it is called.

        """
        cls.exception = None
        cls._patches = []

        cls.arrange()
        try:
            cls.act()
        except cls.allowed_exceptions as exc:
            cls.exception = exc
        finally:
            cls.destroy()

    @classmethod
    def teardown_class(cls):
        """Stop any patches that have been created."""
        for patcher in cls._patches:
            patcher.stop()

    @classmethod
    def arrange(cls):
        """Arrange the testing environment.

        Concrete test classes will probably override this method and should
        invoke this implementation via ``super()``.

        """
        pass

    @classmethod
    def destroy(cls):
        """Perform post-test cleanup.

        Concrete tests classes may override this method if there are actions
        that need to be performed after :py:meth:`act` is called.

        """
        pass

    @classmethod
    def patch(cls, target, patch_name=None, **kwargs):
        r"""Patch a named class or method.

        :param str target: the dotted-name to patch
        :returns: the result of starting the patch.

        This method calls :py:func:`mock.patch` with *target* and
        *\*\*kwargs*, saves the result, and returns the running patch.

        """
        patcher = mock.patch(target, **kwargs)
        patched = patcher.start()
        cls._patches.append(patcher)
        return patched

    @classmethod
    def patch_instance(cls, target, **kwargs):
        r"""Patch a named class and return the created instance.

        :param str target: the dotted-name of the class to patch
        :returns: tuple of (patched class, patched instance)

        This method calls :py:meth:`patch` with *\*\*kwargs* to patch
        *target* and returns a tuple containing the patched class as
        well as the ``return_value`` attribute of the patched class.
        This is useful if you want to patch a class and manipulate the
        result of the code under test creating an instance of the class.

        """
        patched_class = cls.patch(target, **kwargs)
        return patched_class, patched_class.return_value

    @classmethod
    def act(cls):
        """The action to test.

        **Subclasses are required to replace this method.**

        """
        raise NotImplementedError
