# -*- coding: UTF-8 -*-

"""
allows for easy gif editing
"""

import pygame, warnings

from typing import Union, Tuple, Sequence, Iterable, Optional, List
from importlib.metadata import version as libver
from packaging.version import Version

from ._common import is_ce, Point, ColorLike, RectLike
from gif_pygame.gif_pygame import GIFPygame


def _get_frames(gif: GIFPygame, frames: Union[Iterable[int], None]) -> Tuple[List[pygame.Surface], List[int]]:
	if frames is not None:
		frames = list(frames)

	old_surfs = gif.get_surfaces(frames)
	if not frames:
		frames = list(range(len(gif.frames)))

	return old_surfs, frames


# based on pygame.transform
def flip(gif: GIFPygame, flip_x: bool, flip_y: bool, frames: Optional[Iterable[int]]=None, new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	flip vertically and horizontally

	:param gif: the gif that you want to edit
	:param flip_x: flip horizontally
	:param flip_y: flip vertically
	:param frames: (optional) choose the frames to edit. Leave empty to edit the entire gif
	:param new_gif: (optional) whether to create a new gif with these changes or not
	"""
	old_surfs, frames = _get_frames(gif, frames); new_surfs = []

	for i, surf in enumerate(old_surfs):
		new_surfs.append((pygame.transform.flip(surf, flip_x, flip_y), frames[i]))
	return surfaces(gif, new_surfs, new_gif)

def scale(gif: GIFPygame, size: Point, frames: Optional[Iterable[int]]=None, new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	resize to new resolution

	:param gif: the gif that you want to edit
	:param size: width and height of the new resolution
	:param frames: (optional) choose the frames to edit. Leave empty to edit the entire gif
	:param new_gif: (optional) whether to create a new gif with these changes or not
	"""
	old_surfs, frames = _get_frames(gif, frames); new_surfs = []

	for i, surf in enumerate(old_surfs):
		new_surfs.append((pygame.transform.scale(surf, size), frames[i]))
	return surfaces(gif, new_surfs, new_gif)

def scale_by(gif: GIFPygame, factor: Union[float, Sequence[float]], frames: Optional[Iterable[int]]=None, new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	resize to new resolution, using scalar(s)

	:param gif: the gif that you want to edit
	:param factor: the factor of resizing
	:param frames: (optional) choose the frames to edit. Leave empty to edit the entire gif
	:param new_gif: (optional) whether to create a new gif with these changes or not
	"""
	old_surfs, frames = _get_frames(gif, frames); new_surfs = []

	for i, surf in enumerate(old_surfs):
		new_surfs.append((pygame.transform.scale_by(surf, factor), frames[i]))
	return surfaces(gif, new_surfs, new_gif)

def rotate(gif: GIFPygame, angle: float, frames: Optional[Iterable[int]]=None, new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	rotate the gif

	:param gif: the gif that you want to edit
	:param angle: the rotation angle
	:param frames: (optional) choose the frames to edit. Leave empty to edit the entire gif
	:param new_gif: (optional) whether to create a new gif with these changes or not
	"""
	old_surfs, frames = _get_frames(gif, frames); new_surfs = []

	for i, surf in enumerate(old_surfs):
		new_surfs.append((pygame.transform.rotate(surf, angle), frames[i]))
	return surfaces(gif, new_surfs, new_gif)
	
def rotozoom(gif: GIFPygame, angle: int, scale: float, frames: Optional[Iterable[int]]=None, new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	filtered scale and rotation

	:param gif: the gif that you want to edit
	:param angle: the rotation angle
	:param scale: width and height of the new resolution
	:param frames: (optional) choose the frames to edit. Leave empty to edit the entire gif
	:param new_gif: (optional) whether to create a new gif with these changes or not
	"""
	old_surfs, frames = _get_frames(gif, frames); new_surfs = []

	for i, surf in enumerate(old_surfs):
		new_surfs.append((pygame.transform.rotozoom(surf, angle, scale), frames[i]))
	return surfaces(gif, new_surfs, new_gif)
	
def scale2x(gif: GIFPygame, frames: Optional[Iterable[int]]=None, new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	specialized gif frames doubler

	:param gif: the gif that you want to edit
	:param frames: (optional) choose the frames to edit. Leave empty to edit the entire gif
	:param new_gif: (optional) whether to create a new gif with these changes or not
	"""
	old_surfs, frames = _get_frames(gif, frames); new_surfs = []

	for i, surf in enumerate(old_surfs):
		new_surfs.append((pygame.transform.scale2x(surf), frames[i]))
	return surfaces(gif, new_surfs, new_gif)
	
def smoothscale(gif: GIFPygame, size: Point, frames: Optional[Iterable[int]]=None, new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	scale a gif to an arbitrary size smoothly

	:param gif: the gif that you want to edit
	:param size: width and height of the new size
	:param frames: (optional) choose the frames to edit. Leave empty to edit the entire gif
	:param new_gif: (optional) whether to create a new gif with these changes or not
	"""
	old_surfs, frames = _get_frames(gif, frames); new_surfs = []

	for i, surf in enumerate(old_surfs):
		new_surfs.append((pygame.transform.smoothscale(surf, size), frames[i]))
	return surfaces(gif, new_surfs, new_gif)
	
def smoothscale_by(gif: GIFPygame, factor: Union[float, Sequence[float]], frames: Optional[Iterable[int]]=None, new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	resize to new resolution, using scalar(s)

	:param gif: the gif that you want to edit
	:param factor: the factor of resizing
	:param frames: (optional) choose the frames to edit. Leave empty to edit the entire gif
	:param new_gif: (optional) whether to create a new gif with these changes or not
	"""
	old_surfs, frames = _get_frames(gif, frames); new_surfs = []

	for i, surf in enumerate(old_surfs):
		new_surfs.append((pygame.transform.smoothscale_by(surf, factor), frames[i]))
	return surfaces(gif, new_surfs, new_gif)
	
def chop(gif: GIFPygame, rect: RectLike, frames: Optional[Iterable[int]]=None, new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	Chops a gif to extract a portion of that gif

	:param gif: the gif that you want to edit
	:param rect: the area to be chopped
	:param frames: (optional) choose the frames to edit. Leave empty to edit the entire gif
	:param new_gif: (optional) whether to create a new gif with these changes or not
	"""
	old_surfs, frames = _get_frames(gif, frames); new_surfs = []

	for i, surf in enumerate(old_surfs):
		new_surfs.append((pygame.transform.chop(surf, rect), frames[i]))
	return surfaces(gif, new_surfs, new_gif)

def laplacian(gif: GIFPygame, frames: Optional[Iterable[int]]=None, new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	Finds the edges of each surface in the gif

	:param gif: the gif that you want to edit
	:param frames: (optional) choose the frames to edit. Leave empty to edit the entire gif
	:param new_gif: (optional) whether to create a new gif with these changes or not
	"""
	old_surfs, frames = _get_frames(gif, frames); new_surfs = []

	for i, surf in enumerate(old_surfs):
		new_surfs.append((pygame.transform.laplacian(surf), frames[i]))
	return surfaces(gif, new_surfs, new_gif)

def box_blur(gif: GIFPygame, radius: int, repeat_edged_pixels: bool=True, frames: Optional[Iterable[int]]=None, new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	blur a gif using box blur

	:param gif: the gif that you want to edit
	:param radius: intensity of blurring
	:param repeat_edged_pixels: (optional) whether to repeat edged pixels
	:param frames: (optional) choose the frames to edit. Leave empty to edit the entire gif
	:param new_gif: (optional) whether to create a new gif with these changes or not
	"""
	if not is_ce:
		warnings.warn("This function, gif_pygame.transform.box_blur, will not run because your pygame version is not compatible with this function.\nPlease use pygame-ce for extra speed, better support, and better experience.\npip uninstall pygame\npip install pygame-ce", Warning, 2)
		return
	old_surfs, frames = _get_frames(gif, frames); new_surfs = []

	for i, surf in enumerate(old_surfs):
		new_surfs.append((pygame.transform.box_blur(surf, radius, repeat_edged_pixels), frames[i]))
	return surfaces(gif, new_surfs, new_gif)
	
def gaussian_blur(gif: GIFPygame, radius: int, repeat_edged_pixels: bool=True, frames: Optional[Iterable[int]]=None, new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	blur a surface using gaussian blur (slow)

	:param gif: the gif that you want to edit
	:param radius: intensity of blurring
	:param repeat_edged_pixels: (optional) whether to repeat edged pixels
	:param frames: (optional) choose the frames to edit. Leave empty to edit the entire gif
	:param new_gif: (optional) whether to create a new gif with these changes or not
	"""
	if not is_ce:
		warnings.warn("This function, gif_pygame.transform.gaussian_blur, will not run because your pygame version is not compatible with this function.\nPlease use pygame-ce for extra speed, better support, and better experience.\npip uninstall pygame\npip install pygame-ce", Warning, 2)
		return
	old_surfs, frames = _get_frames(gif, frames); new_surfs = []

	for i, surf in enumerate(old_surfs):
		new_surfs.append((pygame.transform.gaussian_blur(surf, radius, repeat_edged_pixels), frames[i]))
	return surfaces(gif, new_surfs, new_gif)
	
def average_surfaces(gif: GIFPygame, palette_colors: Optional[Union[bool, int]]=1, frames: Optional[Iterable[int]]=None) -> pygame.Surface:
	"""
	Returns a surface with the average colors of the gif

	:param gif: the gif that you want to edit
	:param palette_colors: if `True`, colors are averaged based on a palette
	:param frames: (optional) choose the frames to edit. Leave empty to edit the entire gif
	"""
	
	old_surfs, frames = _get_frames(gif, frames); new_surfs = []

	return pygame.transform.average_surfaces(old_surfs, None, palette_colors)

def invert(gif: GIFPygame, frames: Optional[Iterable[int]]=None, new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	inverts the RGB elements of a gif

	:param gif: the gif that you want to edit
	:param frames: (optional) choose the frames to edit. Leave empty to edit the entire gif
	:param new_gif: (optional) whether to create a new gif with these changes or not
	"""
	if not is_ce:
		warnings.warn("This function, gif_pygame.transform.invert, will not run because your pygame version is not compatible with this function.\nPlease use pygame-ce for extra speed, better support, and better experience.\npip uninstall pygame\npip install pygame-ce", Warning, 2)
		return
	old_surfs, frames = _get_frames(gif, frames); new_surfs = []

	for i, surf in enumerate(old_surfs):
		new_surfs.append((pygame.transform.invert(surf), frames[i]))
	return surfaces(gif, new_surfs, new_gif)
	
def grayscale(gif: GIFPygame, frames: Optional[Iterable[int]]=None, new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	convert a gif to grayscale

	:param gif: the gif that you want to edit
	:param frames: (optional) choose the frames to edit. Leave empty to edit the entire gif
	:param new_gif: (optional) whether to create a new gif with these changes or not
	"""
	old_surfs, frames = _get_frames(gif, frames); new_surfs = []

	for i, surf in enumerate(old_surfs):
		new_surfs.append((pygame.transform.grayscale(surf), frames[i]))
	return surfaces(gif, new_surfs, new_gif)

def solid_overlay(gif: GIFPygame, color: ColorLike, keep_alpha: bool=False, frames: Optional[Iterable[int]]=None, new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	Replaces all non-transparent pixels of every surface in the gif to the provided color

	:param gif: the gif that you want to edit
	:param color: The color that will replace the pixels
	:param keep_alpha: (optional) whether to keep the surface alpha
	:param frames: (optional) choose the frames to edit. Leave empty to edit the entire gif
	:param new_gif: (optional) whether to create a new gif with these changes or not
	"""
	if not is_ce:
		warnings.warn("This function, gif_pygame.transform.solid_overlay, will not run because your pygame version is not compatible with this function.\nPlease use pygame-ce for extra speed, better support, and better experience.\npip uninstall pygame\npip install pygame-ce", Warning, 2)
		return
	elif Version(libver("pygame-ce")) < Version("2.5.2"):
		warnings.warn("This function, gif_pygame.transform.solid_overlay, will not run because your pygame-ce version number is older than 2.5.2\nPlease upgrade pygame-ce.\npip install pygame-ce --upgrade", Warning, 2)
		return
	old_surfs, frames = _get_frames(gif, frames); new_surfs = []
	
	for i, surf in enumerate(old_surfs):
		new_surfs.append((pygame.transform.solid_overlay(surf, color, None, keep_alpha), frames[i]))
	return surfaces(gif, new_surfs, new_gif)

def hsl(gif: GIFPygame, hue: float=0, saturation: float=0, lightness: float=0, frames: Optional[Iterable[int]]=None, new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	Changes the hue, saturation, and lightness of every surface in the gif

	:param gif: the gif that you want to edit
	:param hue: the amount to change the hue
	:param saturation: the amount to change the saturation
	:param lightness: the amount to change the lightness
	:param frames: (optional) choose the frames to edit. Leave empty to edit the entire gif
	:param new_gif: (optional) whether to create a new gif with these changes or not
	"""
	if not is_ce:
		warnings.warn("This function, gif_pygame.transform.hsl, will not run because your pygame version is not compatible with this function.\nPlease use pygame-ce for extra speed, better support, and better experience.\npip uninstall pygame\npip install pygame-ce", Warning, 2)
		return
	elif Version(libver("pygame-ce")) < Version("2.5.0"):
		warnings.warn("This function, gif_pygame.transform.hsl, will not run because your pygame-ce version number is older than 2.5.0\nPlease upgrade pygame-ce.\npip install pygame-ce --upgrade", Warning, 2)
		return

	old_surfs, frames = _get_frames(gif, frames); new_surfs = []
	
	for i, surf in enumerate(old_surfs):
		new_surfs.append((pygame.transform.hsl(surf, hue, saturation, lightness), frames[i]))
	return surfaces(gif, new_surfs, new_gif)


# based on pygame.Surface
def convert(gif: GIFPygame, colorkey: Optional[ColorLike]=None, colorkey_flags: int=0, frames: Optional[Iterable[int]]=None, new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	converts a gif

	:param gif: the gif that you want to convert
	:param colorkey: (optional) the transparent colorkey, leave empty for None
	:param colorkey_flags: (optional) the colorkey flags, leave empty for no flags
	:param frames: (optional) choose the frames where the conversion will take effect. Leave empty to convert the entire gif
	:param new_gif: (optional) whether to create a new gif with these changes or not
	"""
	old_surfs, frames = _get_frames(gif, frames); new_surfs = []

	for i, surf in enumerate(old_surfs):
		surf = surf.convert()
		if colorkey is not None:
			surf.set_colorkey(colorkey, colorkey_flags)
		new_surfs.append((surf, frames[i]))
	return surfaces(gif, new_surfs, new_gif)

def convert_alpha(gif: GIFPygame, frames: Optional[Iterable[int]]=None, new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	converts a gif with alpha

	:param gif: the gif that you want to convert
	:param frames: (optional) choose the frames where the conversion will take effect. Leave empty to convert the entire gif
	:param new_gif: (optional) whether to create a new gif with these changes or not
	"""
	old_surfs, frames = _get_frames(gif, frames); new_surfs = []

	for i, surf in enumerate(old_surfs):
		new_surfs.append((surf.convert_alpha(), frames[i]))
	return surfaces(gif, new_surfs, new_gif)

def alpha(gif: GIFPygame, new_alpha: int, flags: int=0, frames: Optional[Iterable[int]]=None, new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	Replaces the alpha of a frame with a new alpha

	:param gif: the gif that you want to replace its surfaces
	:param new_alphas: A list of the new alphas, inside the list must be another list with the alpha as the first item and the frame index as the second item, must be as follows: `[[alpha1, index1], [alpha2, index2]]`
	:param new_gif: (optional) whether to create a new gif with these changes or not

	if a given frame index cannot be found or a frame is duplicated, a warning will be sent and the frame will be ignored

	:raises IndexError: all of the given frame numbers given aren't an index of the frames list
	"""
	old_surfs, frames = _get_frames(gif, frames)
	if new_gif:
		new_surfs = []

		for i, surf in enumerate(old_surfs):
			new_surf = surf.copy()
			new_surf.set_alpha(new_alpha, flags)
			new_surfs.append((new_surf, frames[i]))

		return surfaces(gif, new_surfs, new_gif)
	else:
		for surf in old_surfs:
			surf.set_alpha(new_alpha, flags)

def alphas(gif: GIFPygame, new_alphas: Iterable[Tuple[int, int]], new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	Replaces the alpha of a frame with a new alpha

	:param gif: the gif that you want to replace its surfaces
	:param new_alphas: A list of the new alphas, inside the list must be another list with the alpha as the first item and the frame index as the second item, must be as follows: `[[alpha1, index1], [alpha2, index2]]`
	:param new_gif: (optional) whether to create a new gif with these changes or not

	if a given frame index cannot be found or a frame is duplicated, a warning will be sent and the frame will be ignored

	:raises IndexError: all of the given frame numbers given aren't an index of the frames list
	"""
	warnings.warn("gif_pygame.transform.alphas deprecated since 1.2.0, use gif_pygame.transform.alpha instead", DeprecationWarning, 2)

	return alpha(gif, new_alphas, 0, None, new_gif)


# for the animation itself
def surfaces(gif: GIFPygame, new_surfaces: Iterable[Tuple[pygame.Surface, int]], new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	Replaces the surface of a frame with a new surface

	:param gif: the gif that you want to replace its surfaces
	:param new_surfaces: A list of the new surfaces, inside the list must be another list with the surface as the first item and the frame index as the second item, must be as follows: `[[surf1, index1], [surf2, index2]]`
	:param new_gif: (optional) whether to create a new gif with these changes or not

	if a given frame index cannot be found or a frame is duplicated, a warning will be sent and the frame will be ignored

	:raises IndexError: all of the given frame numbers given aren't an index of the frames list
	"""
	if new_gif:
		gif = gif.copy()

	duplicated = set()
	n = len(gif.frames)
	failed_indices = 0
	
	for surface, index in new_surfaces:
		if index not in duplicated and 0 <= index < n:
			duplicated.add(index)
			gif.frames[index][0] = surface.copy()
		else:
			failed_indices += 1

	if failed_indices == len(new_surfaces):
		raise IndexError("None of the given frames are in the frames list")

	if new_gif:
		return gif

def durations(gif: GIFPygame, new_durations: Iterable[Tuple[float, int]], new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	Replaces the duration of a frame with a new duration (in seconds)

	:param gif: the gif that you want to replace its surfaces
	:param new_durations: A list of the new durations, inside the list must be another list with the duration as the first item and the frame index as the second item, must be as follows: `[[duration1, index1], [duration2, index2]]`
	:param new_gif: (optional) whether to create a new gif with these changes or not

	if a given frame index cannot be found or a frame is duplicated, a warning will be sent and the frame will be ignored

	:raises IndexError: all of the given frame numbers given aren't an index of the frames list
	"""
	if new_gif:
		gif = gif.copy()

	duplicated = set()
	n = len(gif.frames)
	failed_indices = 0
	
	for duration, index in new_durations:
		if index not in duplicated and 0 <= index < n:
			duplicated.add(index)
			gif.frames[index][1] = duration
		else:
			failed_indices += 1

	if failed_indices == len(new_durations):
		raise IndexError("None of the given frames are in the frames list")

	if new_gif:
		return gif

def frame_data(gif: GIFPygame, new_frame_data: Iterable[Tuple[pygame.Surface, float, int]], new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	Replaces the data of a frame (surface and duration) with a new data

	:param gif: the gif that you want to replace its surfaces
	:param new_frame_data: A list of the new data, inside the list must be another list with the surface as the first item, duration as the second item, and the frame index as the third item, must be as follows: `[[surface1, duration1, index1], [surface2, duration2, index2]]`
	:param new_gif: (optional) whether to create a new gif with these changes or not

	if a given frame index cannot be found or a frame is duplicated, a warning will be sent and the frame will be ignored

	:raises IndexError: all of the given frame numbers given aren't an index of the frames list
	"""
	if new_gif:
		gif = gif.copy()

	duplicated = set()
	n = len(gif.frames)
	failed_indices = 0
	
	for surface, duration, index in new_frame_data:
		if index not in duplicated and 0 <= index < n:
			duplicated.add(index)
			gif.frames[index] = [surface.copy(), duration]
		else:
			failed_indices += 1

	if failed_indices == len(new_frame_data):
		raise IndexError("None of the given frames are in the frames list")

	if new_gif:
		return gif

def datas(gif: GIFPygame, new_frame_data: Iterable[Tuple[pygame.Surface, float, int]], new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	Replaces the data of a frame (surface and duration) with a new data

	:param gif: the gif that you want to replace its surfaces
	:param new_frame_data: A list of the new data, inside the list must be another list with the surface as the first item, duration as the second item, and the frame index as the third item, must be as follows: `[[surface1, duration1, index1], [surface2, duration2, index2]]`
	:param new_gif: (optional) whether to create a new gif with these changes or not

	if a given frame index cannot be found or a frame is duplicated, a warning will be sent and the frame will be ignored

	:raises IndexError: all of the given frame numbers given aren't an index of the frames list
	"""
	warnings.warn("gif_pygame.transform.datas deprecated since 1.2.0, use gif_pygame.transform.frame_data instead", DeprecationWarning, 2)
	return frame_data(gif, new_frame_data, new_gif)

def reverse(gif: GIFPygame, new_gif: bool=False) -> Optional[GIFPygame]:
	"""
	Reverses the animation

	:param gif: the gif that you want to edit
	:param new_gif: (optional) whether to create a new gif with these changes or not
	"""
	if new_gif:
		gif = gif.copy()

	orig_frames = gif.frames.copy()
	for i in range(len(gif.frames)):
		gif.frames[i] = orig_frames[-i-1]

	if new_gif:
		return gif
