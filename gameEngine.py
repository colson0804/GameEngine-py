#!/usr/bin/env python

import sdl2
import sdl2.ext

class Vec3d:
    def __init__(self, x, y, z):
        self.x = x 
        self.y = y
        self.z = z 

    def __str__(self):
        return "Vec3d({self.x}, {self.y}, {self.z})"
    
class Triangle:
    def __init__(self, vec3d):
        self.vec3d = vec3d

class Mesh:
    def __buildMesh():
        return

    def __init__(self, triangles):
        self.triangles = triangles
        self.mesh = self.__buildMesh()


class GameEngine(object):
    def __init__(self):
        self.__runLoop()

    # game loop
    def onStart(self):
        return True

    def onUpdate(self):
        return True

    # private 
    def __runLoop(self):
        running = True
        self.onStart()
        while running and self.onUpdate():
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_QUIT:
                    running = False
                    break

        sdl2.ext.quit()

class CubeEngine(GameEngine):
    def __init__(self):
        super(CubeEngine, self).__init__()
        self.cubeMesh = None

    # Lifecycle methods
    def onStart(self):
        return True 
    
    def onUpdate(self):
        return True


def main():
    # initialize game console
    sdl2.ext.init() 
    width, height = 800, 600 
    window = sdl2.ext.Window("Game Console", size=(width, height))
    window.show()

    game = CubeEngine()
   

if __name__ == "__main__":
    main() 