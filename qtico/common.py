from pathlib import Path
from typing import Union, Optional, Tuple, Iterable, Generator, List


PATH_ICON_THEME = Path('icons')


def k(n: Union[str, int]) -> int:
	return int(n) if n != 'scalable' else 10000


def all_sizes(dir_theme: Path) -> List[str]:
	return sorted((p.name.split('x')[0] for p in dir_theme.iterdir() if p.is_dir()), key=k)


def size_dirs(
	dir_theme: Path,
	sizes: Optional[Iterable[Union[str, int]]]=None,
) -> Generator[Tuple[Union[str, int], Path], None, None]:
	if sizes is None:
		sizes = all_sizes(dir_theme)
	
	for s in sizes:
		n = '{0}x{0}'.format(s) if s != 'scalable' else s
		yield s, dir_theme / n
