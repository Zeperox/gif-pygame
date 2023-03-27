# gif_pygame
[PyPI Link](https://pypi.org/project/gif-pygame/0.0.1/)

A pygame addon that allows you to load, animate, and render animated image files like .gif and .apng

## How to use
```py
# example code

import pygame, pygame_gif, sys

win = pygame.display.set_mode((512, 512))
example_gif = pygame_gif.load("example.gif") # Loads a .gif file
example_png = pygame_gif.load("example.png") # Loads a .png file, the module supports non-animated files, but it is not recommended
example_apng = pygame_gif.load("example.apng") # Loads a .apng file

while 1:
    win.fill((0, 0, 0))
    
    # There are 2 ways of rendering the animated img file, the first method is doing "gif.render(surface, (x, y))", the other method is doing "surface.blit(gif.blit_ready(), (x, y))". THE "blit_ready()" FUNCTION MUST BE CALLED WHEN DOING THE SECOND METHOD
    example_gif.render(win, (128-example_gif.get_width()*0.5, 256-example_gif.get_height()*0.5))
    example_png.render(win, (256-example_png.get_width()*0.5, 256-example_png.get_height()*0.5))
    example_apng.blit(example_apng.blit_ready(), (384-example_apng.get_width()*0.5, 256-example_apng.get_height()*0.5))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if example_gif.paused:
                    example_gif.unpause()
                else:
                    example_gif.pause()
                if example_png.paused:
                    example_png.unpause()
                else:
                    example_png.pause()
                if example_apng.paused:
                    example_apng.unpause()
                else:
                    example_apng.pause()
                    
    pygame.display.update()
```

To recap:

`pygame_gif.load` loads in the image

To render the image you've got 2 options:
- `img.render(surf, (x, y))`
- `surf.blit(img.blit_ready(), (x, y))` (`.blit_ready()` can be used to return the current frame's surface)

There are other extra functions. The ones showcased in the example code are `img.pause()` and `img.unpause()`.

There are also:
- `.get_width()`, returns the width of the image
- `.get_height()`, returns the height of the image
- `.get_size()`, returns the size of the image
- `.get_rect()`, returns the rect of the image
- `.get_surface()`, returns a list of all surfaces in the animation, you can also pass in certain indexes
- `.set_surface()`, replaces some of the surfaces in the animation with newer surfaces
- `.get_duration()`, returns a list of all durations in the animation, you can also pass in certain indexes
- `.set_duration()`, replaces some of the durations in the animation with newer durations
- `.get_data()`, returns a list of all surfaces and durations in the animation, you can also pass in certain indexes
- `.set_data()`, replaces some of the surfaces and durations in the animation with newer surfaces and durations
- `.get_alpha()`, returns a list of that includes the alphas of all surfaces in the animation, you can also pass in certain indexes
- `.set_alpha()`, replaces all the alphas of surfaces with newer alphas, you can also pass in certain indexes
- `.convert()`, converts all the surfaces in the animation, you can also pass in a `colorkey` and certain indexes

Please use python's `help()` function for more in-depth explanation
