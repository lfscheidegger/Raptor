# Raptor - smart hooks for git
# Copyright (C) 2012 Luiz Scheidegger
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

"""
main.py

main entry point for raptor.
"""

import sys

from src.bash_support import print_colored
from src.git_support  import get_aliases
from src.git_support import passthrough

from src.hooks.commit import exports as commit_exports
from src.hooks.push   import exports as push_exports

def usage():
    """
    usage() -> None
    
    prints small help message before exiting.
    """
    print 'usage: %s [command] [options]' % (sys.argv[0], )
    sys.exit(0)



def main():
    """
    main() -> None
    
    Main entry point function for raptor.
    """
    options = sys.argv[1:]
    command = ""
    try: 
        command = options[0]
    except IndexError: 
        pass

    aliases = get_aliases()
    if command in aliases:
        command = aliases[command]

    recognized_commands = {
        commit_exports[0]: commit_exports[1],
        push_exports[0]  : push_exports[1]
    }

    if command in recognized_commands:
        if recognized_commands[command](sys.argv):
            passthrough(options)
        else:
            print_colored('Raptor raised unresolved issues.', color='red')
    else:
        passthrough(options)

if __name__ == '__main__':
    main()
