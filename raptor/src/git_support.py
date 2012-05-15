# Raptor - smart hooks for git
# Copyright (C) 2012 Luiz Scheidegger

"""
git_support.py

Functions to interact with common git commands.
"""

from raptor.src.bash_support import run_command

def get_aliases():
    """
    get_aliases() -> dict
    returns a dictionary containing git command aliases, where the
    keys are the aliases and the values are the corresponding actual
    command names
    """

    output = run_command('git config --get-regexp alias*')

    aliases = output['stdout'].split('\n')

    result = {}

    for alias in aliases:
        if len(alias) == 0: 
            continue
        
        alias_name = alias.split()[0][6:]
        alias_value = alias.split(' ', 1)[1]

        result[alias_name] = alias_value
        
    return result

def get_diffed_files(diff_output, **kwargs):
    include_deleted = False
    try: 
        include_deleted = kwargs['include_deleted']
    except KeyError: 
        pass

    result = []

    lines = diff_output.strip().split('\n')
    for line in lines:
        try:
            [status, filename] = line.split()
            if status == 'D' and not include_deleted: 
                continue
            result.append(filename)
        except ValueError:
            pass

    return result

def passthrough(options):
    """
    git_passthrough() -> None
    runs git with options passed to raptor.
    """
    cmd = 'git %s' % (' '.join(options))
    run_command(cmd, ignore_output=True)
