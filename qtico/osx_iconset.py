from pathlib import Path
from logging import getLogger

from .common import size_dirs


logger = getLogger(__name__)


iconset_sizes = {16, 32, 128, 256, 512}


def write_iconset(app_name: str, dir_themes: Path, dir_iconset: Path):
	"""Create a OSX-compatible iconset.
	
	:param app_name: Your application’s name. We use the files ``<dir_themes>/hicolor/<s>x<s>/<app_name>.png``.
	:param dir_themes: A directory containing the freedesktop icon theme ``hicolor`` with all OSX-sized icons.
	:param dir_iconset: Directory where the iconset will be written to.
	"""
	logger.info('Creating iconset files %s', dir_iconset / 'icon_?x?[@2x].png')
	dir_iconset.mkdir(parents=True, exist_ok=True)
	for size, size_dir in size_dirs(dir_themes / 'hicolor', iconset_sizes):
		links = [dir_iconset / 'icon_{s}x{s}.png'.format(s=size)]
		if size // 2 in iconset_sizes:
			links += [dir_iconset / 'icon_{h}x{h}@2x.png'.format(h=size // 2)]
		
		target = size_dir / 'apps' / (app_name + '.png')
		for link in links:
			if link.is_symlink():
				link.unlink()
			link.symlink_to('..' / target)
