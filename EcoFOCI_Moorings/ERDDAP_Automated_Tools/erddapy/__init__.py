"""
Easier access to scientific data
"""

from erddapy.erddapy import ERDDAP, servers


__all__ = ["ERDDAP", "servers"]

try:
    from ._version import __version__
except ImportError:
    __version__ = "unknown"
