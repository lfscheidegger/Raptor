"""
lint.py

Lints diffed files based on the configured linter.
"""

from src.bash_support import print_colored
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
        for regex in lint_engine['patterns']:
            if re.match(regex, filename):
                cmd = '%s %s' % (lint_engine['command'], filename)
                err_codes += call_command(cmd)

                break
        
    return err_codes == 0
