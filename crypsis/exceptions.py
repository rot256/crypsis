def essert(cond, exc):
    """
    Like an assert but raises
    the given exceptions on failure.

    Whereas the asserts are used solely for testing,
    this construct is used in "production"
    """
    if not cond:
        raise exc

class InvalidPadding(Exception):
    pass

class NoCandidateFound(Exception):
    pass
