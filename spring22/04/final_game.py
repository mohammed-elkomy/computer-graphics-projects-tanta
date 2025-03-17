import sys
from math import *
from playsound import playsound
from OpenGL.GLU import *
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
import pygame

#######constants #######################
delta_time = 1
##############status########################
control_color = 0  # عشان نعمل تدرج الالوان في الخلفيه
minus_x = -100
positive_x = -95
######للطالب ####

step_boy = .15 # المقدار الي هيمشيه الطالب كل مره
Amount_of_acceleration = .0001  # للتحكم في مقدار التسارع الي هيحصل للطالب كل مايتقدم في الخطوات
x_boy = -94  # مكان الطالب في الاول
y_boy = -.7

#   الحواف بتاعت الطالب هيتعملها update في func_play
left_boy = 0
right_boy = 0
top_boy = 0
bottom_boy = 0
right_head = 0
left_head = 0

grades = 0

flag_sound = False
#### للحفرة #####
list_hole = [[-82, -81.4], [-52, -51.4], [2, 2.6], [32, 32.6], [72, 72.6]]  # اماكن الحفر متخزن فيها left & right لكل حفرة
flag_falling = False
flag_exit = False

# ####للطوب###
FONT_DOWNSCALE_x = .000975
FONT_DOWNSCALE_y = .001
top_bricks = .2
bottom_bricks = .05

list1_tecture = []
list_assi = []
list_quiz = []
list_bouns = []
list_attend = []
mid = [0, .5]
oral = [80, 80.35]
final = [94, 94.35]


# row بتعبر عن عدد الطوب الي من النوع الواحد
# start بتعبر عن الليفت بتاع الطوبة
# step بتعبر عن طول الطوبة
# step2  المقدار المطلوب للوصول للطوبة التاليه
def write_2d_arr(row, cols, start, step, step2, arr):
    for i in range(row):
        arr.append([0] * cols)

    for i in range(row):
        for j in range(cols):
            arr[i][j] = start
            start += step

        start += step2 - step
    return arr


list_assi = write_2d_arr(4, 2, -91, .7, 49.3, list_assi)
list_quiz = write_2d_arr(8, 2, -87, .3, 24.7, list_quiz)
list_bouns = write_2d_arr(10, 2, -92, .2, 14, list_bouns)
list_attend = write_2d_arr(10, 2, -93, .4, 9, list_attend)

#### للاعداء###

x = 0
bottom = 0
top_anmy = -.8
dir = .5  # الطول الي مسموح بيه العدو يتحرك فيه ذهابا وايابا
step_animy = .1 # المقدار الي هيمشي بيه

facebook = []
twiteer = []
instgram = []
tiktok = []
youtube = []

facebook = write_2d_arr(4, 2, -90.1, .2, 49.8, facebook)
twiteer = write_2d_arr(4, 2, -80.1, .2, 49.8, twiteer)
instgram = write_2d_arr(4, 2, -60.1, .2, 49.8, instgram)
tiktok = write_2d_arr(4, 2, -56.7, .2, 49.8, tiktok)
youtube = write_2d_arr(4, 2, -70.1, .2, 49.8, youtube)


incr_decr_values={"fac_value":-.2,"youtube_value":-.3,"tiktok_value":-.1,"instgram_value":-.2,"twiteer":-.1,
                  "assi_vaue":10,"quiz_value":5,"bouns_value":.5,"attendanc_value":.5,
                  "mid_value":20,"oral_value":30,"final_value":50}

#####################################################################################################################################
circle_memo = {}
# KOMY: I optimized this  # ظهر مشكلة في رسم الانستجرام والتيك توك
def draw_circle(r, delta_x=0, delta_y=0, start_ang=0, end_ang=360, resolution=1, scale_x=1, scale_y=1, type=GL_POLYGON):
    glBegin(type)
    for ang in np.arange(start_ang, end_ang, resolution):
        if (scale_x, scale_y, ang,resolution,start_ang, end_ang,) not in circle_memo:
            x = scale_x * r * cos(ang * pi / 180)
            y = scale_y * r * sin(ang * pi / 180)
            circle_memo[(scale_x, scale_y, ang,resolution,start_ang, end_ang,)] = (x, y)

        x, y = circle_memo[(scale_x, scale_y, ang,resolution,start_ang, end_ang,)]
        x += delta_x
        y += delta_y

        glVertex(x, y)
    glEnd()
"""
def draw_circle(r, delta_x=0, delta_y=0, start_ang=0, end_ang=360, resolution=1, scale_x=1, scale_y=1, type=GL_POLYGON):
    glBegin(type)
    for ang in np.arange(start_ang, end_ang, resolution):
        x = scale_x * r * cos(ang * pi / 180) + delta_x
        y = scale_y * r * sin(ang * pi / 180) + delta_y
        glVertex(x, y)
    glEnd()
"""
def text(str, x, y):
    global FONT_DOWNSCALE_x, FONT_DOWNSCALE_y
    glLineWidth(3)
    glColor(1, 1, 1)
    glPushMatrix()
    str = str.encode()
    glLoadIdentity()
    glTranslate(x, y, 0)
    glScale(FONT_DOWNSCALE_x, FONT_DOWNSCALE_y, 1)
    for i in str:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, i)
    glPopMatrix()


def time_fun(var):
    print(var)
    play()
    glutTimerFunc(delta_time, time_fun, var + 1)


def keyboard_callback(key, x, y):
    global minus_x, positive_x, x_boy, y_boy,step_boy
    if flag_exit == False:

        if key == GLUT_KEY_RIGHT and 94.7 > minus_x >= -95:  # عشان ميعرفش يدخل اللعبه بالزرار ده
            minus_x += step_boy
            minus_x = min(minus_x, 90)  # عشان لما يقرب من الفاينل  صورة جيم اوفر ماتبقاش موجوده جنبه
            positive_x += step_boy
            positive_x = min(positive_x, 95)  # عشان لما يقرب من الفاينل  صورة جيم اوفر ماتبقاش موجوده جنبه
            x_boy += step_boy
            step_boy+=Amount_of_acceleration            # للتسارع
            print("GLUT_KEY_RIGHT")
            
        if key == b'a':  # عشان ينط
            if y_boy <= -.55:  # الشرط ده عشان مايقدرش انو يبقي فوق زي الطاير عليطول ويبقي اللعبه فيها هاك
                y_boy += .5

            y_boy = min(y_boy, -.2)  # استخدمت min عشان لو نط تاني مايقدش يطلع لفوق اكبر من مقدار معين
            print("a")
            
        if key == b'\r':  # عشان يدخل اللعبه
            # الشرط ده عشان لو  الاعب ضغط c في نص اللعبه
            if minus_x < -95:
                minus_x += 5
                positive_x += 5

    else:  # عشان في حالة الوقوع في الحفرة ايا كان الحرف الي هيضغط عليه يطلع من البرنامج
        pygame.quit()
        sys.exit()

def adjust_view():    # KOMY: I optimized this
    global control_color

    glClearColor(control_color, control_color, control_color, 0)
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    #glOrtho(-100, 100, -2, 2,-2,2) #try it to see full points
    glOrtho(min(minus_x, 95), min(positive_x, 100), -2, 2, -2, 2)  # استخدمت min عشان مايخرجش برا المكان المرسوم فيه  لما يخلص الللعبه

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 0,
              0, 0, -1,
              0, 1, 0)


def init_texture():
    loadTextures()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


texture_names = [0, 1, 2, 3, 4]

def loadTextures():
    glEnable(GL_TEXTURE_2D)

    images = []
    images.append(pygame.image.load("welcome.jpeg"))
    images.append(pygame.image.load("ground.jpg"))
    images.append(pygame.image.load("trees.png"))
    images.append(pygame.image.load("falling.jpeg"))
    images.append(pygame.image.load("game_over.jpg"))

    textures = [pygame.image.tostring(image, "RGBA", True)
                for image in images]

    glGenTextures(len(images), texture_names)

    for i in range(len(images)):
        texture_setup(textures[i],
                      texture_names[i],
                      images[i].get_width(),
                      images[i].get_height())


def texture_setup(texture_image_binary, texture_name, width, height):
    glBindTexture(GL_TEXTURE_2D, texture_name)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    glTexImage2D(GL_TEXTURE_2D,
                 0,
                 GL_RGBA,
                 width, height,
                 0,
                 GL_RGBA,
                 GL_UNSIGNED_BYTE,
                 texture_image_binary)


def draw_scene():
    global flag_exit, flag_sound

    glColor3f(1, 1, 1)

    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_names[0])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2d(-100, 2)

    glTexCoord2f(1, 1)
    glVertex2d(-95, 2)

    glTexCoord2f(1.0, 0)
    glVertex2d(-95, -2)

    glTexCoord2f(0, 0)
    glVertex2d(-100, -2)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, texture_names[1])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2d(-95, -1)

    glTexCoord2f(1, 1)
    glVertex2d(list_hole[0][0], -1)

    glTexCoord2f(1.0, 0)
    glVertex2d(list_hole[0][0], -2)

    glTexCoord2f(0, 0)
    glVertex2d(-95, -2)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, texture_names[1])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2d(list_hole[0][1], -1)

    glTexCoord2f(1, 1)
    glVertex2d(list_hole[1][0], -1)

    glTexCoord2f(1.0, 0)
    glVertex2d(list_hole[1][0], -2)

    glTexCoord2f(0, 0)
    glVertex2d(list_hole[0][1], -2)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, texture_names[1])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2d(list_hole[1][1], -1)

    glTexCoord2f(1, 1)
    glVertex2d(list_hole[2][0], -1)

    glTexCoord2f(1.0, 0)
    glVertex2d(list_hole[2][0], -2)

    glTexCoord2f(0, 0)
    glVertex2d(list_hole[1][1], -2)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, texture_names[1])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2d(list_hole[2][1], -1)

    glTexCoord2f(1, 1)
    glVertex2d(list_hole[3][0], -1)

    glTexCoord2f(1.0, 0)
    glVertex2d(list_hole[3][0], -2)

    glTexCoord2f(0, 0)
    glVertex2d(list_hole[2][1], -2)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, texture_names[1])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2d(list_hole[3][1], -1)

    glTexCoord2f(1, 1)
    glVertex2d(list_hole[4][0], -1)

    glTexCoord2f(1.0, 0)
    glVertex2d(list_hole[4][0], -2)

    glTexCoord2f(0, 0)
    glVertex2d(list_hole[3][1], -2)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, texture_names[1])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2d(list_hole[4][1], -1)

    glTexCoord2f(1, 1)
    glVertex2d(95, -1)

    glTexCoord2f(1.0, 0)
    glVertex2d(95, -2)

    glTexCoord2f(0, 0)
    glVertex2d(list_hole[4][1], -2)
    glEnd()

    # draw trees
    glBindTexture(GL_TEXTURE_2D, texture_names[2])
    for i in range(-90, 95, 5):
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex2d(i, 0)

        glTexCoord2f(1, 1)
        glVertex2d(i + .5, 0)

        glTexCoord2f(1.0, 0)
        glVertex2d(i + .5, -1.3)

        glTexCoord2f(0, 0)
        glVertex2d(i, -1.3)
        glEnd()

    if flag_falling == True:
        glBindTexture(GL_TEXTURE_2D, texture_names[3])
    else:
        glBindTexture(GL_TEXTURE_2D, texture_names[4])

    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2d(95, 1.2)

    glTexCoord2f(1, 1)
    glVertex2d(100, 1.2)

    glTexCoord2f(1.0, 0)
    glVertex2d(100, -1.2)

    glTexCoord2f(0, 0)
    glVertex2d(95, -1.2)
    glEnd()

    if flag_falling == True:
        flag_exit = True  # عشان البرنامج يقف لو وقع في الحفرة
    else:
        if minus_x == 95 and positive_x == 100:
            flag_sound = True

    glPopMatrix()

    # glDeleteTextures(5, texture_names)
    # السطر ده مهم اويييييييييييييييييييييييييييي عشان من غيره كل الرسم هيبقي اسود
    # glDisable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, -1)


def draw_student():
    # face
    glColor3d(9.06, .74, .67)
    draw_circle(r=.2, delta_y=.4, resolution=.6, scale_y=.8)

    # eyef
    glColor3d(0, 0, 0)
    glLineWidth(1.5)
    draw_circle(r=.05, delta_x=.11, delta_y=.42, resolution=.01, scale_y=1.3)

    # eye
    glColor3d(1, 1, 1)
    draw_circle(r=.045, delta_x=.11, delta_y=.42, resolution=.05, scale_y=1.3)

    # smile
    glColor3d(0, 0, 0)
    draw_circle(r=.093, delta_x=.1, delta_y=.38, start_ang=230, end_ang=330, resolution=.5, type=GL_LINE_STRIP)

    # nose
    glColor3d(0, 0, 0)
    draw_circle(r=.025, delta_x=.17, delta_y=.337, start_ang=-30, end_ang=60, resolution=.5, type=GL_LINE_STRIP)

    # eyeiner
    glColor4f(0.0, 1.0, 1.0, 1.0)
    draw_circle(r=.03, delta_x=.13, delta_y=.42, resolution=.05, scale_x=.9, scale_y=1.3)

    # eye1
    glColor3d(0, 0, 0)
    draw_circle(r=.01, delta_x=.13, delta_y=.42, resolution=.5, scale_y=1.3)

    # hair
    glColor(0, 0, 0)
    draw_circle(r=.2, delta_x=0, delta_y=.4, start_ang=80, end_ang=205, resolution=.6, scale_y=.8)

    glColor3d(.7, 0, 0)
    draw_circle(r=.2, delta_x=0, delta_y=.4, start_ang=40, end_ang=180, resolution=.6, scale_y=.8)

    glLineWidth(9)
    glBegin(GL_LINES)
    glVertex2d(.05, .5)
    glVertex2d(.3, .5)
    glEnd()

    # body
    glColor3d(0.8, 0.75, 0.4)
    glBegin(GL_POLYGON)
    glVertex2d(-.136, 0.17)
    glVertex2d(-.136, -.13)
    glVertex2d(-.186, -.13)
    glVertex2d(-.186, 0.17)
    glVertex2d(-.336, 0.17)
    glVertex2d(-.336, 0.22)
    glVertex2d(.084, 0.22)
    glVertex2d(.084, 0.17)

    glEnd()
    glColor3d(9.06, .74, .67)
    glBegin(GL_POLYGON)
    glVertex2d(.05, .28)
    glVertex2d(.05, 0.12)
    glVertex2d(-.05, 0.12)
    glVertex2d(-.05, .28)
    glEnd()

    glColor3d(.7, 0, 0)
    glBegin(GL_POLYGON)
    glVertex2d(.05, 0.2)
    glVertex2d(.2, 0.02)
    glVertex2d(.18, -0.28)
    glVertex2d(-.18, -0.28)
    glVertex2d(-.2, 0.02)
    glVertex2d(-.05, .2)
    glEnd()

    glColor3d(0, 0, 0)
    glBegin(GL_POLYGON)

    glVertex2d(.18, -0.28)
    glVertex2d(.18, -.32)
    glVertex2d(-.18, -.32)
    glVertex2d(-.18, -0.28)

    glEnd()

    glColor3d(9.06, .74, .67)
    glBegin(GL_POLYGON)
    glVertex2d(.05, 0.2)
    glVertex2d(0, .12)
    glVertex2d(-.05, 0.2)
    glEnd()

    glColor3d(.7, 0, 0)
    glBegin(GL_POLYGON)
    glVertex2d(.2, 0.02)
    glVertex2d(.15, 0.02)
    glVertex2d(.35, -.30)
    glVertex2d(.40, -.30)
    glEnd()

    glColor3d(.7, 0, 0)
    glBegin(GL_POLYGON)
    glVertex2d(-.2, 0.02)
    glVertex2d(-.15, 0.02)
    glVertex2d(-.35, -.30)
    glVertex2d(-.40, -.30)
    glEnd()

    glColor3d(0, 0, 0)
    glBegin(GL_POLYGON)
    glVertex2d(.18, -.28)
    glVertex2d(.48, -.48)
    glVertex2d(.32, -.48)
    glVertex2d(.005, -.28)
    glEnd()

    glColor3d(0, 0, 0)
    glBegin(GL_POLYGON)
    glVertex2d(-.005, -.28)
    glVertex2d(-.22, -.62)
    glVertex2d(-.38, -.62)
    glVertex2d(-.18, -.28)
    glEnd()

    glColor3d(.7, 0, 0)
    glBegin(GL_POLYGON)
    glVertex2d(-.18, -.62)
    glVertex2d(-.35, -.62)
    glVertex2d(-.35, -.68)
    glVertex2d(-.18, -.68)
    glEnd()

    glColor3d(.7, 0, 0)
    glBegin(GL_POLYGON)
    glVertex2d(0.53, -.48)
    glVertex2d(.36, -.48)
    glVertex2d(.36, -.54)
    glVertex2d(.53, -.54)

    glEnd()


########################################### to draw assi & quiz & +1& attend & mid & oral& final####################
class rectangle:
    def __init__(self, left_x, bottom_y, right_x, top_y):
        self.left_x = left_x
        self.right_x = right_x
        self.top_y = top_y
        self.bottom_y = bottom_y

    def draw_rect(self):
        glLoadIdentity()
        glColor(.5, 0, 0)
        glBegin(GL_QUADS)
        glVertex(self.left_x, self.top_y)
        glVertex(self.left_x, self.bottom_y)
        glVertex(self.right_x, self.bottom_y)
        glVertex(self.right_x, self.top_y)
        glEnd()


class rect2(rectangle):

    def __init__(self, left_x, bottom_y, right_x, top_y, str):
        super().__init__(left_x, bottom_y, right_x, top_y)
        self.str = str

    def draw_text(self):
        y = (self.top_y + self.bottom_y) / 2 - .03  # عاوز أكتب الtext في نص المستطيل
        x = self.left_x
        text(self.str, x, y)


def bricks(str, arr):  # to draw assi & quiz & +1& attend

    if len(arr) != 0:
        for i in range(len(arr)):
            block = rect2(arr[i][0], bottom_bricks, arr[i][1], top_bricks, str)
            block.draw_rect()
            block.draw_text()


def mid_oral_final():  # to draw mid & oral & final

    if len(mid) != 0:
        block_m = rect2(mid[0], bottom_bricks, mid[1], top_bricks, "Midterm")
        block_m.draw_rect()
        block_m.draw_text()

    if len(oral) != 0:
        block_o = rect2(oral[0], bottom_bricks, oral[1], top_bricks, "Oral")
        block_o.draw_rect()
        block_o.draw_text()

    if len(final) != 0:
        block_f = rect2(final[0], bottom_bricks, final[1], top_bricks, "Final")
        block_f.draw_rect()
        block_f.draw_text()


def draw_bricks():
    global list_attend, list_assi, list_attend, list_quiz

    glLoadIdentity()
    bricks("Assignment", list_assi)  # for assignment

    glLoadIdentity()
    bricks("quiz", list_quiz)  # for quiz

    glLoadIdentity()
    bricks("+1", list_bouns)  # for bouns

    glLoadIdentity()
    bricks("attend", list_attend)  # for attendance

    glLoadIdentity()
    mid_oral_final()


#######################################to draw Enemies and control it ########################################
def animate(left_xrange):
    global x
    glLoadIdentity()
    glTranslate(left_xrange + x, -.9, 0)
    glScale(.2, .2, 0)


def Enemies():
    global x, dir

    if x < 0 or x > abs(dir):
        dir = -dir
    x = x + dir * step_animy
    for i in range(0, 4):
        animate(facebook[i][0] + .1)
        facebooklogo()

        animate(twiteer[i][0] + .1)
        twiteerlogo()

        animate(youtube[i][0] + .1)
        youtubelogo()

        animate(instgram[i][0] + .1)
        instgramlogo()

        animate(tiktok[i][0] + .1)
        tiktoklogo()


def twiteerlogo():
    glBegin(GL_QUADS)
    glColor3ub(0, 200, 255)
    glVertex(.5, .5)
    glVertex(.5, -.5)
    glVertex(-.5, -.5)
    glVertex(-.5, .5)
    glEnd()

    glColor3d(1, 1, 1)
    draw_circle(.4, 0, 0, 230, 370)  # body
    draw_circle(.26, -.16, -.13, 210, 313)

    draw_circle(.21, -.14, -.03, 174, 300)  # 1st wing
    draw_circle(.21, -.06, 0, 245, 288)

    draw_circle(.21, -0.04, 0.02, 150, 290)  # 2nd wing
    draw_circle(.21, -.17, .13, 220, 283)

    draw_circle(.36, .06, .11, 158, 261)  # 3d wing
    draw_circle(.55, .14, .39, 213, 300)

    draw_circle(.21, .19, 0, 0, 230)  # head

    draw_circle(.21, .27, .26, 270, 346)  # 1st منقار
    draw_circle(.22, .29, .33, 245, 328)

    draw_circle(.21, .27, .14, 290, 360)  # 2nd منقار
    draw_circle(.22, .25, .18, 242, 340)


def youtubelogo():
    glBegin(GL_QUADS)
    glColor3d(1, 1, 1)
    glVertex(.5, .5)
    glVertex(.5, -.5)
    glVertex(-.5, -.5)
    glVertex(-.5, .5)
    glEnd()

    glBegin(GL_QUADS)
    glColor3d(1, 0, 0)
    glVertex(.4, .3)
    glVertex(.4, -.3)
    glVertex(-.4, -.3)
    glVertex(-.4, .3)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3d(1, 1, 1)
    glVertex(.15, 0)
    glVertex(-.15, -.15)
    glVertex(-.15, .15)
    glEnd()


def tiktoklogo():
    glScale(1.5, 1.5, 1)

    glColor3f(0, 0, 0)
    draw_circle(r=.3, resolution=.6)



    glColor3f(0, 0, 0)
    draw_circle(r=.05, resolution=.6)

    glColor3f(1, 1, 1)
    glBegin(GL_POLYGON)
    glVertex2d(.075, -.045)
    glVertex2d(.075, .13)
    glVertex2d(.05, .13)
    glVertex2d(.05, -.045)
    glEnd()

    glColor3f(1, 1, 1)
    draw_circle(r=.09, delta_x=.14, delta_y=.13, start_ang=180, end_ang=270, resolution=.5)

    glColor3f(0, 0, 0)
    draw_circle(r=.05, delta_x=.125, delta_y=.117, start_ang=180, end_ang=270, resolution=.07)

    glColor3f(1, 1, 1)
    draw_circle(r=.089, start_ang=90, end_ang=310, resolution=.1,type=GL_POINTS)


def instgramlogo():
    glScale(.5, .5, .5)
    glColor(.7, 0, .4, 1)
    glBegin(GL_POLYGON)
    glVertex2d(1, 1)
    glVertex2d(1, -1)
    glVertex2d(-1, -1)
    glVertex2d(-1, 1)
    glEnd()

    glLineWidth(3)
    glColor(1, 1, 1)
    glBegin(GL_LINE_LOOP)
    glVertex2d(.5, .5)
    glVertex2d(.5, -.5)
    glVertex2d(-.5, -.5)
    glVertex2d(-.5, .5)
    glEnd()



    draw_circle(r=.25,type=GL_LINE_LOOP)
    #glColor(.7, 0, .4, 0)
    #draw_circle(r=.17)
    glColor(1, 1, 1)
    draw_circle(r=.008, delta_x=.35, delta_y=.35)



def facebooklogo():
    glColor(0, 0, 1)
    glBegin(GL_POLYGON)
    glVertex2d(.5, .5)
    glVertex2d(.5, -.5)
    glVertex2d(-.5, -.5)
    glVertex2d(-.5, .5)
    glEnd()

    glColor(1, 1, 1)
    glLineWidth(5)  #
    glBegin(GL_LINES)
    glVertex2d(.25, .3)
    glVertex2d(0, .3)

    glVertex2d(.25, 0)
    glVertex2d(-.2, 0)

    glVertex2d(0, .35)
    glVertex2d(0, -.4)

    glEnd()

###############################################################################################################################

def write_score():
    global minus_x, positive_x
    string = "Your grades =  " + str(grades) + " : 200"
    if x_boy < 94.7:  # علي طول اللعبه
        text(string, max(minus_x + .5, -94.5), 1.5)
    else:  # لما يخلص اللعبه
        minus_x = 95
        positive_x = 100
        string = "YOUR GRADES = " + str(grades) + " : 200 "
        text(string, 95.5, 1.5)

def sound():
    global flag_sound
    if flag_sound == True:
        if grades < 100:
            playsound('ya_sagt.mp3')
        else:
            playsound('win.mp3')

##############################################################################################################

def falling_hole():
    global left_boy, right_boy, flag_falling, step_boy, x_boy
    for i in range(len(list_hole)):
        if list_hole[i][0] <= right_boy <= list_hole[i][1] and bottom_boy <= -1.04:  # اول لما رجله اليمين تدخل الحفرة هيقع
            flag_falling = True
            step_boy = 0
            x_boy = list_hole[i][0]


##########################################################################################################
# to control score###########
def binary_search(alist):  # بترجع ال index بتاع العنصر الي اصغر من left_head بالظبط
    left = 0
    righ = len(alist) - 1
    while left <= righ:
        mid = (righ + left) // 2
        if left_head <= alist[0][0]:  # الشرط ده عشان لو الطالب موجود قبل اول طوبه
            return -1
        elif left_head >= alist[len(alist) - 1][
            0]:  # الشرط ده عشان لو العنصر الي احنا بندور عليه طلع  اخر عنصر في الليست
            return len(alist) - 1
        elif left_head >= alist[mid][0] and left_head < alist[mid + 1][0]:
            return mid
        elif left_head < alist[mid][0]:
            righ = mid - 1
        elif left_head > alist[mid][0]:
            left = mid + 1


def control_score(alist, value):
    global grades, control_color
    temp = binary_search(alist)
    if temp != -1:
        if (right_head <= alist[temp][1]) and top_boy >= bottom_bricks:
            control_grades(value)
            del alist[temp]  # عملت دلييت عشان الاسكور مايزيدش غير في مره واحده لما يخبط فيها الاعب الطوبه


def gain_score():
    global grades, control_color

    if len(list_assi) != 0:
        control_score(list_assi,incr_decr_values["assi_vaue"])

    if len(list_quiz) != 0:
        control_score(list_quiz, incr_decr_values["quiz_value"])

    if len(list_bouns) != 0:
        control_score(list_bouns, incr_decr_values["bouns_value"])

    if len(list_attend) != 0:
        control_score(list_attend, incr_decr_values["attendanc_value"])

    if len(mid) != 0:
        if (left_head >= mid[0] and right_head <= mid[1]) and top_boy >= bottom_bricks:
            control_grades(incr_decr_values["mid_value"])
            mid.clear()

    if len(oral) != 0:
        if (left_head >= oral[0] and right_head <= oral[1]) and top_boy >= bottom_bricks:
            control_grades(incr_decr_values["oral_value"])
            oral.clear()
    if len(final) != 0:
        if (left_head >= final[0] and right_head <= final[1]) and top_boy >= bottom_bricks:
            control_grades(incr_decr_values["final_value"])
            final.clear()


##########################################################################################################################
def control_grades(value):
    global x, grades, control_color
    grades = max(0, grades + value)  # max عشان لو لسه ماخدش درجات ماتبقاش درجاته بالسالب
    grades = round(grades, 1)
    if value>0:
        control_color = max(0, control_color + .02)
    else:
        control_color = max(0, control_color - .002)


def contol_enemies():
    for i in range(4):
        if (top_anmy >= bottom_boy) and (
                (left_boy <= facebook[i][0] + x <= right_boy) or (left_boy <= facebook[i][1] + x <= right_boy)):
            control_grades(incr_decr_values["fac_value"])
            break

        elif (top_anmy >= bottom_boy) and (
                (left_boy <= youtube[i][0] + x <= right_boy) or (left_boy <= youtube[i][1] + x <= right_boy)):
            control_grades(incr_decr_values["youtube_value"])
            break

        elif (top_anmy >= bottom_boy) and (
                (left_boy <= tiktok[i][0] + x <= right_boy) or (left_boy <= tiktok[i][1] + x <= right_boy)):
            control_grades(incr_decr_values["tiktok_value"])
            break

        elif (top_anmy >= bottom_boy) and (
                (left_boy <= instgram[i][0] + x <= right_boy) or (left_boy <= instgram[i][1] + x <= right_boy)):
            control_grades(incr_decr_values["instgram_value"])
            break

        elif (top_anmy >= bottom_boy) and (
                (left_boy <= twiteer[i][0] + x <= right_boy) or (left_boy <= twiteer[i][1] + x <= right_boy)):
            control_grades(incr_decr_values["twiteer"])
            break

##################################################################################################################################################3
def play():
    global x_boy, y_boy, left_boy, right_boy, top_boy, bottom_boy, right_head, left_head, x, flag_falling, flag_exit, flag_sound, minus_x, positive_x

    left_boy = x_boy - .18
    right_boy = x_boy + .27
    top_boy = y_boy + .29
    bottom_boy = y_boy - .34
    right_head = x_boy + .01
    left_head = x_boy - .0

    adjust_view()

    sound()

    glLoadIdentity()
    draw_scene()

    glLoadIdentity()
    glTranslate(min(x_boy, 94.7), y_boy, 0)  # استخدمت  min at x_boy عشان الطالب مايخرجش برا الفرستم في اخر اللعبه
    glScale(.5, .5, 0)
    if flag_falling == True:  # عشان الولد يتقلب لو وقع في الحفرة
        minus_x = 95
        positive_x = 100
        glTranslate(.6, -1.5, 0)
        glRotate(167, 0, 0, -1)
    draw_student()

    glLoadIdentity()
    draw_bricks()

    glLoadIdentity()
    Enemies()

    glLoadIdentity()
    write_score()

    falling_hole()

    gain_score()

    contol_enemies()

    if y_boy > -.7:  # الشرط ده عشان ينزل بعد النطه وبتدرجفي النزول مش مره واحده
        y_boy -= .05
        
        
    """glColor(1,1,1) 
    glLineWidth(.5)
    glBegin(GL_LINES)
    glVertex2d(left_boy,top_boy)
    glVertex2d(left_boy,bottom_boy)

    glVertex2d(right_boy,top_boy)
    glVertex2d(right_boy,bottom_boy)

    glVertex2d(right_boy,bottom_boy)
    glVertex2d(left_boy,bottom_boy)

    glVertex2d(right_boy,top_boy)
    glVertex2d(left_boy,top_boy)

    glVertex2d(left_head, top_boy)
    glVertex2d(left_head, bottom_boy)

    glVertex2d(right_head, top_boy)
    glVertex2d(right_head, bottom_boy)

    glEnd()"""
    glutSwapBuffers()

if __name__ == '__main__':
    glutInit()
    glutInitWindowSize(1000, 1000)
    glutInitWindowPosition(0, 0)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutCreateWindow(b"Reality Simulation ")
    glutDisplayFunc(play)
    glutKeyboardFunc(keyboard_callback)
    glutSpecialFunc(keyboard_callback)  # علشان GLUT_KEY_RIGHT
    glutTimerFunc(delta_time, time_fun, 1)
    init_texture()
    glutMainLoop()

