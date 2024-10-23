from __future__ import annotations

from logging import getLogger
from subprocess import run
from typing import TYPE_CHECKING
from warnings import warn

from .common import PATH_ICON_THEME, size_dirs


if TYPE_CHECKING:
	from pathlib import Path

logger = getLogger(__name__)

template_qrc = """\
<RCC>
	<qresource>
{}
	</qresource>
</RCC>
""".format

template_qrc_file = '\t\t<file>{}</file>'.format


def warn_suffix(path: Path, suffix: str) -> None:
	if path.suffix != suffix:
		msg = f'path {path!r} does not end with the suffix {suffix!r}'
		warn(msg, stacklevel=2)


def ensure_is_file(path: Path, creator: str) -> None:
	if not path.is_file():
		msg = f'Could not find {path}. Consider creating it via {creator}'
		raise FileNotFoundError(msg)


def process_resource_files(paths: Path, out: Path) -> None:
	run(['rcc', '-g', 'python', *paths, '-o', out], check=True)


def write_resources(
	path_qrc: Path,
	path_rcpy: Path,
	dir_themes: Path | None = None,
) -> None:
	warn_suffix(path_qrc, '.qrc')
	warn_suffix(path_rcpy, '.py')

	dir_project = path_qrc.parent
	if dir_themes is None:
		dir_themes = dir_project / PATH_ICON_THEME
	if not dir_themes.is_absolute():
		dir_themes = dir_project / dir_themes

	if dir_project not in dir_themes.parents:
		msg = 'path_qrc needs to be in a parent directory of dir_themes'
		raise ValueError(msg)

	files = []
	for dir_theme in dir_themes.iterdir():
		path_index = dir_theme / 'index.theme'
		from .theme_index import write_theme_indices

		ensure_is_file(path_index, write_theme_indices.__name__)
		files.append(template_qrc_file(path_index.relative_to(dir_project)))
		for _, size_dir in size_dirs(dir_theme):
			for sec in size_dir.iterdir():
				for icon in sec.iterdir():
					files.append(template_qrc_file(icon.relative_to(dir_project)))  # noqa: PERF401

	logger.info('Creating QRC file: %s', path_qrc)
	path_qrc.parent.mkdir(parents=True, exist_ok=True)
	with path_qrc.open('wt', encoding='utf-8') as qrc:
		qrc.write(template_qrc('\n'.join(files)))

	logger.info('Creating RC.py file %s from %s', path_rcpy, path_qrc)
	path_rcpy.parent.mkdir(parents=True, exist_ok=True)
	process_resource_files(path_qrc, out=path_rcpy)


write_resources.__doc__ = f"""\
Create a ``.qrc`` and a ``_rc.py`` file for your project containing all themes’ icons.

Make sure your icon themes have an index.theme (We have a function for creating them!).

:param path_qrc: A path to a ``.qrc`` file to write.
    Usually directly in the project directory.
:param path_rcpy: A path to a compiled python file containing the resources.
    Usually ``*_rc.py``.
:param dir_themes: A directory containing freedesktop icon themes
    with the necessary icons for your application.
    The default is ``{PATH_ICON_THEME}`` next to ``path_qrc``.
	Needs to be next to or below ``path_qrc``.
"""
