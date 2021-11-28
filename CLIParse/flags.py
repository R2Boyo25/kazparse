"""
Contains Flags class
"""

class Flags:
    "Class that is used to give the values of flags to a command"

    def __init__(self, flags : dict):
        self._values = flags
    
    def __getattr__(self, attr):
        return self._values[attr]
    
    def __getitem__(self, item):
        return self._values[item]
    
    def __str__(self):
        return str(self._values)