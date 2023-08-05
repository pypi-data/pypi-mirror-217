"""
Module: const.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  
| 2023/06/30 | 3.0.15.0    | Changed 'Development Status' to '5 - Production/Stable', and uploaded to Pypi.org site.

</details>
"""

# our package imports.
from .color import Color

# constants are placed in this file if they are used across multiple files.
# the only exception to this is for the VERSION constant, which is placed here for convenience.

VERSION:str = "3.0.15"
""" 
Current version of the SmartInspect Python3 Library. 
"""


# Text file related constants:

TEXTFILE_PATTERN_DEFAULT:str = "[%timestamp%] %level%: %title%"
""" 
Default value assigned to a Pattern property, which controls how lines are formatted in text log files. 

Value: 
    `"[%timestamp%] %level%: %title%"`
"""

TEXTFILE_INDENT_DEFAULT:bool = False
""" 
Default value assigned to a Indent property, which controls how lines are indented in text log files. 

Value: 
    False
"""

TEXTFILE_HEADER_BOM = bytearray([0xEF, 0xBB, 0xBF])
"""
Standard UTF-8 Byte Order Mark (BOM) that is written to a file stream to identify a log file as text in UTF-8 encoding.

Value: 
    `[0xEF, 0xBB, 0xBF]`
"""


# SmartInspect Console server related constants:

CLIENT_BANNER:str = "SmartInspect Python Library v" + VERSION + " ({0})\r\n"
"""
Our (client) banner sent to a SmartInspect Console server, which will be added to the console connections log.
This identifies what clients are connecting to the SI Console server.

Value: 
    `"SmartInspect Python3 Library vN.NN \n"`
"""

SERVER_BANNER_ERROR:str = "Could not read server banner correctly: Connection has been closed unexpectedly!"
"""
Indicates that the SmartInspect Console server unexpectedly closed the connection to our client.

Value: 
    `"Could not read server banner correctly: Connection has been closed unexpectedly!"`
"""


# Color-related constants:

DEFAULT_COLOR_VALUE:int = 16777215  # A=0x00, R=0xFF, G=0xFF, B=0xFF (white, transparent)
""" 
Default color integer value that represents 'White (transparent)'.

Value: 
    16777215 (0x00FFFFFF in ARGB format).
"""

DEFAULT_COLOR_OBJECT:Color = Color(DEFAULT_COLOR_VALUE)
""" 
Default color Color object that represents 'White (transparent)'.
"""


# Miscellaneous constants:

UNKNOWN_VALUE:str = "<unknown>"
"""
Indicates if an event argument value is unknown for event argument objects that are displayed as a string.

Value: 
    `"<unknown>"`
"""

