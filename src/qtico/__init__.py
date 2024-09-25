"""Tools for using cross-platform Qt icon themes."""

from __future__ import annotations

from importlib.metadata import version

from .common import PATH_ICON_THEME
from .install_theme import install_icon_theme
from .osx_iconset import write_iconset
from .qrc_compile import write_resources
from .theme_index import write_theme_indices


__all__ = [
	'PATH_ICON_THEME',
	'write_theme_indices',
	'write_resources',
	'write_iconset',
	'install_icon_theme',
]
__version__ = version('qtico')
