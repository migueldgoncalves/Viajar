import io
import sys

"""
Utility routines for unit tests
"""

def redirect_output() -> io.StringIO:
    """
    Redirects stdout to be monitorable inside tests

    :return: Object to where stdout is now being redirected
    """
    stdout_redirect: io.StringIO = io.StringIO()
    sys.stdout = stdout_redirect
    return stdout_redirect
