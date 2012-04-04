#!/usr/bin/python

"""
raptor.py intercepts known commands, and just sends unknown commands
over to git
"""

import os
import sys
import subprocess

if len(sys.argv) < 2:
    print 'usage: %s [command] [options]' % (sys.argv[0], )
    sys.exit(0)

command = sys.argv[1]

def prompt(message, default):
    """
    prompt(message: str, default: bool) -> bool
    Prompts user with a yes/no message and default choice
    """
    message += (' [Y/n]: ' if default else ' [y/N]: ')
    result = raw_input(message)
    while True:
        if result == "":
            return default

        result = result.upper()
        if result == 'Y':
            return True
        elif result == 'N':
            return False
        else:
            result = raw_input("Please answer 'y' or 'n': ")
            if result == "": result = 'x'

def run_linter_py(filename):
    """
    run_linter_py(filename: str) -> int
    Runs linter on given filename and returns exit status
    """
    print 'Linter for %s' % (filename ,)

    status =  subprocess.call(['pylint', filename])
    print

    return status

# callback to run before a git commit
def commit_callback():
    """
    commit_callback() -> bool
    runs custom commit hooks, returns True if everything ok, False if should
    abort.
    """
    err_code = 0
    git_files = subprocess.Popen(
        ['git', 'diff', '--name-status'],
        stdout=subprocess.PIPE).communicate()[0]

    for line in str(git_files).strip().split('\n'):
        line = line.strip()

        # skip deleted files
        if line.startswith('D'): continue

        # run pylint on the files
        if len(line.split()) < 2: continue

        filename = line.split()[1]

        if filename.endswith('.py'):
            err_code += run_linter_py(filename)

        if err_code == 0:
            # no errors or warnings, all good.
            return True
        else:
            # some errors/warnings, let's talk to the user
            return prompt('Linter raised unresolved issues. Continue?', False)

## falls back to normal git if the command isn't being treated
## specifically
def git_passthru():
    """
    git_passthru() -> None
    runs git with options passed to raptor.
    """
    cmd = 'git %s' % (' '.join(sys.argv[1:]))
    os.system(cmd)

recognized_commands = {
    'commit': commit_callback
}

if command in recognized_commands:
    if recognized_commands[command]():
        git_passthru()
    else:
        print "Aborting command due to unresolved issues."
        sys.exit(0)
else:
    git_passthru()
