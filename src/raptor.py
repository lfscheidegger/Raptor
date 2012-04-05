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

def check_diff_line(line):
    """
    check_diff_line(line: str) -> int
    processes an individual git diff line and returns int return codes
    """
    line = line.strip()

    # skip deleted files
    if line.startswith('D'): return 0

    # run pylint on the files
    if len(line.split()) < 2: return 0

    filename = line.split()[1]

    if filename.endswith('.py'):
        return run_linter_py(filename)

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
        err_code += check_diff_line(line)

    if err_code == 0:
        # no errors or warnings, all good.
        return True
    else:
        # some errors/warnings, let's talk to the user
        return prompt('Linter raised unresolved issues. Continue?', False)

def push_callback():
    """
    push_callback() -> bool
    runs custom push hooks, returns True if everythink ok, False if should
    abort.
    """

    remote_name = sys.argv[2]
    branch_name = sys.argv[3].split(':')[1]

    [stdout, stderr] = subprocess.Popen(
        ['git', 'diff', '--stat', '--name-status', 
         '%s/%s' % (remote_name, branch_name)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    stdout = str(stdout).strip()
    stderr = str(stderr).strip()

    if stderr.startswith('fatal'):
        print 'remote has no branch "%s"' % (branch_name,), \
            '- falling back to master'
        [stdout, stderr] = \
            subprocess.Popen(
                 ['git', 'diff', '--stat',
                  '--name-status', '%s/master' % (remote_name, )],
                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)\
            .communicate()

        stdout = str(stdout).strip()
        stderr = str(stderr).strip()

        if stderr.startswith('fatal'):
            print "couldn't push to master. bailing."
            return False

    err_code = 0

    lines = stdout.split('\n')
    for line in lines:
        err_code += check_diff_line(line)

    if err_code == 0:
        # no errors or warnings, all good.
        return True
    else:
        # some errors/warnings, let's talk to the user
        return prompt('Linter raised unresolved issues. Continue?', False)

def lint_callback():
    """
    lint_callback() -> int
    runs custom callback to just check the linter
    """

    err_code = 0
    git_files = subprocess.Popen(
        ['git', 'diff', '--name-status'],
        stdout=subprocess.PIPE).communicate()[0]

    for line in str(git_files).strip().split('\n'):
        err_code += check_diff_line(line)

    if err_code == 0:
        print 'Linter raised no issues.'
        sys.exit(0)
    else:
        print 'Linter raised unresolved issues.'
        sys.exit(0)

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
    'commit': commit_callback,
    'push': push_callback,
    'lint': lint_callback
}

if command in recognized_commands:
    if recognized_commands[command]():
        git_passthru()
    else:
        print "Aborting command due to unresolved issues."
        sys.exit(0)
else:
    git_passthru()
