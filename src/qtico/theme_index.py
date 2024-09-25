from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from .common import PATH_ICON_THEME, size_dirs
from .install_theme import install_icon_theme

# just for refactoring names
from .qrc_compile import write_resources


if TYPE_CHECKING:
	from pathlib import Path


logger = getLogger(__name__)


contexts = dict(apps='Applications', mimetypes='MimeTypes', actions='Actions')


template_index = """\
[Icon Theme]
Name={name}
Inherits=default
Directories={dirs}

{sections}
""".format

template_section = """\
[{s}x{s}/{sec}]
Size={s}
Type=Fixed
Context={ctx}\
""".format

template_scalable = """\
[{s}/{sec}]
Size=512
Type=Scalable
MinSize=1
MaxSize=1024
Context={ctx}\
""".format


def write_theme_indices(dir_themes: Path) -> None:
	dirs = []
	sections = []

	for dir_theme in dir_themes.iterdir():
		for size, size_dir in size_dirs(dir_theme):
			for sec in size_dir.iterdir():
				dirs.append(str(sec.relative_to(dir_theme)))
				template = template_scalable if size == 'scalable' else template_section
				sections.append(
					template(
						s=size,
						sec=sec.name,
						ctx=contexts[sec.name],
					),
				)

		index_theme = dir_theme / 'index.theme'
		logger.info('Creating theme index file: %s', index_theme)
		with index_theme.open('wt', encoding='utf-8') as index:
			index.write(
				template_index(
					name=dir_theme.name.title(),
					dirs=','.join(dirs),
					sections='\n\n'.join(sections),
				),
			)


write_theme_indices.__doc__ = f"""\
Create index.theme files for all icon themes in the directory.

If you use the directory name ``{PATH_ICON_THEME}``,
you can use ``{write_resources.__name__}``
and ``{install_icon_theme.__name__}`` without specifying this.

:param dir_themes: A directory containing freedesktop-compatible icon themes
(without index.theme).
"""
