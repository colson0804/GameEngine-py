#!/usr/bin/env python

import sys
import sdl2
import sdl2.ext

def main():
    # initialize game console
    sdl2.ext.init() 
    width, height = 800, 600 
    window = sdl2.ext.Window("Game Console", size=(width, height))
    window.show()

    # Set up the run loop
    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break

    sdl2.ext.quit()

if __name__ == "__main__":
    main() 