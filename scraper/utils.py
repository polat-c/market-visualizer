"""
Utilities:
- time conversion
- etc.
"""

from datetime import datetime

def to_string(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')