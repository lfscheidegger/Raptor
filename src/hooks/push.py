# Raptor - smart hooks for git
# Copyright (C) 2012 Luiz Scheidegger

"""
push.py

Callback for git push.
"""

from src.bash_support import run_command
from src.bash_support import call_command
from src.bash_support import print_colored
from src.git_support import get_diffed_files
from src.jobs.lint import prompt_lint

def callback(args):
    """
    push_callback() -> bool
    runs custom push hooks, returns True if everythink ok, False if should
    abort.
    """

    try:
        remote_name = args[2]
        branch_name = args[3].split(':')[1]
    except IndexError:
        print_colored('Raptor doesnt support pushing without '+\
                      'arguments (yet). Sadface.', color='red')
        return False

    # fetch the remote so we have the most up-to-date information
    call_command('git fetch %s' % (remote_name, ))

    output = run_command('git diff HEAD %s/%s --name-status' %\
                             (remote_name, branch_name))
    
    stdout = output['stdout'].strip()
    stderr = output['stderr'].strip()

    if stderr.startswith('fatal'):
        print 'remote has no branch "%s"' % (branch_name,), \
            '- falling back to master'
        output = run_command('git diff HEAD %s/master --name-status' %\
                                 (remote_name, ))

        stdout = output['stdout'].strip()
        stderr = output['stderr'].strip()

        if stderr.startswith('fatal'):
            print "couldn't push to master. bailing."
            return False

    git_files = get_diffed_files(stdout)
    return prompt_lint(git_files)

exports = ('push', callback)
