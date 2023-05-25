#!/usr/bin/env python

import sdl2
import sdl2.ext
import numpy as np

SCREEN_WIDTH = 800 
SCREEN_HEIGHT = 600

class Vec3d:
    def __init__(self, x, y, z):
        self.x = x 
        self.y = y
        self.z = z 

    def __str__(self):
        return "Vec3d({self.x}, {self.y}, {self.z})"
    
class Triangle:
    def __init__(self, vertices):
        self.vertices = vertices

class Mesh:
    def __init__(self, triangles = []):
        self.triangles = triangles


class GameEngine(object):
    def __init__(self):
        sdl2.ext.init()
        self.window = sdl2.ext.Window("Game Console", size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.window.show()
        self.renderer = sdl2.ext.Renderer(self.window)
        self.surface = sdl2.SDL_CreateRGBSurface(0, SCREEN_WIDTH, SCREEN_HEIGHT, 32, 0, 0, 0, 1)
        self.__runLoop()

    # game loop
    def onStart(self):
        return True

    def onUpdate(self):
        # Clear the screen 
        sdl2.SDL_SetRenderDrawColor(self.renderer.sdlrenderer, 0xFF, 0xFF, 0xFF, 0xFF);
        sdl2.SDL_RenderClear(self.renderer.sdlrenderer)

        return True

    # private 
    def __runLoop(self):
        running = True
        if self.onStart():
            while running and self.onUpdate():
                events = sdl2.ext.get_events()
                for event in events:
                    if event.type == sdl2.SDL_QUIT:
                        running = False
                        break

        sdl2.SDL_FreeSurface(self.surface)
        sdl2.ext.quit()

class CubeEngine(GameEngine):
    def __init__(self):
        self.cubeMesh = Mesh()
        super(CubeEngine, self).__init__()

    # Lifecycle methods
    def onStart(self):
        if not GameEngine.onStart(self):
            return False 
        
        self.renderer.present()
        self.cubeMesh.triangles = [
            # SOUTH 
            Triangle([Vec3d(0, 0, 0), Vec3d(0, 1, 0), Vec3d(1, 1, 0)]),
            Triangle([Vec3d(0, 0, 0), Vec3d(1, 1, 0), Vec3d(1, 0, 0)]),

            # EAST 
            Triangle([Vec3d(1, 0, 0), Vec3d(1, 1, 0), Vec3d(1, 1, 1)]),
            Triangle([Vec3d(1, 0, 0), Vec3d(1, 1, 1), Vec3d(1, 0, 1)]),

            # NORTH 
            Triangle([Vec3d(1, 0, 1), Vec3d(1, 1, 1), Vec3d(0, 1, 1)]),
            Triangle([Vec3d(1, 0, 1), Vec3d(0, 1, 1), Vec3d(0, 0, 1)]),

            # WEST
            Triangle([Vec3d(0, 0, 1), Vec3d(0, 1, 1), Vec3d(0, 1, 0)]),
            Triangle([Vec3d(0, 0, 1), Vec3d(0, 1, 0), Vec3d(0, 0, 0)]),

            # TOP
            Triangle([Vec3d(0, 1, 0), Vec3d(0, 1, 1), Vec3d(1, 1, 1)]),
            Triangle([Vec3d(0, 1, 0), Vec3d(1, 1, 1), Vec3d(1, 1, 0)]),

            # BOTTOM
            Triangle([Vec3d(1, 0, 1), Vec3d(0, 0, 1), Vec3d(0, 0, 0)]),
            Triangle([Vec3d(1, 0, 1), Vec3d(0, 0, 0), Vec3d(1, 0, 0)]),
        ]

        # Projection Matrix 
        near = 0.2 
        far = 1000.0
        fov = 90.0
        aspectRatio = float(SCREEN_HEIGHT) / float(SCREEN_WIDTH)
        fovRad = 1.0 / np.tan(np.deg2rad(fov) / 2)

        # self.projectionMatrix = np.matrix([
        #     [aspectRatio * fovRad, 0, 0, 0],
        #     [0, fovRad, 0, 0],
        #     [0, 0, far / (far - near), 1],
        #     [0, 0, (-far * near) / (far - near), 0]
        # ], dtype=np.float32)

        self.projectionMatrix = np.matrix([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ], dtype=np.float32)

        return True 
    
    def onUpdate(self):
        if not GameEngine.onUpdate(self):
            return False

        # Draw triangles 
        for triangle in self.cubeMesh.triangles:
            vertices = map(lambda t: np.array([t.x, t.y, t.z]).reshape(3, 1), triangle.vertices)
            projectedTriangle = np.dot(self.projectionMatrix, vertices)

            for i in range(len(projectedTriangle[0])):
                # get start and end point
                start_point = [projectedTriangle.item(0, i), projectedTriangle.item(1, i)]
                endIndex = (i + 1) % projectedTriangle.shape[1]
                end_point = [projectedTriangle.item(0, endIndex), projectedTriangle.item(1, endIndex)]

                # scale the point
                start_point[0] = (start_point[0] + 1) * SCREEN_WIDTH / 4
                start_point[1] = (start_point[1] + 1) * SCREEN_HEIGHT / 4
                end_point[0] = (end_point[0] + 1) * SCREEN_WIDTH / 4
                end_point[1] = (end_point[1] + 1) * SCREEN_HEIGHT / 4


                sdl2.SDL_SetRenderDrawColor(self.renderer.sdlrenderer, 0x00, 0x00, 0x00, 0xFF)
                sdl2.SDL_RenderDrawLine(self.renderer.sdlrenderer, int(start_point[0]), int(start_point[1]), int(end_point[0]), int(end_point[1]))
        
        self.renderer.present()

        return True

def main():
    game = CubeEngine()
   

if __name__ == "__main__":
    main() 