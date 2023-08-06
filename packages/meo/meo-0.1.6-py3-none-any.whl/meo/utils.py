"""
    awesome functions
"""
import os

def script_path(__file__):
    """return script real path in disk."""
    return os.path.split(os.path.realpath(__file__))[0]

class ScriptPath:
    def __init__(self, __file__) -> None:
        self.path = script_path(__file__)
    
    def join(self, *paths):
        self.path = os.path.join(self.path, *paths)
        return self
