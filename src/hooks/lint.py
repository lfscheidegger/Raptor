def callback():
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

exports = ('lint', callback)
