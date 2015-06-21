

class ProgramException(Exception):

    def __init__(self, type, message=None):
        self.type = type
        self.message = message
        super(ProgramException, self).__init__(type, message)


class ExceptionDefinition(object):

    def __init__(self, type):
        self.type = type

    def execute(self, env):
        env[self.type] = self
