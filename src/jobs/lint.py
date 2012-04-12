from src.bash_support import print_colored
from src.bash_support import call_command
from src.config import get_config

def lint(files):
    config = get_config()
    try:
        lint_engine = config['linter']
    except KeyError:
        print_colored('No linter configured for this project.', color='yellow')
        return True

    print_colored('Running Linter...', color='none')

    err_codes = 0
    for filename in files:
        cmd = '%s %s' % (lint_engine, filename)
        err_codes += call_command(cmd)
        
    return err_codes == 0
