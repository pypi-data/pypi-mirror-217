

class ReadOnlyViewError(Exception):
    """
    Models that query Views are read-only, this will be raised if a mutation is attempted.
    """
    pass

