#https://stackoverflow.com/questions/67367424/how-do-i-add-an-image-as-texture-of-my-3d-cube-in-pyopengl

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
import cv2
import numpy as np

verticies = (
( 1, -1, -1), # 0
( 1,  1, -1), # 1
(-1,  1, -1), # 2
(-1, -1, -1), # 3
( 1, -1,  1), # 4
( 1,  1,  1), # 5
(-1, -1,  1), # 6
(-1,  1,  1), # 7
)

textureCoordinates = ((0, 0), (0, 1), (1, 1), (1, 0))

surfaces = (
(0,1,2,3),
(3,2,7,6),
(6,7,5,4),
(4,5,1,0),
(1,5,7,2),
(4,0,3,6),
)

normals = [
( 0,  0, -1),  # surface 0
(-1,  0,  0),  # surface 1
( 0,  0,  1),  # surface 2
( 1,  0,  0),  # surface 3
( 0,  1,  0),  # surface 4
( 0, -1,  0)   # surface 5
    ]

colors = (
(1,1,1),
(0,1,0),
(0,0,1),
(0,1,0),
(0,0,1),
(1,0,1),
(0,1,0),
(1,0,1),
(0,1,0),
(0,0,1),
)

edges = (
(0,1),
(0,3),
(0,4),
(2,1),
(2,3),
(2,7),
(6,3),
(6,4),
(6,7),
(5,1),
(5,4),
(5,7),
)


def Cube():
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    for i_surface, surface in enumerate(surfaces):
        x = 0
        glNormal3fv(normals[i_surface])
        for i_vertex, vertex in enumerate(surface):
            x+=1
            #
            glTexCoord2fv(textureCoordinates[i_vertex])
            glVertex3fv(verticies[vertex])
    glEnd()

    glColor3fv(colors[0])
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def main():
    global surfaces

    pygame.init()
    display = (400, 300)
    screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    clock = pygame.time.Clock()

    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('output.avi', fourcc, 20.0, (400, 300))

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0, 0, -5)

    #glLight(GL_LIGHT0, GL_POSITION,  (0, 0, 1, 0)) # directional light from the front
    glLight(GL_LIGHT0, GL_POSITION,  (5, 5, 5, 1)) # point light from the left, top, front
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))

    glEnable(GL_DEPTH_TEST) 

    image = pygame.image.load('data/1.jpeg')
    datas = pygame.image.tostring(image, 'RGBA')
    texID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texID)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(), image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, datas)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glEnable(GL_TEXTURE_2D)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # out.release()
                pygame.quit()
                cv2.destroyAllWindows()
                quit()      

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE )

        glRotatef(1, 3, 1, 1)
        Cube()

        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)
        glDisable(GL_COLOR_MATERIAL)


        img = pygame.surfarray.pixels3d(screen)
        img = np.rot90(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        # out.write(img)
        cv2.imshow('Pygame Screen', img)
        # pygame.display.update()
        pygame.display.flip()
        clock.tick(60)

main()