# -*- coding: UTF-8 -*-

"""
An animated image loader for Pygame
~~~~~~~~~~~~~~~~~~~~~~~~

A tool to make loading animated image files in pygame easier

	>>> # loading
	>>> import gif_pygame
	>>> loaded_gif = gif_pygame.load("path.gif") # Loads the .gif file

	>>> # rendering
	>>> loaded_gif.render(surface, (x, y)) # Renders and animates the animated image. THIS FUNCTION SHOULD NOT BE USED WITH `surface.blit()`
	>>> # or
	>>> surface.blit(loaded_gif.blit_ready(), (x, y)) # Animates the animated image and returns the current frame. Unlike `gif.render()`, this can be used with `surface.blit()`
	>>> More in docs
"""

version = "1.2.0"

import pygame, time, warnings

from PIL import Image
from typing import Union, Tuple, Sequence, Iterable, Optional
from importlib.metadata import version as libver
from packaging.version import Version

from ._common import is_ce, FileLike, Point, RectLike

if not is_ce:
	warnings.warn("\nYour pygame version is not fully compatible with this module, so some functions may not run.\nPlease use pygame-ce for extra speed, better support, and better experience.\npip uninstall pygame\npip install pygame-ce", Warning, 2)
	pygame.FRect = None

class GIFPygame:
	"""
	The class responsible for handling all of the animating functions
	"""
	def __init__(self, frames: Sequence[Tuple[pygame.Surface, float]], loops: int=-1) -> None:
		"""
		Creates a `GIFPygame` instance

		:param frames: The surfaces you want to animate. This should be a list of tuples/lists containing the surface and the amount of time it takes, in seconds, to move to the next frame.
		:param loops: (optional) The amount of loops the animation will play until pausing. Use `-1` for infinite loops
		"""
		for i, frame in enumerate(frames):
			frames[i] = list(frame)
		loops = int(loops)
		if loops < -1:
			loops = -1
		
		self._original_frames: Sequence[Tuple[pygame.Surface, float]] = []
		self._frames: Sequence[Tuple[pygame.Surface, float]] = []
		for frame_data in frames:
			self._frames.append([frame_data[0].copy(), frame_data[1]])
			self._original_frames.append([frame_data[0].copy(), frame_data[1]])
	
		self._frame: int = 0
		self._frame_time: float = 0

		self._paused_time: float = 0
		self._paused: bool = False

		self._end_time: float = 0
		self._ended: bool = False

		self._loops: Tuple[int, int] = [0, loops]
		self._speed: float = 1

	
	def _animate(self):
		"""
		Manages animating, looping, and timing
		"""
		if self._frame_time == 0:
			self._frame_time = time.time()

		if time.time()-self._frame_time >= self._frames[self._frame][1] / self.speed and not self._paused and not self._ended:
			if self._frame >= len(self._frames)-1:
				self._loops[0] += 1

			self._frame = self._frame + 1 if self._frame < len(self._frames)-1 else 0
			self._frame_time = time.time()
		
		if self._loops[1] != -1 and self._loops[0] > self._loops[1]:
			self.end()


	@property
	def original_frames(self) -> Sequence[Tuple[pygame.Surface, float]]:
		"""
		Returns the original, unedited frame surfaces and durations that were first loaded
		"""
		return self._original_frames

	@property
	def orig_frame(self) -> Sequence[Tuple[pygame.Surface, float]]:
		"""
		Returns the original, unedited frame surfaces and durations that were first loaded
		"""
		warnings.warn("gif_pygame.GIFPygame.orig_frame deprecated since 1.2.0, use gif_pygame.GIFPygame.original_frames instead", DeprecationWarning, 2)
		return self._original_frames

	@property
	def frames(self) -> Sequence[Tuple[pygame.Surface, float]]:
		"""
		Returns the frame surfaces with their durations
		"""
		return self._frames

	@property
	def frame_time(self) -> float:
		"""
		Returns the Unix time when the frame last changed
		"""
		return self._frame_time

	@property
	def paused_time(self) -> float:
		"""
		Returns the Unix time when the animation paused
		"""
		return self._paused_time

	@property
	def paused(self) -> bool:
		"""
		Returns whether the animation is paused or not
		"""
		return self._paused

	@property
	def current_loop(self) -> int:
		"""
		Returns the amount of loops that have happened
		"""
		return self._loops[0]

	@property
	def ended(self) -> bool:
		"""
		Returns whether the animation has ended or not
		"""
		return self._ended

	@property
	def end_time(self) -> float:
		"""
		Returns the Unix time when the animation ended
		"""
		return self._end_time


	@property
	def frame(self) -> int:
		"""
		Returns the current frame number
		"""
		return self._frame
	
	@frame.setter
	def frame(self, frame: int):
		"""
		Sets the current frame number
		"""
		if not (0 <= frame < len(self._frames)):
			raise IndexError(f"Given frame number \"{frame}\" is not within the frame range")
		self._frame = int(frame)

	@property
	def speed(self) -> float:
		"""
		Returns the current speed of the animation
		"""
		return self._speed

	@speed.setter
	def speed(self, speed: float):
		"""
		Sets the speed of the animation
		"""
		if speed <= 0:
			raise AttributeError("Speed attribute cannot be 0 or a negative number")
		self._speed = float(speed)

	@property
	def loops(self) -> Tuple[int, int]:
		"""
		Returns all the data regarding loops, both the amount of loops that have happened and the amount of loops that will play
		"""
		return self._loops

	@loops.setter
	def loops(self, loop_count: int):
		"""
		Sets the amount of times the animation will loop.
		"""
		if loop_count < -1:
			loop_count = -1

		self._loops[1] = loop_count

	@property
	def total_loops(self) -> int:
		"""
		Returns the amount of loops the animation will play
		"""
		return self._loops[1]

	@total_loops.setter
	def total_loops(self, loop_count: int):
		"""
		Sets the amount of times the animation will loop.
		"""
		self.loops = loop_count


	@property
	def width(self) -> int:
		"""
		Returns the width of the animation
		"""
		return self._frames[0][0].get_width()

	@property
	def height(self) -> int:
		"""
		Returns the height of the animation
		"""
		return self._frames[0][0].get_height()

	@property
	def size(self) -> Tuple[int, int]:
		"""
		Returns the size of the animation
		"""
		return self._frames[0][0].get_size()

	@property
	def current_surface(self) -> pygame.Surface:
		"""
		Returns the current frame surface
		"""
		return self._frames[self._frame][0]

	@property
	def current_duration(self) -> float:
		"""
		Returns the current frame duration
		"""
		return self._frames[self._frame][1]

	@property
	def current_frame_data(self) -> Tuple[pygame.Surface, float]:
		"""
		Returns the current frame surface and duration
		"""
		return self._frames[self._frame]


	def get_width(self) -> int:
		"""
		Returns the width of the animation
		"""
		return self._frames[0][0].get_width()

	def get_height(self) -> int:
		"""
		Returns the height of the animation
		"""
		return self._frames[0][0].get_height()

	def get_size(self) -> Tuple[int, int]:
		"""
		Returns the size of the animation
		"""
		return self._frames[0][0].get_size()

	def get_rect(self, **kwargs) -> pygame.Rect:
		"""
		Returns the rect of the animation

		:param kwargs: (optional) the keyword arguments that will be passed into the `surface.get_rect()` function.
		"""
		return self._frames[0][0].get_rect(**kwargs)

	def get_frect(self, **kwargs) -> pygame.FRect:
		"""
		Returns the rect of the animation with float values

		:param kwargs: (optional) the keyword arguments that will be passed into the `surface.get_frect()` function.
		"""
		if not is_ce:
			warnings.warn("This function, gif_pygame.GIFPygame.get_frect, will not run because your pygame version is not compatible with this function.\nPlease use pygame-ce for extra speed, better support, and better experience.\npip uninstall pygame\npip install pygame-ce", Warning, 2)
			return
		return self._frames[0][0].get_frect(**kwargs)

	def get_surfaces(self, frames: Optional[Iterable[int]]=None) -> Sequence[pygame.Surface]:
		"""
		Returns the surface of the selected frame(s)
		
		:param frames: (optional) Get the surface of the selected frames, leave empty to select all frames
		"""
		if not frames:
			selected_frames = self._frames
		else:
			selected_frames = []
			for frame in frames:
				try:
					selected_frames.append(self._frames[frame])
				except IndexError:
					print(f"Index {frame} does not exist, so it will be skipped")

		l = [frame[0] for frame in selected_frames]
		return l

	def get_durations(self, frames: Optional[Iterable[int]]=None) -> Sequence[float]:
		"""
		Returns the duration of the selected frame(s)
		
		:param frames: (optional) Get the frame duration of the selected frames, leave empty to select all frames
		"""
		if not frames:
			selected_frames = self._frames
		else:
			selected_frames = []
			for frame in frames:
				try:
					selected_frames.append(self._frames[frame])
				except IndexError:
					print(f"Index {frame} does not exist, so it will be skipped")

		l = [frame[1] for frame in selected_frames]
		return l

	def get_frame_data(self, frames: Optional[Iterable[int]]=None) -> Sequence[Tuple[pygame.Surface, float]]:
		"""
		Returns both the surface and the duration of the selected frame(s)
		
		:param frames: (optional) Get the frame data of the selected frames, leave empty to select all frames
		"""
		if not frames:
			selected_frames = self._frames
		else:
			selected_frames = []
			for frame in frames:
				try:
					selected_frames.append(self._frames[frame])
				except IndexError:
					print(f"Index {frame} does not exist, so it will be skipped")

		l = [frame for frame in selected_frames]
		return l

	def get_datas(self, frames: Optional[Iterable[int]]=None) -> Sequence[Tuple[pygame.Surface, float]]:
		"""
		Returns both the surface and the duration of the selected frame(s)
		
		:param frames: (optional) Get the frame data of the selected frames, leave empty to select all frames
		"""
		warnings.warn("gif_pygame.GIFPygame.get_datas deprecated since 1.2.0, use gif_pygame.GIFPygame.get_frame_data instead", DeprecationWarning, 2)
		return self.get_frame_data(frames)

	def get_current_surface(self) -> pygame.Surface:
		"""
		Returns the current frame surface
		"""
		return self._frames[self._frame][0]

	def get_current_duration(self) -> float:
		"""
		Returns the current frame duration
		"""
		return self._frames[self._frame][1]

	def get_current_frame_data(self) -> Tuple[pygame.Surface, float]:
		"""
		Returns the current frame surface and duration
		"""
		return self._frames[self._frame]

	def get_alphas(self, frames: Optional[Iterable[int]]=None) -> Sequence[int]:
		"""
		Returns the alpha of the selected frame(s)
		
		:param frames: (optional) Get the surface alpha of the selected frames, leave empty to select all frames
		"""
		if not frames:
			selected_frames = self._frames
		else:
			selected_frames = []
			for frame in frames:
				try:
					selected_frames.append(self._frames[frame])
				except IndexError:
					print(f"Index {frame} does not exist, so it will be skipped")

		l = [frame[0].get_alpha() for frame in selected_frames]
		return l


	def render(self, surface: pygame.Surface, dest: Union[Point, RectLike]) -> None:
		"""
		Renders and animates the animation

		:param surface: The surface you want to render the animation on
		:param dest: Where the animation will be rendered at relative to the given surface
		"""
		self._animate()
		surface.blit(self._frames[self._frame][0], dest)

	def blit_ready(self) -> pygame.Surface:
		"""
		Animates the animation and returns the current frame. Best used with the `pygame.Surface().blit()` function
		"""
		self._animate()
		return self.current_surface

	def pause(self) -> None:
		"""
		Pauses the animation
		"""
		if not self._paused:
			self._paused_time = time.time()
		self._paused = True

	def unpause(self) -> None:
		"""
		Continues the animation
		"""
		if self._paused:
			self._frame_time += time.time()-self._paused_time
		self._paused_time = 0
		self._paused = False

	def end(self) -> None:
		"""
		Abruptly ends the animation
		"""
		if not self._ended:
			self._end_time = time.time()
		self._ended = True

	def unend(self, subtract_loops_by: int, reset_animation: bool) -> None:
		"""
		Continues the animation even after ending

		:param subtract_loops_by: the number of loops that will be subtracted from the number of loops that have played. This prevents the animation from immediately ending when loops are limited
		:param reset_animation: whether the animation should play from the start again or not
		"""
		if self._ended and not reset_animation:
			self._frame_time += time.time()-self._paused_time
		self._end_time = 0
		self._ended = False
		self._loops[0] -= abs(subtract_loops_by)

		if reset_animation:
			self._frame = 0
			self._frame_time = 0

	def reset(self, full_reset: bool = False) -> None:
		"""
		Resets the animation

		:param full_reset: (optional) Fully resets the animation to its original, unedited form

		Leave `full_reset` as `False` to keep the current data, only restart the animation from frame 0
		"""
		if full_reset:
			self._frames: Sequence[Tuple[pygame.Surface, float]] = []
			for frame_data in self._original_frames:
				self._frames.append([frame_data[0].copy(), frame_data[1]])

		self._frame = 0
		self._frame_time = 0

		self._paused_time = 0
		self._paused = False

		self._end_time = 0
		self._ended = False

		self._loops[0] = 0
		self._speed = 1

	def reset_surfaces(self) -> None:
		"""
		Resets the surfaces to their original, unedited surfaces that were first loaded
		"""
		for i in range(len(self._frames)):
			self._frames[i][0] = self._original_frames[i][0].copy()

	def reset_durations(self) -> None:
		"""
		Resets the frame durations to their original, unedited durations that were first loaded
		"""
		for i in range(len(self._frames)):
			self._frames[i][1] = self._original_frames[i][1]

	def reset_frame_data(self) -> None:
		"""
		Fully resets the animation to its original, unedited form
		"""
		self._frames: Sequence[Tuple[pygame.Surface, float]] = []
		for frame_data in self._original_frames:
			self._frames.append([frame_data[0].copy(), frame_data[1]])

	def copy(self, original_frame_data: bool=False):
		"""
		Returns a copy of the gif

		:param original_frame_data: (optional) whether the copy based on the original, unedited frame data or based on the edited data
		"""
		if original_frame_data:
			gif = GIFPygame([(frame[0].copy(), frame[1]) for frame in self._original_frames], self._loops[1])
			gif._frames = self._frames
			return gif
		else:
			return GIFPygame([(frame[0].copy(), frame[1]) for frame in self._frames], self._loops[1])


def load(filepath: FileLike, loops: int=-1) -> GIFPygame:
	"""
	Loads the animation file

	:param filepath: The file path to the animation file that you want to load
	:param loops: The amount of loops the animation will play until pausing. Use `-1` for infinite loops
	"""
	
	if is_ce and Version(libver("pygame-ce")) >= Version("2.5.4"):
		frames = pygame.image.load_animation(filepath)
		for i, frame in enumerate(frames):
			frames[i] = [frame[0], frame[1]*.001]
	else:
		gif = Image.open(filepath)
		frames = []

		for frame in range(gif.n_frames):
			gif.seek(frame)
			frames.append([pygame.image.frombytes(gif.tobytes(), gif.size, gif.mode), gif.info.get("duration", 1000)*0.001])
		gif.close()
	
	return GIFPygame(frames, loops)

def save(gif: GIFPygame, file: FileLike) -> None:
	"""
	Saves the animation into a file

	:param gif: the animation to be saved
	:param file: the location where the animation will be saved
	"""
	images = []

	for surf in gif.get_surfaces():
		surf_data = pygame.image.tobytes(surf, "RGBA")
		img = Image.frombytes("RGBA", surf.get_size(), surf_data)
		images.append(img)

	images[0].save(
		file,
		save_all=True,
		append_images=images[1:],
		duration=[int(d*1000) for d in gif.get_durations()],
		loop=0
	)
