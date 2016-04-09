Writing plugins
===============

Every plugin is its own Python package. The name for the package must be ``tinycm_<name>`` and that package
should have the class ``<Name>Definition`` in its __init__.py file.

In the case of the example vim plugin: ``tinycm_vim`` and ``VimDefinition``

The Definition class should subclass ``tinycm.basedefinition.BaseDefinition``. A example of an empty plugin:

.. code-block:: python

    from tinycm.basedefinition import BaseDefinition
    from tinycm import Dependency, ExecutionResult
    from tinycm.reporting import VerifyResult

    class ExampleDefinition(BaseDefinition)
        def __init__(self, identifier, parameters, source, after, context):
                # Run the BaseDefinition init so the graph library works
                super().__init__(identifier)

                # The usual fields
                self.identifier = identifier
                self.source = source
                self.after = after
                self.context = context
                self.name = parameters['name']

        def try_merge(self, other):
            """
            This method is called when a duplicate definition exists.
            Return a merged definition or raise DefinitionConflictError
            """
            return self

        def lint(self):
            """
            This method is called after all definitions have been parsed. This is the
            point where you can raise an InvalidParameterError because the manifest
            contains invalid parameters
            """
            pass

        def verify(self):
            """
            This method is where you check if the current state of the linux installation matches
            The parameters defined in this definition.

            This method must always return a VerifyResult
            """
            return VerifyResult(self.identifier, success=True)

        def execute(self):
            """
            This method is called if --apply is passed to TinyCM.
            Here you manipulate the state of the Linux machine so it matches the definition
            and it should be the only place that actually changes anything on the machine.
            You should probably call self.verify() here to check if anything needs to be done.
            """
            return ExecutionResult("Changed something on the server")

        def dependencies(self):
            """
            Here you can create other definitions that need to be successfull before this definition
            is run. The vim plugin doesn't do anything in it's own verify and execute method
            but specifies a file and package dependency based on the parameters passed to the plugin.
            """
            return [Dependency('package', 'vim', {'ensure': 'installed'})]
