from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING


if TYPE_CHECKING:
	from collections.abc import Generator, Iterable


PATH_ICON_THEME = Path('icons')


def k(n: str | int) -> int:
	return int(n) if n != 'scalable' else 10000


def all_sizes(dir_theme: Path) -> list[str]:
	return sorted(
		(p.name.split('x')[0] for p in dir_theme.iterdir() if p.is_dir()),
		key=k,
	)


def size_dirs(
	dir_theme: Path,
	sizes: Iterable[str | int] | None = None,
) -> Generator[tuple[str | int, Path], None, None]:
	if sizes is None:
		sizes = all_sizes(dir_theme)

	for s in sizes:
		n = f'{s}x{s}' if s != 'scalable' else s
		yield s, dir_theme / n
