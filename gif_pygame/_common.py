import pygame
from importlib.metadata import version as libver
from packaging.version import Version
from os import PathLike

try:
	pygame.IS_CE
	is_ce = True
except AttributeError:
	is_ce = False

if is_ce and Version(libver("pygame-ce")) >= Version("2.5.2"):
	from pygame.typing import Point, RectLike, FileLike, ColorLike
else:
	from typing import Union, Tuple, Sequence

	Point = Union[Tuple[float, float], Sequence[float], pygame.Vector2]
	RectLike = Union[pygame.Rect, pygame.FRect, Tuple[int, int, int, int], Tuple[Point, Point]]
	FileLike = Union[str, bytes, PathLike]
	ColorLike = Union[pygame.Color, int, str, Tuple[int, int, int], Tuple[int, int, int, int]]
