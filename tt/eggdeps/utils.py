class Options(dict):

    version_numbers = False
    once = False
    terse = False
    cluster = False
    version_specs = False

    def __init__(self, *args, **kwargs):
        self.__dict__ = self
        super(Options, self).__init__(*args, **kwargs)
