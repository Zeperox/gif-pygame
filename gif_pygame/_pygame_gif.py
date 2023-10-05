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
from typing import Union, Tuple, Sequence, SupportsIndex, Iterable, Optional

_Coordinate = Union[Tuple[float, float], Sequence[float], pygame.Vector2]
_CanBeRect = Union[pygame.Rect, Tuple[int, int, int, int], Tuple[_Coordinate, _Coordinate], Tuple[_Coordinate]]
_FileArg = Union[str, bytes]
_RgbaOutput = Tuple[int, int, int, int]
_ColorValue = Union[pygame.Color, int, str, Tuple[int, int, int], _RgbaOutput]


version = "1.0.0"

try:
	pygame.IS_CE
	is_ce = True
except AttributeError:
	warnings.warn("Your pygame version is not fully compatible with this module, so some functions may not run.\nPlease use pygame-ce for extra speed, better support, and better experience.\npip uninstall pygame\npip install pygame-ce", Warning, 2)
	is_ce = False

class PygameGIF:
	"""
	The class responsible for handling all of the .gif file functions
	"""
	def __init__(self, filepath: _FileArg, loops: Optional[int]=-1) -> None:
		"""
		Does the same thing as `PygameGIF.load()`, so why not use that?

		:param filepath: The path of the .gif file that you want to load
		:param loops: The amount of loops the .gif will play until pausing. Use `-1` for infinite loops

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
				self.frames.append([pygame.image.frombytes(self.gif.tobytes(), self.gif.size, self.gif.mode), self.gif.info["duration"]*.001])
		
		self.gif.close()
		self.frame = 0
		self.frame_time = 0
		self.paused_time = 0
		self.paused = False
		self.loops = [0, loops]
		self.ended = False

	
	def _animate(self):
		if self.frame_time == 0:
			self.frame_time = time.time()

		if time.time()-self.frame_time >= self.frames[self.frame][1] and not self.paused and not self.ended:
			if self.frame >= self.gif.n_frames-1:
				self.loops[0] += 1
			self.frame = self.frame + 1 if self.frame < self.gif.n_frames-1 else 0
			self.frame_time = time.time()

		
		if self.loops[1] != -1 and self.loops[0] > self.loops[1]:
			self.ended = True
			self.pause()
			self.paused = False

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

	def get_surfaces(self, frames: Optional[Iterable[int]]=[]) -> Sequence[pygame.Surface]:
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
		return l

	def set_surface(self, surfaces: Iterable[Tuple[pygame.Surface, int]]) -> None:
		"""
		Replaces the surface of a frame with a new surface

		:param surfaces: A list of the new surfaces, inside the list must be another list with the surface as the first item and the frame index as the second item, must be as follows: `[[surf1, index1], [surf2, index2]]`
		
		if a given frame index cannot be found or a frame is duplicated, a warning will be sent and the frame will be ignored

		:raises IndexError: all of the given frame numbers given aren't an index of the frames list
		"""
		warnings.warn("gif_pygame.PygameGIF.set_surface deprecated since 1.0.0, use gif_pygame.transform.surfaces instead", DeprecationWarning, 2)
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

	def get_durations(self, frames: Optional[Iterable[int]]=[]) -> Sequence[float]:
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
		return l

	def set_duration(self, durations: Iterable[Tuple[float, int]]) -> None:
		"""
		Replaces the duration of a frame with a new duration (in seconds)

		:param durations: A list of the new durations, inside the list must be another list with the duration as the first item and the frame index as the second item, must be as follows: `[[duration1, index1], [duration2, index2]]`
		
		if a given frame index cannot be found or a frame is duplicated, a warning will be sent and the frame will be ignored

		:raises IndexError: all of the given frame numbers given aren't an index of the frames list
		"""
		warnings.warn("gif_pygame.PygameGIF.set_duration deprecated since 1.0.0, use gif_pygame.transform.durations instead", DeprecationWarning, 2)
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

	def get_datas(self, frames: Optional[Iterable[int]]=[]) -> Sequence[Tuple[pygame.Surface, float]]:
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
		return l

	def set_data(self, datas: Iterable[Tuple[pygame.Surface, float, int]]) -> None:
		"""
		Replaces the data of a frame (surface and duration) with a new data

		:param datas: A list of the new data, inside the list must be another list with the surface as the first item, duration as the second item, and the frame index as the second item, must be as follows: `[[surface1, duration1, index1], [surface2, duration2, index2]]`
		
		if a given frame index cannot be found or a frame is duplicated, a warning will be sent and the frame will be ignored

		:raises IndexError: all of the given frame numbers given aren't an index of the frames list
		"""
		warnings.warn("gif_pygame.PygameGIF.set_data deprecated since 1.0.0, use gif_pygame.transform.datas instead", DeprecationWarning, 2)
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

	def get_alphas(self, frames: Optional[Iterable[int]]=[]) -> Sequence[int]:
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
		return l

	def set_alpha(self, alpha: int, select_frame: Optional[Union[None, SupportsIndex]] = None, first_frame: Optional[Union[None, SupportsIndex]] = None, last_frame: Optional[Union[None, SupportsIndex]] = None) -> None:
		"""
		Sets the alpha of the selected frame(s)

		:param alpha: The new alpha value
		:param select_frame: (optional) Set the `alpha` of only 1 frame, will ignore `first_frame` and `last_frame`, leave as `None` to use `first_frame` and `last_frame`
		:param first_frame: (optional) The first frame in the frames to set the `alpha` to, leave as `None` to start from the first frame
		:param last_frame: (optional) The last frame in the frames to set the `alpha` to, leave as `None` to end at the last frame

		Leave everything (except `alpha`) as `None` to set the `alpha` all of the frames
		"""
		warnings.warn("gif_pygame.PygameGIF.set_alpha deprecated since 1.0.0, use gif_pygame.transform.alphas instead", DeprecationWarning, 2)
		selected_frames = self._grab_frame(select_frame, first_frame, last_frame)

		for index, _ in enumerate(selected_frames):
			self.frames[index][0].set_alpha(alpha)


	def convert(self, colorkey: Optional[Union[None, _ColorValue]] = None, select_frame: Optional[Union[None, SupportsIndex]] = None, first_frame: Optional[Union[None, SupportsIndex]] = None, last_frame: Optional[Union[None, SupportsIndex]] = None) -> None:
		"""
		Converts all surfaces

		:param colorkey: (optional) sets the colorkey of the frames, type `None` in order to not set a colorkey
		"""
		warnings.warn("gif_pygame.PygameGIF.convert deprecated since 1.0.0, use gif_pygame.transform.convert instead", DeprecationWarning, 2)
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
		return self.get_surfaces([self.frame])

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
		if self.paused or self.ended:
			self.frame_time = time.time()-(time.time()-self.paused_time)
		self.paused = False
		self.ended = False

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
					self.frames.append((pygame.image.frombytes(self.gif.tobytes(), self.gif.size, self.gif.mode), self.gif.info["duration"]*.001))

			self.gif.close()

		self.frame = 0
		self.frame_time = 0
		self.paused_time = 0
		self.paused = False

class transform:
	"""
	allows for easy gif tranformation
	"""
	@staticmethod
	def flip(gif: PygameGIF, flip_x: bool, flip_y: bool, frames: Optional[Iterable[int]]=[]):
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
		transform.surfaces(gif, new_surfs)

	@staticmethod
	def scale(gif: PygameGIF, size: _Coordinate, frames: Optional[Iterable[int]]=[]):
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
		transform.surfaces(gif, new_surfs)

	@staticmethod
	def scale_by(gif: PygameGIF, factor: Union[float, Sequence[float]], frames: Optional[Iterable[int]]=[]):
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
		transform.surfaces(gif, new_surfs)

	@staticmethod
	def rotate(gif: PygameGIF, angle: float, frames: Optional[Iterable[int]]=[]):
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
		transform.surfaces(gif, new_surfs)
		
	@staticmethod
	def rotozoom(gif: PygameGIF, angle: int, scale: float, frames: Optional[Iterable[int]]=[]):
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
		transform.surfaces(gif, new_surfs)
		
	@staticmethod
	def scale2x(gif: PygameGIF, frames: Optional[Iterable[int]]=[]):
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
		transform.surfaces(gif, new_surfs)
		
	@staticmethod
	def smoothscale(gif: PygameGIF, size: _Coordinate, frames: Optional[Iterable[int]]=[]):
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
		transform.surfaces(gif, new_surfs)
		
	@staticmethod
	def smoothscale_by(gif: PygameGIF, factor: Union[float, Sequence[float]], frames: Optional[Iterable[int]]=[]):
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
		transform.surfaces(gif, new_surfs)
		
	@staticmethod
	def box_blur(gif: PygameGIF, radius: int, repeat_edged_pixels: Optional[bool]=True, frames: Optional[Iterable[int]]=[]):
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
		transform.surfaces(gif, new_surfs)
		
	@staticmethod
	def gaussian_blur(gif: PygameGIF, radius: int, repeat_edged_pixels: Optional[bool]=True, frames: Optional[Iterable[int]]=[]):
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
		transform.surfaces(gif, new_surfs)
		
	@staticmethod
	def invert(gif: PygameGIF, frames: Optional[Iterable[int]]=[]):
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
		transform.surfaces(gif, new_surfs)
		
	@staticmethod
	def grayscale(gif: PygameGIF, frames: Optional[Iterable[int]]=[]):
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
		transform.surfaces(gif, new_surfs)
	

	@staticmethod
	def convert(gif: PygameGIF, colorkey: Optional[Union[None, _ColorValue]]=None, colorkey_flags: Optional[int]=0, frames: Optional[Iterable[int]]=[]):
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
		transform.surfaces(gif, new_surfs)

	@staticmethod
	def convert_alpha(gif: PygameGIF, frames: Optional[Iterable[int]]=[]):
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
		transform.surfaces(gif, new_surfs)

	@staticmethod
	def surfaces(gif: PygameGIF, surfaces: Iterable[Tuple[pygame.Surface, int]]) -> None:
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

	@staticmethod
	def durations(gif: PygameGIF, durations: Iterable[Tuple[float, int]]) -> None:
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

	@staticmethod
	def datas(gif: PygameGIF, datas: Iterable[Tuple[pygame.Surface, float, int]]) -> None:
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

	@staticmethod
	def alphas(gif: PygameGIF, alphas: Iterable[Tuple[int, int]]) -> None:
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

def load(filepath: _FileArg, loops: Optional[int]=-1) -> PygameGIF:
	"""
	Loads the .gif file

	:param filepath: The path of the .gif/.apng file that you want to load
	:param loops: The amount of loops the .gif will play until pausing. Use `-1` for infinite loops

	:raises TypeError: if the `filepath` is not a .gif file
	"""
	return PygameGIF(filepath, loops)
