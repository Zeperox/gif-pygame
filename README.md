# gif_pygame
A pygame addon that allows you to load, animate, and render animated image files like .gif and .apng

## How to use
```py
# example code

import pygame, sys, gif_pygame

win = pygame.display.set_mode((512, 512))
example_gif = gif_pygame.load("example.gif") # Loads a .gif file
example_png = gif_pygame.load("example.png") # Loads a .png file, the module supports non-animated files, but it is not recommended

s1 = pygame.Surface((66, 66))
s2 = pygame.Surface((66, 66))
s3 = pygame.Surface((66, 66))
s1.fill((255, 0, 0))
s2.fill((0, 255, 0))
s3.fill((0, 0, 255))

example_surfs = gif_pygame.GIFPygame([(s1, 1), (s2, 1), (s3, 1)])

while True:
    win.fill((0, 0, 0))
    
    # There are 2 ways of rendering the animated img file, the first method is doing "gif.render(surface, (x, y))", the other method is doing "surface.blit(gif.blit_ready(), (x, y))". THE ".blit_ready()" FUNCTION MUST BE CALLED WHEN DOING THE SECOND METHOD
    example_gif.render(win, (128-example_gif.get_width()*0.5, 256-example_gif.get_height()*0.5))
    example_png.render(win, (256-example_png.get_width()*0.5, 256-example_png.get_height()*0.5))
    win.blit(example_surfs.blit_ready(), (384-example_surfs.get_width()*0.5, 256-example_surfs.get_height()*0.5))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if example_gif.paused: # Check whether `example_gif` is paused or not
                    example_gif.unpause() # unpauses `example_gif` if it was paused
                else:
                    example_gif.pause() # pauses `example_gif` if it was unpaused

                if example_png.paused: # Check whether `example_png` is paused or not, since this is a non-animated image, it will not be affected
                    example_png.unpause() # unpauses `example_png` if it was paused, since this is a non-animated image, it will not be affected
                else:
                    example_png.pause() # pauses `example_png` if it was unpaused, since this is a non-animated image, it will not be affected

                if example_surfs.paused: # Check whether `example_surfs` is paused or not
                    example_surfs.unpause() # unpauses `example_surfs` if it was paused
                else:
                    example_surfs.pause() # pauses `example_surfs` if it was unpaused
                    
    pygame.display.update()
```

To recap:

`gif_pygame.load` loads in the image

To render the image you've got 2 options:
- `img.render(surf, (x, y))`
- `surf.blit(img.blit_ready(), (x, y))` (`.blit_ready()` can be used to return the current frame's surface)

There are other extra functions. The ones showcased in the example code are `img.pause()` and `img.unpause()`.

There are also:
- `GIFPygame.get_width()`, returns the width of the image
- `GIFPygame.get_height()`, returns the height of the image
- `GIFPygame.get_size()`, returns the size of the image
- `GIFPygame.get_rect()`, returns the rect of the image
- `GIFPygame.get_surfaces()`, returns a list of all surfaces in the animation, you can also pass in certain indexes
- `GIFPygame.set_surface()`, replaces some of the surfaces in the animation with newer surfaces
- `.get_durations()`, returns a list of all durations in the animation, you can also pass in certain indexes
- `.set_duration()`, replaces some of the durations in the animation with newer durations
- `.get_datas()`, returns a list of all surfaces and durations in the animation, you can also pass in certain indexes
- `.set_data()`, replaces some of the surfaces and durations in the animation with newer surfaces and durations
- `.get_alphas()`, returns a list of that includes the alphas of all surfaces in the animation, you can also pass in certain indexes
- `.set_alpha()`, replaces all the alphas of surfaces with newer alphas, you can also pass in certain indexes

Please use python's `help()` function for more in-depth explanation

(A documentation will be added soon)