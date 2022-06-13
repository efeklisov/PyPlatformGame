import glm
from math import sin, cos
from app_state import app_state, init_app_state, delete_app_state
from render.shaders import ShaderManager
from ui_descr import menu_ui, pause_ui, game_ui
from scene import Scene, Light, Camera
from renderer import draw
import pygame as pg


sound = 0.5
music = 0.5
def sound_callback(l: float):
    global sound
    sound = l
    print('Sound', l)
def music_callback(l: float):
    global music
    music = l
    print('Music', l)



MENU = 1
GAME = 2
PAUSE = 3
cur_state = MENU
prev_state = MENU
should_stop = False
def exit_callback():
    global should_stop
    should_stop = True

def play_callback():
    global cur_state
    cur_state = GAME

def menu_callback():
    global cur_state
    cur_state = MENU




pos = glm.vec3(0.0, 0.0, 0.0)
dir = glm.vec3(0.0, 0.0, -1.0)
x_rot = 0
y_rot = 0
mouse_x = None
mouse_y = None
def process_mouse():
    x, y = pg.mouse.get_pos()
    global mouse_x
    global mouse_y
    if (mouse_x is not None) and (mouse_y is not None):
        delta_x = x - mouse_x
        delta_y = y - mouse_y
        global x_rot
        global y_rot
        x_rot -= delta_x * 0.01
        y_rot -= delta_y * 0.01
    global dir
    dir = glm.vec3(sin(x_rot) * cos(y_rot), sin(y_rot), cos(x_rot) * cos(y_rot))
    mouse_x = x
    mouse_y = y

scene = None
def process_keyboard():
    global cur_state
    global scene
    keys = pg.key.get_pressed()
    global pos
    if keys[pg.K_w]:
        pos += dir * 0.001
    elif keys[pg.K_s]:
        pos -= dir * 0.001
    elif keys[pg.K_r]:
        app_state().shader_manager = ShaderManager('shaders')
        scene = Scene('assets/scene.json')
    elif keys[pg.K_ESCAPE]:
        cur_state = PAUSE

def logic():
    global should_stop
    if cur_state == GAME:
        process_keyboard()
        process_mouse()
    for s in interface.sliders:
        s.process_input()
    for e in pg.event.get():
        if e.type == pg.QUIT:
            should_stop = True
        else:
            for b in interface.buttons:
                b.process_event(e)

pg.init()
pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 4)
pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 1)
pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
pg.display.set_mode((1920, 1080), pg.OPENGL|pg.DOUBLEBUF)
init_app_state((1920, 1080), 'shaders', 'assets/textures', 'assets/meshes')
interface = menu_ui(play_callback, exit_callback, sound_callback, music_callback, (sound, music))
scene = Scene('assets/scene.json')
FPS = 60
clock = pg.time.Clock()
while True:
    if cur_state != prev_state:
        if cur_state == MENU:
            interface = menu_ui(play_callback, exit_callback, sound_callback, music_callback, (sound, music))
        elif cur_state == PAUSE:
            interface = pause_ui(play_callback, menu_callback, sound_callback, music_callback, (sound, music))
        elif cur_state == GAME:
            interface = game_ui()
        prev_state = cur_state
    clock.tick(FPS)
    scene.before_render()
    # scene.add_bilboard('test.png', (0.05, 0.05), (0.1, 0.1))
    logic()
    if should_stop:
        break
    draw(scene, interface, Camera(pos, dir))
    pg.display.flip()
interface = None
delete_app_state()
pg.quit()