"""
config.py

Includes general configuration facilities.
"""

import json

def get_config_factory(context):
    """
    get_config_factory(context: { _config: {}, _loaded: boolean }) -> function(filename: str) -> {}
    
    Returns a closed-over instance of the get_config function. Because
    closures are cool.
    """
    def get_config_instance(filename=".raptorconfig"):
        """
        get_config_instance(filename: str) -> boolean

        Upon first execution, reads the configuration file. After
        that, uses the closed-over variable context to return a cached
        version of the config.
        """
        if not context['_loaded']:
            try:
                data = open(filename).read()
            except IOError:
                data = ""

            try:
                context['_config'] = json.loads(data)
            except ValueError:
                context['_config'] = {}
            context['_loaded'] = True
        return context['_config']

    return get_config_instance

get_config = get_config_factory({ '_config': {}, '_loaded': False })
