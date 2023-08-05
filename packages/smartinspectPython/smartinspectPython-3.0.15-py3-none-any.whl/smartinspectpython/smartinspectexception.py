"""
Module: smartinspectexception.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""


# external package imports.
# none

# our package imports.
# none

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class SmartInspectException(Exception):
    """
    Used internally to report any kind of error.

    This is the base class for several exceptions which are mainly
    used for internal error reporting. However, it can be useful
    to have a look at its derived classes, LoadConnectionsException
    and ProtocolException, which provide additional information
    about occurred errors besides the normal exception message.

    This can be useful if you need to obtain more information about
    a particular error in the SmartInspect.Error event.
    """
    def __init__(self, message, *args, **kwargs) -> None:
        """
        Initializes a new instance of the class.

        Args:
            message (object):
                The exception message.
        """

        # initialize base class.
        super(SmartInspectException, self).__init__(message, *args, **kwargs)
