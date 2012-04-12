import json

_loaded = False
_config = {}
def get_config(filename='.raptorconfig'):
    global _loaded, _config

    if not _loaded:
        try:
            data = open(filename).read()
        except IOError:
            data = ""

        try:
            _config = json.loads(data)
        except ValueError:
            _config = {}
        _loaded = True
    return _config
