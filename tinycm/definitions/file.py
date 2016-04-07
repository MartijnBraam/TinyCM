from tinycm import DefinitionConflictError, InvalidParameterError, ExecutionResult
from tinycm.basedefinition import BaseDefinition
from tinycm.reporting import VerifyResult
import os
import requests
import difflib


class FileDefinition(BaseDefinition):
    def __init__(self, identifier, parameters, source, after, context):
        self.source = source
        self.after = after
        self.identifier = identifier
        self.type = parameters['type']
        self.path = parameters['name']
        self.contents = parameters['contents']
        self.context = context

        # Optional parameters
        self.interpolate = False
        self.encoding = "utf-8"
        self.ensure = 'contents'

        if 'interpolate' in parameters:
            self.interpolate = parameters['interpolate']
        if 'encoding' in parameters:
            self.encoding = parameters['encoding']
        if 'ensure' in parameters:
            self.ensure = parameters['ensure']

        # Internal parameters
        self._fetched_and_interpolated = False

        super().__init__(identifier)

    def try_merge(self, other):
        if self.type != other.type:
            raise DefinitionConflictError('Duplicate definition for {} with different type'.format(self.identifier))
        if self.contents != other.contents:
            raise DefinitionConflictError('Duplicate definition for {} with different contents'.format(self.identifier))
        return self

    def _ensure_contents(self):
        if self._fetched_and_interpolated:
            return

        if self.type == 'http':
            url = self.contents
            response = requests.get(url)
            self.contents = response.content().decode(self.encoding)

        if self.interpolate:
            self.contents = self.contents.format(**self.context)

        self._fetched_and_interpolated = True

    def lint(self):
        if self.type not in ['constant', 'http']:
            raise InvalidParameterError('Type not in [constant, http]')
        if self.ensure not in ['deleted', 'exists', 'contents']:
            raise InvalidParameterError('Ensure not in [deleted, exists, contents]')

    def verify(self):
        self._ensure_contents()
        if not os.path.isfile(self.path):
            return VerifyResult(self.identifier, success=False, message="File {} does not exist".format(self.path))
        if self.type == 'constant':
            with open(self.path) as input_file:
                contents = input_file.read()
            if contents != self.contents:
                return VerifyResult(self.identifier, success=False,
                                    message="File contents incorrect for {}".format(self.path))
        return VerifyResult(self.identifier, success=True)

    def execute(self):
        self._ensure_contents()
        verify_result = self.verify()
        exists = os.path.isfile(self.path)
        if exists:
            with open(self.path, 'r') as input_file:
                old_file = input_file.readlines()

        if not verify_result.success:
            with open(self.path, 'w') as target_file:
                target_file.write(self.contents)

        if exists:
            new_lines = self.contents.split("\n")
            diff = difflib.context_diff(old_file, new_lines,
                                        fromfile="old {}".format(self.path),
                                        tofile="new ".format(self.path))
            return ExecutionResult(message="Updated file {}".format(self.path), diff=diff)
        else:
            return ExecutionResult(message="Created file {}".format(self.path), diff=self.contents.split("\n"))
