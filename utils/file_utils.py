"""
File path utility functions.

This module provides helper functions for resolving and manipulating file paths.
"""
import os


def resolve_path(p, base_dir=None):
    """
    Resolve a relative path to an absolute path with quotes.

    Args:
        p: Path to resolve (relative or absolute)
        base_dir: Base directory to resolve from (defaults to script directory)

    Returns:
        Absolute path wrapped in quotes
    """
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up two levels since we're in utils/file_utils.py
        base_dir = os.path.dirname(os.path.dirname(base_dir))

    norm_path = os.path.normpath(os.path.join(base_dir, p))
    return f'"{norm_path}"'


def resolve_path_without_quotes(p, base_dir=None):
    """
    Resolve a relative path to an absolute path without quotes.

    Args:
        p: Path to resolve (relative or absolute)
        base_dir: Base directory to resolve from (defaults to script directory)

    Returns:
        Absolute path without quotes
    """
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up two levels since we're in utils/file_utils.py
        base_dir = os.path.dirname(os.path.dirname(base_dir))

    norm_path = os.path.normpath(os.path.join(base_dir, p))
    return norm_path
