"""
commit.py

Callback for a custom git pre-commit hook.
"""

from src.bash_support import run_command
from src.git_support import get_diffed_files
from src.jobs.lint import prompt_lint

def callback(args):
    """
    commit_callback() -> bool
    runs custom commit hooks, returns True if everything ok, False if should
    abort.
    """
    command = ''
    if '-a' in args or '--all' in args:
        command = 'git diff HEAD --name-status'
    else:
        command = 'git diff --cached --name-status'
    
    output = run_command(command)
    git_files = get_diffed_files(output['stdout'])

    return prompt_lint(git_files)

exports = ('commit', callback)
