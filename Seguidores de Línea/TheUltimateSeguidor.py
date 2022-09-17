from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
import hub as advancedHub
import math
from math import *

# INITIALIZATIONS
hub = PrimeHub()
motor_pair = MotorPair('C', 'A')
sen_1 = ColorSensor("B")
sen_2 = ColorSensor("D")
sen_3 = ColorSensor("F")

# MATRIXES
H = 9
L = 7
_ = 0

nada = [
    [_,_,_,_,_],
    [_,_,_,_,_],
    [_,_,_,_,_],
    [_,_,_,_,_],
    [_,_,_,_,_],
]

flecha_frente = [
    [_,_,H,_,_],
    [_,_,_,H,_],
    [H,H,H,H,H],
    [_,_,_,H,_],
    [_,_,H,_,_],
]

flecha_atras = [
    [_,_,H,_,_],
    [_,H,_,_,_],
    [H,H,H,H,H],
    [_,H,_,_,_],
    [_,_,H,_,_],
]

flecha_der = [
    [_,_,H,_,_],
    [_,_,H,_,_],
    [H,_,H,_,H],
    [_,H,H,H,_],
    [_,_,H,_,_],
]

flecha_izq = [
    [_,_,H,_,_],
    [_,H,H,H,_],
    [H,_,H,_,H],
    [_,_,H,_,_],
    [_,_,H,_,_],
]

cruz_h = [
    [_,_,H,_,_],
    [_,_,H,_,_],
    [H,H,H,H,H],
    [_,_,H,_,_],
    [_,_,H,_,_],
]

cruz_l = [
    [_,_,L,_,_],
    [_,_,L,_,_],
    [L,L,L,L,L],
    [_,_,L,_,_],
    [_,_,L,_,_],
]

verde = [
    [H,H,_,_,_],
    [_,_,H,H,_],
    [_,_,_,_,H],
    [_,_,H,H,_],
    [H,H,_,_,_],
]

verde_l = [
    [L,L,_,_,_],
    [_,_,L,L,_],
    [_,_,_,_,L],
    [_,_,L,L,_],
    [L,L,_,_,_],
]

buscar = [
    [H,H,H,_,_],
    [H,_,_,H,_],
    [H,H,H,_,_],
    [H,_,_,H,_],
    [H,H,H,_,_],
]

# FUNCTIONS
def avanzar(veli,veld):
    motor_pair.start_tank(veli,veld)

def girar_90_der():
    hub.motion_sensor.reset_yaw_angle()
    while (hub.motion_sensor.get_yaw_angle() < 88):
        motor_pair.start_tank(40, -35)
    motor_pair.start_tank(0, 0)
    hub.motion_sensor.reset_yaw_angle()

def girar_90_izq():
    hub.motion_sensor.reset_yaw_angle()
    while (hub.motion_sensor.get_yaw_angle() < -90):
        motor_pair.start_tank(-35, 40)
    motor_pair.start_tank(0, 0)
    hub.motion_sensor.reset_yaw_angle()

def girar_180_der():
    girar_90_der()
    girar_90_der()

def girar_180_izq():
    girar_90_izq()
    girar_90_izq()

def sound_emitter(num):
    for i in range(num):
        hub.speaker.beep(60, 0.5)

def show_image_on_display(matrix):
    return advancedHub.Image(":".join(["".join([str(n) for n in r]) for r in matrix]))

def green_verification():
    Gcolor_1 = sen_1.get_color()
    Gcolor_3 = sen_3.get_color()
    if (Gcolor_1 == 'green'):
        hub.light_matrix.show_image('HAPPY')
        motor_pair.move_tank(0.5, 'cm', 0, 10)
        if (Gcolor_1 == 'green'):
            if (Gcolor_1 == 'green') and (Gcolor_3 == 'green'):
                girar_180_der()
                hub.motion_sensor.reset_yaw_angle()
                while (hub.motion_sensor.get_yaw_angle() < 40):
                    motor_pair.start_tank(40, -35)
                motor_pair.start_tank(0, 0)
                hub.motion_sensor.reset_yaw_angle()
                motor_pair.move_tank(2,'cm',10, 10)
            elif (Gcolor_1 == 'green') and (Gcolor_3 != 'green'):
                motor_pair.move_tank(1.5, 'cm', 0, 10)
                girar_90_izq()
    elif (Gcolor_3 == 'green'):
        motor_pair.move_tank(0.5, 'cm',10, 0)
        if (Gcolor_3 == 'green'):
            if (Gcolor_1 == 'green') and (Gcolor_3 == 'green'):
                girar_180_izq()
                hub.motion_sensor.reset_yaw_angle()
                while (hub.motion_sensor.get_yaw_angle() < 40):
                    motor_pair.start_tank(-35, 40)
                motor_pair.start_tank(0, 0)
                hub.motion_sensor.reset_yaw_angle()
            elif (Gcolor_3 == 'green') and (Gcolor_1 != 'green'):
                motor_pair.move_tank(1.5, 'cm', 0, 10)
                girar_90_der()

def double_black():
    color_1 = sen_1.get_reflected_light()
    color_2 = sen_2.get_reflected_light()
    color_3 = sen_3.get_reflected_light()
    if (color_1 < 30) and (color_2 < 30) and (color_3 < 30):
        motor_pair.move_tank(2, 'cm', 20, 20)
        green_verification()

while True:
    color_1 = sen_1.get_reflected_light()
    color_2 = sen_2.get_reflected_light()
    color_3 = sen_3.get_reflected_light()
    Gcolor_1 = sen_1.get_color()
    Gcolor_3 = sen_3.get_color()

    # LINE FOLLOWER
    if Gcolor_1 == 'green' or Gcolor_3 == 'green':
        green_verification()
    elif (color_1 < 30) and (color_3 < 30):
        double_black()
    elif (color_3 < 30):
        motor_pair.start_tank(40,-25)
        double_black()
    elif (color_1 < 30):
        motor_pair.start_tank(-25,40)
    else:
        motor_pair.start_tank(100,100)