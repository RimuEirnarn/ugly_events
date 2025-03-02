"""Filters"""

import logging


def filter_maker(level):
    """Create a filter for logging based on the level"""
    level = getattr(logging, level)

    def filter_log(record):
        """Filter"""
        return record.levelno < level

    return filter_log
