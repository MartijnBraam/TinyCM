import ruamel.yaml
import difflib
from colorama import Fore, Style
import logging


def get_state_diff(tasks):
    logger = logging.getLogger('tinycm')
    for task in tasks:
        logger.debug('Making state diff for {}'.format(task.identifier))
        config_state = task.get_config_state()
        system_state = task.get_system_state()
        yield StateDiff(task, config_state, system_state)


class StateDiff(object):
    def __init__(self, task, config, system):
        self.config = config
        self.system = system
        self.logger = logging.getLogger('tinycm')

        self.config_text = ruamel.yaml.safe_dump(config, default_flow_style=False)
        self.system_text = ruamel.yaml.safe_dump(system, default_flow_style=False)

        config_lines = self.config_text.splitlines(True)
        system_lines = self.system_text.splitlines(True)
        self.diff = difflib.unified_diff(system_lines, config_lines,
                                         fromfile="Current state",
                                         tofile="Wanted state ")

        changed = self.changed_keys()
        self.correct = len(changed) == 0
        if not self.correct:
            self.logger.debug('State for {} is incorrect'.format(task.identifier))
        self.task = task
        self.identifier = task.identifier

    def changed_keys(self):
        config = []
        system = []
        for item in self.config.items():
            if isinstance(item[1], list):
                config.append((item[0], tuple(item[1])))
            else:
                config.append(item)
        for item in self.system.items():
            if isinstance(item[1], list):
                system.append((item[0], tuple(item[1])))
            else:
                system.append(item)
        config = set(config)
        system = set(system)

        key_value_diff = config ^ system
        changed = []

        for item in key_value_diff:
            if item[0] in self.config:
                changed.append(item[0])

        return set(changed)

    def print_diff(self, indent=0):
        indent = " " * indent
        for line in self.diff:
            if line.startswith('+'):
                print(indent + Fore.GREEN + line + Style.RESET_ALL, end='')
            elif line.startswith('-'):
                print(indent + Fore.RED + line + Style.RESET_ALL, end='')
            else:
                print(indent + line, end='')

    def __repr__(self):
        correct = 'Incorrect'
        if self.correct:
            correct = 'Correct'
        return "<StateDiff {} {}>".format(self.task.identifier, correct)
