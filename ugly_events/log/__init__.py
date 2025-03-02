# system/log/__init__.py
"""Logging package initialization"""
from .filters import filter_maker # pylint: disable=import-error
from .logger import debug, info, warning, error, critical, system

__all__ = ['debug', 'info', 'warning', 'error', 'critical', 'system', 'filter_maker']
