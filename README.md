# gif_pygame

A pygame addon that allows you to load, animate, and render animated image files like .gif and .apng

## Basic Example Code

```py
import pygame
import gif_pygame
import sys

screen = pygame.display.set_mode((512, 512))
clock = pygame.Clock()

# Loading from a file. You can specify the number of loops, but by default it is infinite
animation_gif = gif_pygame.load("exmaple.gif")

# Creating an animation from a list of surfaces
s1 = pygame.Surface((20, 0))
s2 = pygame.Surface((20, 0))
s3 = pygame.Surface((20, 0))
s1.fill((255, 0, 0))
s2.fill((0, 255, 0))
s3.fill((0, 0, 255))

# For every list, first index must be the surface and second must be the duration in seconds. You can specify the number of loops, but by default it is infinite
animation_surfs = gif_pygame.GIFPygame([[s1, 1], [s2, 1], [s3, 0.5]])

# Main loop
while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    # This module provides 2 methods for rendering the animation.

    # Method 1: using .render() | Animates and renders into the screen inside the function itself. You must pass down the surface to blit to and the location
    animation_gif.render(screen, (10, 10))

    # Method 2: using .blit_ready() | Animates the animation and returns the current frame. This was meant to be used alongside pygame.Surface().blit()
    screen.blit(animation_surfs.blit_ready(), (70, 70))

    pygame.display.flip()
```

To recap:

- `gif_pygame.load()`: Loads the animation file
- `gif_pygame.GIFPygame()`: Creates an animation from a list of surfaces and durations

To render the image you've got 2 options:
- `GIFPygame().render(surf, (x, y))`
- `surf.blit(GIFPygame().blit_ready(), (x, y))` (`.blit_ready()` can be used to return the current frame's surface)

There are also:
- `GIFPygame().pause()`: Pauses the animation
- `GIFPygame().unpause()`: Resumes the animation
- `GIFPygame().reset()`: Resets the animation's data
- `GIFPygame().copy()`: Returns a copy of the animation
- `GIFPygame().get_width()`: Returns the width of the animation
- `GIFPygame().get_height()`: Returns the height of the animation
- `GIFPygame().get_size()`: Returns the size of the animation
- `GIFPygame().get_rect()`: Returns the rect of the animation
- `GIFPygame().get_surfaces()`: Returns a list of all surfaces in the animation, you can also pass in certain indexes
- `GIFPygame().get_durations()`: Returns a list of all durations in the animation, you can also pass in certain indexes
- `GIFPygame().get_frame_data()`: Returns a list of all surfaces and durations in the animation, you can also pass in certain indexes

The module also contains a sublibrary for editing the animation, `gif_pygame.transform`, which has almost all of the transform options pygame gives, and allows for editing the animation's frame data

Please use python's `help()` function for more in-depth explanation

*(A documentation will be added soon)*
