import subprocess

color_code_map = {
    'none': '\033[0m',
    'black':  '\033[030m',
    'red':    '\033[31m',
    'green':  '\033[32m',
    'brown':  '\033[033m',
    'blue':   '\033[034m',
    'purple': '\033[35m',
    'cyan':   '\033[36m',
    'gray':   '\033[037m',
    'yellow': '\033[1;33m'
}

def print_colored(*args, **kwargs):
    color = color_code_map['none']
    try:
        color = color_code_map[kwargs['color']]
    except KeyError:
        pass

    print color + ' '.join(args) + color_code_map['none']

def run_command(cmd, **kwargs):
    if kwargs.has_key('ignore_output'):
        subprocess.Popen(
            cmd.split())
    else:
        [stdout, stderr] = subprocess.Popen(
            cmd.split(),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        return {
            'stdout': str(stdout),
            'stderr': str(stderr)
            }

def call_command(cmd):
    return subprocess.call(cmd.split())

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
