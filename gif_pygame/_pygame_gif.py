# -*- coding: UTF-8 -*-

"""
A animated image loader for Pygame
~~~~~~~~~~~~~~~~~~~~~~~~

A tool to make loading animated image files in pygame easier

    >>> # loading
    >>> import PygameGIF
    >>> loaded_gif = PygameGIF.load("path.gif") # Loads the .gif file

    >>> # rendering
    >>> loaded_gif.render(surface, (x, y)) # Renders and animates the animated image. THIS FUNCTION SHOULD NOT BE USED WITH `surface.blit()`
    >>> # or
    >>> surface.blit(loaded_gif.blit_ready(), (x, y)) # Animates the animated image and returns the current frame. Unlike `gif.render()`, this can be used with `surface.blit()`
"""

import pygame, time, warnings

from PIL import Image
from typing import Union, Tuple, Sequence, List, SupportsIndex, Iterable, Optional

_Coordinate = Union[Tuple[float, float], Sequence[float], pygame.Vector2]
_CanBeRect = Union[pygame.Rect, Tuple[int, int, int, int], Tuple[_Coordinate, _Coordinate], Tuple[_Coordinate]]
_FileArg = Union[str, bytes]
_RgbaOutput = Tuple[int, int, int, int]
_ColorValue = Union[pygame.Color, int, str, Tuple[int, int, int], _RgbaOutput]

class PygameGIF:
    """
    The class responsible for handling all of the .gif file functions
    """
    def __init__(self, filepath: _FileArg) -> None:
        """
        Does the same thing as `PygameGIF.load()`, so why not use that?

        :param filepath: The path of the .gif file that you want to load

        :raises TypeError: if the `filepath` is not a .gif file
        """
        self.filepath = filepath
        
        self.gif = Image.open(filepath)

        self.frames = []
        for frame in range(self.gif.n_frames):
            self.gif.seek(frame)
            if frame == 0:
                if "duration" in self.gif.info:
                    self.frames.append([pygame.image.load(filepath), self.gif.info["duration"]*.001])
                else:
                    self.frames.append([pygame.image.load(filepath), 1])
            else:
                self.frames.append([pygame.image.fromstring(self.gif.tobytes(), self.gif.size, self.gif.mode), self.gif.info["duration"]*.001])
        
        self.gif.close()
        self.frame = 0
        self.frame_time = 0
        self.paused_time = 0
        self.paused = False

    
    def _animate(self):
        if self.frame_time == 0:
            self.frame_time = time.time()

        if time.time()-self.frame_time >= self.frames[self.frame][1] and not self.paused:
            self.frame = self.frame + 1 if self.frame < self.gif.n_frames-1 else 0
            self.frame_time = time.time()

    def _grab_frame(self, select_frame, first_frame, last_frame):
        if select_frame is not None:
            selected_frames = [self.frames[select_frame]]
        else:
            if first_frame is not None and last_frame is not None:
                selected_frames = self.frames[first_frame:last_frame]
            elif first_frame is not None and not last_frame:
                selected_frames = self.frames[first_frame:]
            elif not first_frame and last_frame is not None:
                selected_frames = self.frames[:last_frame]
            elif (not first_frame and not last_frame) or (0 < last_frame < first_frame):
                selected_frames = self.frames

        return selected_frames


    def get_width(self) -> int:
        """
        Returns the width of the .gif/.apng file
        """
        return self.frames[0][0].get_width()

    def get_height(self) -> int:
        """
        Returns the height of the .gif/.apng file
        """
        return self.frames[0][0].get_height()

    def get_size(self) -> Tuple[int, int]:
        """
        Returns the size of the .gif/.apng file
        """
        return self.frames[0][0].get_size()

    def get_rect(self, **kwargs) -> pygame.Rect:
        """
        Returns the rect of the .gif/.apng file

        :param kwargs: (optional) The the keyword arguments that will be passed in to the `surface.get_rect()` function.
        """
        return self.frames[0][0].get_rect(**kwargs)

    def get_surfaces(self, frames=[]):
        """
        Returns the surface of the selected frame(s)
        
        :param frames: (optional) Get the surface of the selected frames, leave empty to get all of the surfaces
        """
        if len(frames) == 0:
            selected_frames = self.frames.copy()
        else:
            selected_frames = []
            for frame in frames:
                try:
                    selected_frames.append(self.frames[frame])
                except IndexError:
                    print(f"Index {frame} does not exist, so it will be skipped")

        l = [frame[0] for frame in selected_frames]
        if len(l) == 1:
            l = l[0]
        return l

    def get_surface(self, select_frame: Optional[Union[None, SupportsIndex]] = None, first_frame: Optional[Union[None, SupportsIndex]] = None, last_frame: Optional[Union[None, SupportsIndex]] = None) -> List[pygame.Surface]:
        """
        Returns the surface of the selected frame(s)
        
        :param select_frame: (optional) Get the surface of only 1 frame, will ignore `first_frame` and `last_frame`, leave as `None` to use `first_frame` and `last_frame`
        :param first_frame: (optional) The first frame in the frames to get the surface from, leave as `None` to start from the first frame
        :param last_frame: (optional) The last frame in the frames to get the surface from, leave as `None` to end at the last frame
        
        Leave everything as `None` to get the surface all of the frames
        """
        warnings.warn("gif_pygame.PygameGIF.get_surface deprecated since 0.1.0, use gif_pygame.PygameGIF.get_surfaces instead", DeprecationWarning, 2)
        selected_frames = self._grab_frame(select_frame, first_frame, last_frame)

        l = [frame[0] for frame in selected_frames]
        if len(l) == 1:
            l = l[0]
        return l

    def set_surface(self, surfaces: Iterable[Tuple[pygame.Surface, int]]) -> None:
        """
        Replaces the surface of a frame to a new surface

        :param surfaces: A list of the new surfaces, inside the list must be another list with the surface as the first item and the frame index as the second item, must be as follows: `[[surf1, index1], [surf2, index2]]`
        
        if a given frame index cannot be found or a frame is duplicated, a warning will be sent and the frame will be ignored

        :raises IndexError: all of the given frame numbers given aren't an index of the frames list
        """
        failed_frames = []
        duplicated_frames = []
        successful_frames = []

        for index, surface in enumerate(surfaces):
            try:
                self.frames[surface[1]]
            except:
                failed_frames.append((index, surface[1]))
                continue

            if surface in successful_frames:
                duplicated_frames.append((index, surface[1]))
                continue

            else:
                successful_frames.append(surface)
                self.frames[surface[1]][0] = surface[0]

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

    def get_durations(self, frames=[]):
        """
        Returns the duration of the selected frame(s)
        
        :param frames: (optional) Get the surface of the selected frames, leave empty to get all of the durations
        """
        if len(frames) == 0:
            selected_frames = self.frames.copy()
        else:
            selected_frames = []
            for frame in frames:
                try:
                    selected_frames.append(self.frames[frame])
                except IndexError:
                    print(f"Index {frame} does not exist, so it will be skipped")

        l = [frame[1] for frame in selected_frames]
        if len(l) == 1:
            l = l[0]
        return l

    def get_duration(self, select_frame: Optional[Union[None, SupportsIndex]] = None, first_frame: Optional[Union[None, SupportsIndex]] = None, last_frame: Optional[Union[None, SupportsIndex]] = None) -> List[float]:
        """
        Returns the duration of the selected frame(s) in seconds
        
        :param select_frame: (optional) Get the duration of only 1 frame, will ignore `first_frame` and `last_frame`, leave as `None` to use `first_frame` and `last_frame`
        :param first_frame: (optional) The first frame in the frames to get the duration from, leave as `None` to start from the first frame
        :param last_frame: (optional) The last frame in the frames to get the duration from, leave as `None` to end at the last frame

        Leave everything as `None` to get the duration all of the frames
        """
        warnings.warn("gif_pygame.PygameGIF.get_duration deprecated since 0.1.0, use gif_pygame.PygameGIF.get_durations instead", DeprecationWarning, 2)
        selected_frames = self._grab_frame(select_frame, first_frame, last_frame)

        l = [frame[1] for frame in selected_frames]
        if len(l) == 1:
            l = l[0]
        return l

    def set_duration(self, durations: Iterable[Tuple[float, int]]) -> None:
        """
        Replaces the duration of a frame to a new duration (in seconds)

        :param durations: A list of the new durations, inside the list must be another list with the duration as the first item and the frame index as the second item, must be as follows: `[[duration1, index1], [duration2, index2]]`
        
        if a given frame index cannot be found or a frame is duplicated, a warning will be sent and the frame will be ignored

        :raises IndexError: all of the given frame numbers given aren't an index of the frames list
        """
        failed_frames = []
        duplicated_frames = []
        successful_frames = []

        for index, duration in enumerate(durations):
            try:
                self.frames[duration[1]]
            except:
                failed_frames.append((index, duration[1]))
                continue

            if duration in successful_frames:
                duplicated_frames.append((index, duration[1]))
                continue

            else:
                successful_frames.append(duration)
                self.frames[duration[1]][1] = duration[0]

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

    def get_datas(self, frames=[]):
        """
        Returns both the surface and the duration of the selected frame(s)
        
        :param frames: (optional) Get the surface of the selected frames, leave empty to get the surface and duration of all of the frames
        """
        if len(frames) == 0:
            selected_frames = self.frames.copy()
        else:
            selected_frames = []
            for frame in frames:
                try:
                    selected_frames.append(self.frames[frame])
                except IndexError:
                    print(f"Index {frame} does not exist, so it will be skipped")

        l = [frame for frame in selected_frames]
        if len(l) == 1:
            l = l[0]
        return l

    def get_data(self, select_frame: Optional[Union[None, SupportsIndex]] = None, first_frame: Optional[Union[None, SupportsIndex]] = None, last_frame: Optional[Union[None, SupportsIndex]] = None) -> List[Tuple[pygame.Surface, float]]:
        """
        Returns both the surface and the duration (in seconds) of the selected frame(s)
        
        :param select_frame: (optional) Get the surface & duration of only 1 frame, will ignore `first_frame` and `last_frame`, leave as `None` to use `first_frame` and `last_frame`
        :param first_frame: (optional) The first frame in the frames to get the surface & duration from, leave as `None` to start from the first frame
        :param last_frame: (optional) The last frame in the frames to get the surface & duration from, leave as `None` to end at the last frame

        Leave everything as `None` to get the surface & duration all of the frames
        """
        warnings.warn("gif_pygame.PygameGIF.get_data deprecated since 0.1.0, use gif_pygame.PygameGIF.get_datas instead", DeprecationWarning, 2)
        selected_frames = self._grab_frame(select_frame, first_frame, last_frame)

        l = [frame for frame in selected_frames]
        if len(l) == 1:
            l = l[0]
        return l

    def set_data(self, datas: Iterable[Tuple[pygame.Surface, float, int]]) -> None:
        """
        Replaces the data of a frame (surface and duration) to a new data

        :param datas: A list of the new data, inside the list must be another list with the surface as the first item, duration as the second item, and the frame index as the second item, must be as follows: `[[surface1, duration1, index1], [surface2, duration2, index2]]`
        
        if a given frame index cannot be found or a frame is duplicated, a warning will be sent and the frame will be ignored

        :raises IndexError: all of the given frame numbers given aren't an index of the frames list
        """
        failed_frames = []
        duplicated_frames = []
        successful_frames = []

        for index, data in enumerate(datas):
            try:
                self.frames[data[2]]
            except:
                failed_frames.append((index, data[2]))
                continue

            if data in successful_frames:
                duplicated_frames.append((index, data[2]))
                continue

            else:
                successful_frames.append(data)
                self.frames[data[2]][0] = data[0]
                self.frames[data[2]][1] = data[1]

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

    def get_alphas(self, frames=[]):
        """
        Returns the alpha of the selected frame(s)
        
        :param frames: (optional) Get the surface of the selected frames, leave empty to get all of the alphas
        """
        if len(frames) == 0:
            selected_frames = self.frames.copy()
        else:
            selected_frames = []
            for frame in frames:
                try:
                    selected_frames.append(self.frames[frame])
                except IndexError:
                    print(f"Index {frame} does not exist, so it will be skipped")

        l = [frame[0].get_alpha() for frame in selected_frames]
        if len(l) == 1:
            l = l[0]
        return l

    def get_alpha(self, select_frame: Optional[Union[None, SupportsIndex]] = None, first_frame: Optional[Union[None, SupportsIndex]] = None, last_frame: Optional[Union[None, SupportsIndex]] = None) -> List[int]:
        """
        Returns the alpha of the selected frame(s)

        :param select_frame: (optional) Get the alpha of only 1 frame, will ignore `first_frame` and `last_frame`, leave as `None` to use `first_frame` and `last_frame`
        :param first_frame: (optional) The first frame in the frames to get the alpha from, leave as `None` to start from the first frame
        :param last_frame: (optional) The last frame in the frames to get the alpha from, leave as `None` to end at the last frame

        Leave everything as `None` to get the alpha all of the frames
        """
        warnings.warn("gif_pygame.PygameGIF.get_alpha deprecated since 0.1.0, use gif_pygame.PygameGIF.get_alphas instead", DeprecationWarning, 2)
        selected_frames = self._grab_frame(select_frame, first_frame, last_frame)

        alphas = [frame[0].get_alpha() for frame in selected_frames]
        if len(alphas) == 1:
            alphas = alphas[0]
        return alphas

    def set_alpha(self, alpha: int, select_frame: Optional[Union[None, SupportsIndex]] = None, first_frame: Optional[Union[None, SupportsIndex]] = None, last_frame: Optional[Union[None, SupportsIndex]] = None) -> None:
        """
        Sets the alpha of the selected frame(s)

        :param alpha: The new alpha value
        :param select_frame: (optional) Set the `alpha` of only 1 frame, will ignore `first_frame` and `last_frame`, leave as `None` to use `first_frame` and `last_frame`
        :param first_frame: (optional) The first frame in the frames to set the `alpha` to, leave as `None` to start from the first frame
        :param last_frame: (optional) The last frame in the frames to set the `alpha` to, leave as `None` to end at the last frame

        Leave everything (except `alpha`) as `None` to set the `alpha` all of the frames
        """
        selected_frames = self._grab_frame(select_frame, first_frame, last_frame)

        for index, _ in enumerate(selected_frames):
            self.frames[index][0].set_alpha(alpha)


    def convert(self, colorkey: Optional[Union[None, _ColorValue]] = None, select_frame: Optional[Union[None, SupportsIndex]] = None, first_frame: Optional[Union[None, SupportsIndex]] = None, last_frame: Optional[Union[None, SupportsIndex]] = None) -> None:
        """
        Converts all surfaces

        :param colorkey: (optional) sets the colorkey of the frames, type `None` in order to not set a colorkey
        """

        selected_frames = self._grab_frame(select_frame, first_frame, last_frame)

        for index, _ in enumerate(selected_frames):
            self.frames[index][0] = self.frames[index][0].convert()

            if colorkey != None:
                self.frames[index][0].set_colorkey(colorkey)

    def render(self, surface: pygame.Surface, dest: Union[_Coordinate, _CanBeRect]) -> None:
        """
        Renders and animates the .gif file

        :param surface: The surface you want to render the animation at
        :param dest: Where the animation will be rendered at relative to the given surface
        """
        self._animate()
        surface.blit(self.frames[self.frame][0], dest)

    def blit_ready(self) -> pygame.Surface:
        """
        Animates the .gif file and returns the current frame. Best used with `surface.blit()` function

        :param surface: The surface you want to render the animation at
        :param dest: Where the animation will be rendered at relative to the given surface
        """
        self._animate()
        return self.get_surface(self.frame)

    def pause(self) -> None:
        """
        Pauses the animation
        """
        if not self.paused:
            self.paused_time = self.frame_time
        self.paused = True

    def unpause(self) -> None:
        """
        Continues the animation
        """
        if self.paused:
            self.frame_time = time.time()-(time.time()-self.paused_time)
        self.paused = False

    def reset(self, full_reset: Optional[bool] = False) -> None:
        """
        Resets the animation

        :param full_reset: (optional) Fully resets the animation by redoing the initialization

        Leave `full_reset` as `None` to keep the current data, only restart the animation from frame 0
        """
        if full_reset:
            self.gif = Image.open(self.filepath)
        
            self.frames = []
            for frame in range(self.gif.n_frames):
                self.gif.seek(frame)
                if frame == 0:
                    if "duration" in self.gif.info:
                        self.frames.append((pygame.image.load(self.filepath), self.gif.info["duration"]*.001))
                    else:
                        self.frames.append((pygame.image.load(self.filepath), 1))
                else:
                    self.frames.append((pygame.image.fromstring(self.gif.tobytes(), self.gif.size, self.gif.mode), self.gif.info["duration"]*.001))

            self.gif.close()

        self.frame = 0
        self.frame_time = 0
        self.paused_time = 0
        self.paused = False

def load(filepath: _FileArg) -> PygameGIF:
    """
    Loads the .gif file

    :param filepath: The path of the .gif/.apng file that you want to load

    :raises TypeError: if the `filepath` is not a .gif file
    """
    return PygameGIF(filepath)
