import os
import sys


def get_app_directory():
    """Return the directory that contains the application.
    This is the directory of the .py file in most cases, but is the directory
    of the .exe file in the case of py2exe.
    """
    import imp

    if (hasattr(sys, "frozen") # new py2exe
           or hasattr(sys, "importers") # old py2exe
           or imp.is_frozen("__main__")): # tools/freeze
        return os.path.abspath(os.path.dirname(sys.executable))
    else:
        import __main__
        if hasattr(__main__, '__file__'):
            return os.path.abspath(os.path.dirname(__main__.__file__))
        else:
            return os.path.abspath(os.path.dirname(sys.argv[0]))
