import pygame
from typing import Union, Tuple, Sequence

_Coordinate = Union[Tuple[float, float], Sequence[float], pygame.Vector2]
_CanBeRect = Union[pygame.Rect, Tuple[int, int, int, int], Tuple[_Coordinate, _Coordinate], Tuple[_Coordinate]]
_FileArg = Union[str, bytes]
_RgbaOutput = Tuple[int, int, int, int]
_ColorValue = Union[pygame.Color, int, str, Tuple[int, int, int], _RgbaOutput]