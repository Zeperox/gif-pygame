# -*- coding: UTF-8 -*-

"""
allows for easy gif tranformation
"""

import pygame, warnings

from typing import Union, Tuple, Sequence, Iterable, Optional
from gif_pygame.gif_pygame import GIFPygame, is_ce

from ._common import _Coordinate, _ColorValue


def flip(gif: GIFPygame, flip_x: bool, flip_y: bool, frames: Optional[Iterable[int]]=[]):
    """
    flip vertically and horizontally

    :param gif: the gif that you want to tranform
    :param flip_x: flip horizontally
    :param flip_y: flip vertically
    :param frames: (optional) choose the frames where the transformation will take affect. Leave empty to transform the entire gif
    """
    old_surfs = gif.get_surfaces(frames)
    if not frames:
        frames = [i for i in range(len(gif.frames))]
    new_surfs = []

    for i, surf in enumerate(old_surfs):
        new_surfs.append((pygame.transform.flip(surf, flip_x, flip_y), frames[i]))
    surfaces(gif, new_surfs)

def scale(gif: GIFPygame, size: _Coordinate, frames: Optional[Iterable[int]]=[]):
    """
    resize to new resolution

    :param gif: the gif that you want to tranform
    :param size: width and height of the new resolution
    :param frames: (optional) choose the frames where the transformation will take affect. Leave empty to transform the entire gif
    """
    old_surfs = gif.get_surfaces(frames)
    if not frames:
        frames = [i for i in range(len(gif.frames))]
    new_surfs = []

    for i, surf in enumerate(old_surfs):
        new_surfs.append((pygame.transform.scale(surf, size), frames[i]))
    surfaces(gif, new_surfs)

def scale_by(gif: GIFPygame, factor: Union[float, Sequence[float]], frames: Optional[Iterable[int]]=[]):
    """
    resize to new resolution, using scalar(s)

    :param gif: the gif that you want to tranform
    :param factor: the factor of resizing
    :param frames: (optional) choose the frames where the transformation will take affect. Leave empty to transform the entire gif
    """
    old_surfs = gif.get_surfaces(frames)
    if not frames:
        frames = [i for i in range(len(gif.frames))]
    new_surfs = []

    for i, surf in enumerate(old_surfs):
        new_surfs.append((pygame.transform.scale_by(surf, factor), frames[i]))
    surfaces(gif, new_surfs)

def rotate(gif: GIFPygame, angle: float, frames: Optional[Iterable[int]]=[]):
    """
    rotate the gif

    :param gif: the gif that you want to tranform
    :param angle: the rotation angle
    :param frames: (optional) choose the frames where the transformation will take affect. Leave empty to transform the entire gif
    """
    old_surfs = gif.get_surfaces(frames)
    if not frames:
        frames = [i for i in range(len(gif.frames))]
    new_surfs = []

    for i, surf in enumerate(old_surfs):
        new_surfs.append((pygame.transform.rotate(surf, angle), frames[i]))
    surfaces(gif, new_surfs)
    
def rotozoom(gif: GIFPygame, angle: int, scale: float, frames: Optional[Iterable[int]]=[]):
    """
    filtered scale and rotation

    :param gif: the gif that you want to tranform
    :param angle: the rotation angle
    :param scale: width and height of the new resolution
    :param frames: (optional) choose the frames where the transformation will take affect. Leave empty to transform the entire gif
    """
    old_surfs = gif.get_surfaces(frames)
    if not frames:
        frames = [i for i in range(len(gif.frames))]
    new_surfs = []

    for i, surf in enumerate(old_surfs):
        new_surfs.append((pygame.transform.rotozoom(surf, angle, scale), frames[i]))
    surfaces(gif, new_surfs)
    
def scale2x(gif: GIFPygame, frames: Optional[Iterable[int]]=[]):
    """
    specialized gif frames doubler

    :param gif: the gif that you want to tranform
    :param frames: (optional) choose the frames where the transformation will take affect. Leave empty to transform the entire gif
    """
    old_surfs = gif.get_surfaces(frames)
    if not frames:
        frames = [i for i in range(len(gif.frames))]
    new_surfs = []

    for i, surf in enumerate(old_surfs):
        new_surfs.append((pygame.transform.scale2x(surf), frames[i]))
    surfaces(gif, new_surfs)
    
def smoothscale(gif: GIFPygame, size: _Coordinate, frames: Optional[Iterable[int]]=[]):
    """
    scale a gif to an arbitrary size smoothly

    :param gif: the gif that you want to tranform
    :param size: width and height of the new size
    :param frames: (optional) choose the frames where the transformation will take affect. Leave empty to transform the entire gif
    """
    old_surfs = gif.get_surfaces(frames)
    if not frames:
        frames = [i for i in range(len(gif.frames))]
    new_surfs = []

    for i, surf in enumerate(old_surfs):
        new_surfs.append((pygame.transform.smoothscale(surf, size), frames[i]))
    surfaces(gif, new_surfs)
    
def smoothscale_by(gif: GIFPygame, factor: Union[float, Sequence[float]], frames: Optional[Iterable[int]]=[]):
    """
    resize to new resolution, using scalar(s)

    :param gif: the gif that you want to tranform
    :param factor: the factor of resizing
    :param frames: (optional) choose the frames where the transformation will take affect. Leave empty to transform the entire gif
    """
    old_surfs = gif.get_surfaces(frames)
    if not frames:
        frames = [i for i in range(len(gif.frames))]
    new_surfs = []

    for i, surf in enumerate(old_surfs):
        new_surfs.append((pygame.transform.smoothscale_by(surf, factor), frames[i]))
    surfaces(gif, new_surfs)
    
def box_blur(gif: GIFPygame, radius: int, repeat_edged_pixels: Optional[bool]=True, frames: Optional[Iterable[int]]=[]):
    """
    blur a gif using box blur

    :param gif: the gif that you want to tranform
    :param radius: intensity of blurring
    :repeat_edged_pixels: (optional) I've got no clue
    :param frames: (optional) choose the frames where the transformation will take affect. Leave empty to transform the entire gif
    """
    if not is_ce:
        warnings.warn("This function, gif_pygame.transform.box_blur, won't run because your pygame version is not compatible with this function.\nPlease use pygame-ce for extra speed, better support, and better experience.\npip uninstall pygame\npip install pygame-ce", Warning, 2)
        return
    old_surfs = gif.get_surfaces(frames)
    if not frames:
        frames = [i for i in range(len(gif.frames))]
    new_surfs = []

    for i, surf in enumerate(old_surfs):
        new_surfs.append((pygame.transform.box_blur(surf, radius, repeat_edged_pixels), frames[i]))
    surfaces(gif, new_surfs)
    
def gaussian_blur(gif: GIFPygame, radius: int, repeat_edged_pixels: Optional[bool]=True, frames: Optional[Iterable[int]]=[]):
    """
    blur a surface using gaussian blur (slow)

    :param gif: the gif that you want to tranform
    :param radius: intensity of blurring
    :repeat_edged_pixels: (optional) I've got no clue
    :param frames: (optional) choose the frames where the transformation will take affect. Leave empty to transform the entire gif
    """
    if not is_ce:
        warnings.warn("This function, gif_pygame.transform.box_blur, won't run because your pygame version is not compatible with this function.\nPlease use pygame-ce for extra speed, better support, and better experience.\npip uninstall pygame\npip install pygame-ce", Warning, 2)
        return
    old_surfs = gif.get_surfaces(frames)
    if not frames:
        frames = [i for i in range(len(gif.frames))]
    new_surfs = []

    for i, surf in enumerate(old_surfs):
        new_surfs.append((pygame.transform.gaussian_blur(surf, radius, repeat_edged_pixels), frames[i]))
    surfaces(gif, new_surfs)
    
def invert(gif: GIFPygame, frames: Optional[Iterable[int]]=[]):
    """
    inverts the RGB elements of a gif

    :param gif: the gif that you want to tranform
    :param frames: (optional) choose the frames where the transformation will take affect. Leave empty to transform the entire gif
    """
    if not is_ce:
        warnings.warn("This function, gif_pygame.transform.box_blur, won't run because your pygame version is not compatible with this function.\nPlease use pygame-ce for extra speed, better support, and better experience.\npip uninstall pygame\npip install pygame-ce", Warning, 2)
        return
    old_surfs = gif.get_surfaces(frames)
    if not frames:
        frames = [i for i in range(len(gif.frames))]
    new_surfs = []

    for i, surf in enumerate(old_surfs):
        new_surfs.append((pygame.transform.invert(surf), frames[i]))
    surfaces(gif, new_surfs)
    
def grayscale(gif: GIFPygame, frames: Optional[Iterable[int]]=[]):
    """
    grayscale a gif

    :param gif: the gif that you want to tranform
    :param frames: (optional) choose the frames where the transformation will take affect. Leave empty to transform the entire gif
    """
    old_surfs = gif.get_surfaces(frames)
    if not frames:
        frames = [i for i in range(len(gif.frames))]
    new_surfs = []

    for i, surf in enumerate(old_surfs):
        new_surfs.append((pygame.transform.grayscale(surf), frames[i]))
    surfaces(gif, new_surfs)


def convert(gif: GIFPygame, colorkey: Optional[Union[None, _ColorValue]]=None, colorkey_flags: Optional[int]=0, frames: Optional[Iterable[int]]=[]):
    """
    converts a gif

    :param gif: the gif that you want to convert
    :param colorkey: (optional) the transparent colorkey, leave empty for None
    :param colorkey_flags: (optional) the colorkey flags, leave empty for no flags
    :param frames: (optional) choose the frames where the conversion will take affect. Leave empty to convert the entire gif
    """
    old_surfs = gif.get_surfaces(frames)
    if not frames:
        frames = [i for i in range(len(gif.frames))]
    new_surfs = []

    for i, surf in enumerate(old_surfs):
        surf = surf.convert()
        if colorkey:
            surf.set_colorkey(colorkey, colorkey_flags)
        new_surfs.append((surf, frames[i]))
    surfaces(gif, new_surfs)

def convert_alpha(gif: GIFPygame, frames: Optional[Iterable[int]]=[]):
    """
    converts a gif with alpha

    :param gif: the gif that you want to convert
    :param frames: (optional) choose the frames where the conversion will take affect. Leave empty to convert the entire gif
    """
    old_surfs = gif.get_surfaces(frames)
    if not frames:
        frames = [i for i in range(len(gif.frames))]
    new_surfs = []

    for i, surf in enumerate(old_surfs):
        new_surfs.append((surf.convert_alpha(), frames[i]))
    surfaces(gif, new_surfs)

def surfaces(gif: GIFPygame, surfaces: Iterable[Tuple[pygame.Surface, int]]) -> None:
    """
    Replaces the surface of a frame with a new surface

    :param gif: the gif that you want to replace its surfaces
    :param surfaces: A list of the new surfaces, inside the list must be another list with the surface as the first item and the frame index as the second item, must be as follows: `[[surf1, index1], [surf2, index2]]`
    
    if a given frame index cannot be found or a frame is duplicated, a warning will be sent and the frame will be ignored

    :raises IndexError: all of the given frame numbers given aren't an index of the frames list
    """
    failed_frames = []
    duplicated_frames = []
    successful_frames = []

    for index, surface in enumerate(surfaces):
        try:
            gif.frames[surface[1]]
        except:
            failed_frames.append((index, surface[1]))
            continue

        if surface in successful_frames:
            duplicated_frames.append((index, surface[1]))
            continue

        else:
            successful_frames.append(surface)
            gif.frames[surface[1]][0] = surface[0]

    if len(successful_frames) == 0:
        raise IndexError("None of the given frames are in the frames list")
    else:
        if len(failed_frames):
            failed_str = "There were some failed frames, they were:\n"
            for failed_frame in failed_frames:
                failed_str += f"Frame Number: {failed_frame[1]}, Index: {failed_frame[0]}"
            print(failed_str)
        if len(duplicated_frames):
            duplicated_str = "There were some duplicated frames, they were:\n"
            for duplicated_frame in duplicated_frames:
                duplicated_str += f"Frame Number: {duplicated_frame[1]}, Index: {duplicated_frame[0]}"
            print(duplicated_str)

def durations(gif: GIFPygame, durations: Iterable[Tuple[float, int]]) -> None:
    """
    Replaces the duration of a frame with a new duration (in seconds)

    :param gif: the gif that you want to replace its surfaces
    :param durations: A list of the new durations, inside the list must be another list with the duration as the first item and the frame index as the second item, must be as follows: `[[duration1, index1], [duration2, index2]]`
    
    if a given frame index cannot be found or a frame is duplicated, a warning will be sent and the frame will be ignored

    :raises IndexError: all of the given frame numbers given aren't an index of the frames list
    """
    failed_frames = []
    duplicated_frames = []
    successful_frames = []

    for index, duration in enumerate(durations):
        try:
            gif.frames[duration[1]]
        except:
            failed_frames.append((index, duration[1]))
            continue

        if duration in successful_frames:
            duplicated_frames.append((index, duration[1]))
            continue

        else:
            successful_frames.append(duration)
            gif.frames[duration[1]][1] = duration[0]

    if len(successful_frames) == 0:
        raise IndexError("None of the given frames are in the frames list")
    else:
        if len(failed_frames):
            failed_str = "There were some failed frames, they were:\n"
            for failed_frame in failed_frames:
                failed_str += f"Frame Number: {failed_frame[1]}, Index: {failed_frame[0]}"
            print(failed_str)
        if len(duplicated_frames):
            duplicated_str = "There were some duplicated frames, they were:\n"
            for duplicated_frame in duplicated_frames:
                duplicated_str += f"Frame Number: {duplicated_frame[1]}, Index: {duplicated_frame[0]}"
            print(duplicated_str)

def datas(gif: GIFPygame, datas: Iterable[Tuple[pygame.Surface, float, int]]) -> None:
    """
    Replaces the data of a frame (surface and duration) with a new data

    :param gif: the gif that you want to replace its surfaces
    :param datas: A list of the new data, inside the list must be another list with the surface as the first item, duration as the second item, and the frame index as the second item, must be as follows: `[[surface1, duration1, index1], [surface2, duration2, index2]]`
    
    if a given frame index cannot be found or a frame is duplicated, a warning will be sent and the frame will be ignored

    :raises IndexError: all of the given frame numbers given aren't an index of the frames list
    """
    failed_frames = []
    duplicated_frames = []
    successful_frames = []

    for index, data in enumerate(datas):
        try:
            gif.frames[data[2]]
        except:
            failed_frames.append((index, data[2]))
            continue

        if data in successful_frames:
            duplicated_frames.append((index, data[2]))
            continue

        else:
            successful_frames.append(data)
            gif.frames[data[2]][0] = data[0]
            gif.frames[data[2]][1] = data[1]

    if len(successful_frames) == 0:
        raise IndexError("None of the given frames are in the frames list")
    else:
        if len(failed_frames):
            failed_str = "There were some failed frames, they were:\n"
            for failed_frame in failed_frames:
                failed_str += f"Frame Number: {failed_frame[1]}, Index: {failed_frame[0]}"
            print(failed_str)
        if len(duplicated_frames):
            duplicated_str = "There were some duplicated frames, they were:\n"
            for duplicated_frame in duplicated_frames:
                duplicated_str += f"Frame Number: {duplicated_frame[1]}, Index: {duplicated_frame[0]}"
            print(duplicated_str)

def alphas(gif: GIFPygame, alphas: Iterable[Tuple[int, int]]) -> None:
    """
    Replaces the alpha of a frame with a new alpha

    :param gif: the gif that you want to replace its surfaces
    :param alphas: A list of the new alphas, inside the list must be another list with the alpha as the first item and the frame index as the second item, must be as follows: `[[alpha1, index1], [alpha2, index2]]`
    
    if a given frame index cannot be found or a frame is duplicated, a warning will be sent and the frame will be ignored

    :raises IndexError: all of the given frame numbers given aren't an index of the frames list
    """
    failed_frames = []
    duplicated_frames = []
    successful_frames = []

    for index, alpha in enumerate(alphas):
        try:
            gif.frames[alpha[1]]
        except:
            failed_frames.append((index, alpha[1]))
            continue

        if alpha in successful_frames:
            duplicated_frames.append((index, alpha[1]))
            continue

        else:
            successful_frames.append(alpha)
            gif.frames[alpha[1]][0].set_alpha(alpha[0])

    if len(successful_frames) == 0:
        raise IndexError("None of the given frames are in the frames list")
    else:
        if len(failed_frames):
            failed_str = "There were some failed frames, they were:\n"
            for failed_frame in failed_frames:
                failed_str += f"Frame Number: {failed_frame[1]}, Index: {failed_frame[0]}"
            print(failed_str)
        if len(duplicated_frames):
            duplicated_str = "There were some duplicated frames, they were:\n"
            for duplicated_frame in duplicated_frames:
                duplicated_str += f"Frame Number: {duplicated_frame[1]}, Index: {duplicated_frame[0]}"
            print(duplicated_str)
