# -*- coding: utf-8 -*-
"""
Navigator Data-Integration.

Tool for execution of Tasks.
"""
import asyncio
import uvloop
from .version import (
    __title__, __description__, __version__, __author__, __author_email__
)

def version():
    """version.
    Returns:
        str: current version of Navigator flowtask.
    """
    return __version__
