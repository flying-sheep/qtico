from __future__ import annotations

import os
from typing import TYPE_CHECKING
from warnings import warn

from qtpy.QtGui import QIcon

from .common import PATH_ICON_THEME


if TYPE_CHECKING:
	from collections.abc import Iterable


def theme_warning(*msgs: str) -> None:
	msg = f'NBManager: {" ".join(msgs)} – using builtin theme'
	warn(msg, stacklevel=2)


def install_icon_theme(
	builtin_theme_name: str,
	theme_path: os.PathLike = PATH_ICON_THEME,
	*,
	ignore_varnames: Iterable[str] = ('USE_BUILTIN_ICON_THEME',),
) -> None:
	ignore = {vn: os.environ.get(vn, '') for vn in ignore_varnames}
	forced = [vn for vn, val in ignore.items() if val]
	no_theme = not QIcon.themeName()
	if forced:
		theme_warning(', '.join(forced), set)
		paths = QIcon.themeSearchPaths()
		builtin = paths.pop(paths.index(f':/{theme_path}'))
		# this is always available, but we force its use
		QIcon.setThemeSearchPaths([builtin, *paths])
	elif no_theme:
		theme_warning('no available theme found')

	if forced or no_theme:
		QIcon.setThemeName(builtin_theme_name)
