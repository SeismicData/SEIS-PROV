if __name__ == "__main__":
    import inspect
    import os
    import pytest
    import sys
    PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    print(PATH)

    sys.exit(pytest.main(PATH))
