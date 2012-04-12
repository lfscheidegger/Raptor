import sys

from src.bash_support import print_colored
from src.bash_support import run_command
from src.git_support  import get_aliases
from src.git_support import passthrough
from src.hooks.commit import exports as commit_exports
#from src.hooks.push   import exports as push_exports
from src.hooks.lint   import exports as lint_exports

def usage():
    print 'usage: %s [command] [options]' % (sys.argv[0], )
    sys.exit(0)



def main():
    options = sys.argv[1:]
    command = ""
    try: command = options[0]
    except IndexError: pass

    aliases = get_aliases()
    if command in aliases:
        command = aliases[command]

    recognized_commands = {
        commit_exports[0]: commit_exports[1],
        #push_exports[0]  : push_exports[1],
        lint_exports[0]  : lint_exports[1]
    }

    if command in recognized_commands:
        if recognized_commands[command](sys.argv):
            pasthrough(options)
        else:
            print_colored('Raptor raised unresolved issues.', color='red')
    else:
        print_colored('Uncaptured command. Defaulting to git...', color='green')
        passthrough(options)

if __name__ == '__main__':
    main()
