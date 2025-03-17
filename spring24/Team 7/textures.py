import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *

from shapes import Rectangle

ANIMATION_FRAME = 0
FRAME_DURATION = 20

sprites = {
    "pacman": "res/image/pacman.png",
    "ghosts": "res/image/ghosts.png",
    "pellete": "res/image/pellete.png",
    "power_pellete": "res/image/power_pellete.png",
    "level": "res/image/level.png",
    "pac_life": "res/image/pac_life.png",
    "arrow": "res/image/arrow.png",
    "logo": "res/image/logo.png",
    "press_key": "res/image/press_key.png",
    "ready": "res/image/ready.png",
}

sprite_id = {
    "pacman": 0,
    "ghosts": 1,
    "pellete": 2,
    "power_pellete": 3,
    "level": 4,
    "pac_life": 5,
    "arrow": 6,
    "logo": 7,
    "press_key": 8,
    "ready": 9,
}


def my_init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_TEXTURE_2D)
    glMatrixMode(GL_PROJECTION)  # ortho or perspective NO BRAINER
    glLoadIdentity()
    glOrtho(0, 460, 0, 520, 0, 1)  # l,r,b,t,n,f

    glMatrixMode(GL_MODELVIEW)
    loadTextures()

    global test_rect

    test_rect = Rectangle(x=230, y=250, length=456, width=496)


texture_names = [x for x in range(15)]  # TODO IMPORTANT must be numbers


def texture_setup(texture_image_binary, texture_name, width, height):
    """Assign texture attributes to specific images."""
    glBindTexture(GL_TEXTURE_2D, texture_name)  # texture init step [5]

    # texture init step [6]
    # affects the active selected texture which is identified by texture_name
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(
        GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT
    )  # GL_MIRRORED_REPEAT , GL_CLAMP_TO_EDGE, GL_CLAMP_TO_BORDER
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    # END: texture init step [6]

    glTexImage2D(
        GL_TEXTURE_2D,
        0,  # mipmap
        GL_RGBA,  # Bytes per pixel
        width,
        height,
        0,  # Texture border
        GL_RGBA,  # RGBA Exactly as in  pygame.image.tostring(image, "RGBA", True)
        GL_UNSIGNED_BYTE,
        texture_image_binary,
    )  # texture init step [7]


def load_and_setup(image_path, idx):
    # Load images from file system
    image = pygame.image.load(image_path)
    # Convert images to the type needed for textures
    texture = pygame.image.tostring(image, "RGBA", True)  # texture init step [3]
    texture_setup(texture, texture_names[idx], image.get_width(), image.get_height())


def loadTextures():
    """Open images and convert them to "raw" pixel maps and
    bind or associate each image with and integer refernece number.
    """
    # Generate textures names from array
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glGenTextures(len(texture_names), texture_names)  # texture init step [4]

    # Add textures to openGL [2, 3, 5 ,6 ,7]
    # pacman texture is [11 x 6] x 16 pixels

    for key, value in sprites.items():
        load_and_setup(value, sprite_id[key])


def draw_entity(entity, texture_id):
    # glClear(GL_COLOR_BUFFER_BIT)
    # glColor3f(1, 1, 1)  # TODO IMPORTANT
    # glLoadIdentity()
    # glClearColor(0, 0, 0, 0)

    if hasattr(entity, "rect"):
        entity = entity.rect

    glBindTexture(
        GL_TEXTURE_2D, texture_names[texture_id]
    )  # repeat this if you want to bind another texture
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)  # TODO IMPORTANT: glTexCoord2f must come first before glVertex2d
    glVertex2d(entity.left, entity.bottom)

    glTexCoord2f(1, 0)
    glVertex2d(entity.right, entity.bottom)

    glTexCoord2f(1, 1)
    glVertex2d(entity.right, entity.top)

    glTexCoord2f(0, 1)
    glVertex2d(entity.left, entity.top)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, -1)

    # glutSwapBuffers()


def draw_from_atlas(entity, sprite_atlas_id, atlas_size, texture_idx):
    global ANIMATION_FRAME, FRAME_DURATION

    if hasattr(entity, "rect"):
        rect = entity.rect
    else:
        rect = entity

    texture = texture_idx[0]

    if type(texture_idx) == list and len(texture_idx) > 1:
        if hasattr(entity, "is_moving") and not entity.is_moving:
            texture = 0

        else:
            if ANIMATION_FRAME < FRAME_DURATION:
                texture = texture_idx[0]
            elif ANIMATION_FRAME > FRAME_DURATION:
                texture = texture_idx[1]

            ANIMATION_FRAME = (
                ANIMATION_FRAME + 1 if ANIMATION_FRAME < 2 * FRAME_DURATION else 0
            )

    tex_coord = texture * 1 / atlas_size
    sprite_width = 16 / (atlas_size * 16)

    glBindTexture(GL_TEXTURE_2D, texture_names[sprite_atlas_id])

    glBegin(GL_QUADS)
    glTexCoord2f(tex_coord, 0)
    glVertex2d(rect.left, rect.bottom)

    glTexCoord2f(tex_coord + sprite_width, 0)
    glVertex2d(rect.right, rect.bottom)

    glTexCoord2f(tex_coord + sprite_width, 1)
    glVertex2d(rect.right, rect.top)

    glTexCoord2f(tex_coord, 1)
    glVertex2d(rect.left, rect.top)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, -1)


def draw():
    global test_rect
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT)

    # playAnimation(test_rect, 13)

    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(500, 500)
    glutCreateWindow(b"tex example")
    my_init()
    glutDisplayFunc(draw)
    glutMainLoop()


if __name__ == "__main__":
    main()
