"""
blocklist.py

This file contains the blocklist of JWT tokens. It will be imported by app and logout resource so that the token
can be added to the blocklist when the user logs out.
"""

BLOCKLIST = set()