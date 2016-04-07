class DefinitionConflictError(Exception):
    pass


class UndefinedTypeError(Exception):
    pass


class InvalidParameterError(Exception):
    pass


class ExecutionResult(object):
    def __init__(self, message, diff=None, success=True):
        self.message = message
        self.diff = diff
        self.success = success
