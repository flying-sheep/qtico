"""Tools for using cross-platform Qt icon themes.
"""

from .common import PATH_ICON_THEME
from .theme_index import write_theme_indices
from .qrc_compile import write_resources
from .osx_iconset import write_iconset
from .install_theme import install_icon_theme

__version__ = '0.1'
