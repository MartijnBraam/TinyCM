Writing plugins
===============

Every plugin is its own Python package. The name for the package must be ``tinycm_<name>`` and that package
should have the class ``<Name>Definition`` in its __init__.py file.

In the case of the example vim plugin: ``tinycm_vim`` and ``VimDefinition``

The Definition class should subclass ``tinycm.basedefinition.BaseDefinition``. A example of an empty plugin:

.. code-block:: python

    from tinycm.basedefinition import BaseDefinition

    class ExampleDefinition(BaseDefinition)
        def init(self, ensure, foo, bar=None):
            """
            This is where you receive the parameters passed to the definition.
            You can create optional and required parameters. This is also
            where you should check if the combination of paramaters is valid.

            The `name` parameter is handled by the __init__ of BaseDefinition
            and is saved to `self.name`
            """
            self.ensure = ensure
            self.foo = foo
            self.bar = bar

        def try_merge(self, other):
            """
            This method is called when a duplicate definition exists.
            Return a merged definition or raise DefinitionConflictError

            The BaseDefinition has a helper function `merge_if_same` that
            will merge the parameter is the same value or if one of the
            definitions has the parameter undefined.
            """
            self.foo = self.merge_if_same('foo', other)
            return self

        def get_config_state(self):
            """
            Get a dict containing the state defined in this definition. This
            excludes any parameters that are only required for state change.

            For example the 'manage-home' parameter for used isn't listed
            here.

            Parameters that are not defined by the user shouldn't be
            returned here
            """
            result = {
                'exists': self.ensure == 'exists',
                'foo': self.foo
            }
            if self.bar:
                result['bar'] = self.bar
            return result

        def get_system_state(self):
            """
            Get a dict containing the current system state with the same
            rules as `get_config_state()`.

            This method should return all posible parameters, not just
            the ones defined by the user.
            """
            exists = does_it_exist_already()
            if it_exists_already()
                return {
                    'exists': True,
                    'foo': get_the_current_system_foo(),
                    'bar': get_the_current_system_bar()
                }
            else:
                return {
                    'exists': False
                }

        def update_state(self, state_diff):
            """
            This is where the actual system state is updated. The
            `state_diff` object contains the changes between the
            current system state and the user defined state.
            """
            diff = state_diff.changed_keys()

            if 'exists' in diff:
                if self.ensure == 'exists':
                    create_the_thing()
                else:
                    remove_the_thing()

            else:
                if 'foo' in diff:
                    change_the_system_foo()
                if 'bar' in diff:
                    change_the_system_bar()

        def dependencies(self):
            """
            Here you can create other definitions that need to be successfull before this definition
            is run. The vim plugin doesn't do anything in it's own verify and execute method
            but specifies a file and package dependency based on the parameters passed to the plugin.
            """
            return [Dependency('package', 'vim', {'ensure': 'installed'})]
