"""
lint.py

Lints diffed files based on the configured linter.
"""

from src.bash_support import print_colored
from src.bash_support import prompt
from src.bash_support import call_command
from src.config import get_config

import re

def lint(files):
    """
    lint(files: [str]) -> boolean

    Runs the configured linter for each file in files, and returns
    True if no linter issues are found, False otherwise.
    """
    config = get_config()
    try:
        lint_engine = config['linter']
    except KeyError:
        print_colored('No linter configured for this project.', color='yellow')
        return True

    print_colored('Running Linter...', color='none')

    err_codes = 0
    for filename in files:
        for lint_rule in lint_engine:
            regex = lint_rule['pattern']
            if re.match(regex, filename):
                linter = lint_rule['command']
                cmd = '%s %s' % (linter, filename)
                err_codes += call_command(cmd)
                break
        
    return err_codes == 0

def prompt_lint(files):
    """
    prompt_lint(files: [str]) -> boolean

    Higher level wrapper around lint() which prompts user upon success
    or failure.
    """

    if not lint(files):
        return prompt('Lint raised unresolved issues. Continue?', False)
    else:
        print_colored('Lint raised no issues', color='green')
        return True
