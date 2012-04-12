from src.bash_support import run_command

def callback(args):
    """
    push_callback() -> bool
    runs custom push hooks, returns True if everythink ok, False if should
    abort.
    """

    remote_name = args[2]
    branch_name = args[3].split(':')[1]

    output = run_command('git diff --stat --name-status %s/%s' %\
                             (remote_name, branch_name))
    
    stdout = output['stdout'].strip()
    stderr = output['stderr'].strip()

    if stderr.startswith('fatal'):
        print 'remote has no branch "%s"' % (branch_name,), \
            '- falling back to master'
        output = run_command('git diff --stat --name-status %s/master' %\
                                 (remote_name, ))

        stdout = output['stdout'].strip()
        stderr = output['stderr'].strip()

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

exports = ('push', callback)
