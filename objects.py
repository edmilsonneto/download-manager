from blessings import Terminal


class Writer(object):

    def __init__(self, location):
        self.location = location

    def write(self, string):
        term = Terminal()

        with term.location(*self.location):
            print(string)
