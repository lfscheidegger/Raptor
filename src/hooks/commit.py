from src.bash_support import print_colored
from src.bash_support import prompt
from src.bash_support import run_command
from src.git_support import get_diffed_files
from src.jobs.lint import lint

def callback(args):
    """
    commit_callback() -> bool
    runs custom commit hooks, returns True if everything ok, False if should
    abort.
    """
    err_code = 0

    command = ''
    if '-a' in args or '--all' in args:
        command = 'git diff HEAD --name-status'
    else:
        command = 'git diff --cached --name-status'
    
    output = run_command(command)
    git_files = get_diffed_files(output['stdout'])

    # runs linter
    if not lint(git_files):
        return prompt('Lint raised unresolved issues. Continue?', False)
    else:
        print_colored('Lint raised no issues', color='green')
        return True

    return False

exports = ('commit', callback)
