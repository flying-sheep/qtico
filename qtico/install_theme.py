import os
from warnings import warn

from PyQt5.QtGui import QIcon

from .common import PATH_ICON_THEME


def theme_warning(*msgs):
	warn('NBManager: {} – using builtin theme'.format(' '.join(msgs)))


def install_icon_theme(builtin_theme_name, theme_path=PATH_ICON_THEME, *, ignore_varnames=('USE_BUILTIN_ICON_THEME',)):
	ignore = {vn: os.environ.get(vn, '') for vn in ignore_varnames}
	forced = [vn for vn, val in ignore.items() if val]
	no_theme = not QIcon.themeName()
	if forced:
		theme_warning(', '.join(forced), set)
		paths = QIcon.themeSearchPaths()
		builtin = paths.pop(paths.index(':/{}'.format(theme_path)))
		QIcon.setThemeSearchPaths([builtin] + paths)  # this is always available, but we force its use
	elif no_theme:
		theme_warning('no available theme found')
	
	if forced or no_theme:
		QIcon.setThemeName(builtin_theme_name)
