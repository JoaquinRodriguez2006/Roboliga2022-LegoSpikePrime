from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
import hub as advancedHub
import math
from math import *

# INITIALIZATIONS
hub = PrimeHub()
motor_pair = MotorPair('C', 'A')
motor_pair.set_motor_rotation(1.07 * math.pi, 'cm')
distance = DistanceSensor('E')
obstacle_detector = DistanceSensor('E')
sen_1 = ColorSensor("B")
sen_2 = ColorSensor("D")
sen_3 = ColorSensor("F")

# Sensor F = Derecho
# Sensor B = Izquierdo
# Sensor D = Medio

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

def girar_45_der():
    hub.motion_sensor.reset_yaw_angle()
    while (hub.motion_sensor.get_yaw_angle() < 45):
        motor_pair.start_tank(40, -35)
    motor_pair.start_tank(0, 0)
    hub.motion_sensor.reset_yaw_angle()

def girar_45_izq():
    hub.motion_sensor.reset_yaw_angle()
    while (hub.motion_sensor.get_yaw_angle() < -45):
        motor_pair.start_tank(-35, 40)
    motor_pair.start_tank(0, 0)
    hub.motion_sensor.reset_yaw_angle()

def girar_90_der():
    girar_45_der()
    girar_45_der()

def girar_90_izq():
    girar_45_izq()
    girar_45_izq()

def girar_180_der():
    girar_45_der()
    girar_45_der()
    girar_45_der()
    girar_45_der()

def girar_180_izq():
    girar_45_izq()
    girar_45_izq()
    girar_45_izq()
    girar_45_izq()

def girar_num_grados_der(num):
    hub.motion_sensor.reset_yaw_angle()
    while (hub.motion_sensor.get_yaw_angle() < num):
        motor_pair.start_tank(40, -35)
    motor_pair.start_tank(0, 0)
    hub.motion_sensor.reset_yaw_angle()

def girar_num_grados_izq(num):
    hub.motion_sensor.reset_yaw_angle()
    while (hub.motion_sensor.get_yaw_angle() < num):
        motor_pair.start_tank(-35, 40)
    motor_pair.start_tank(0, 0)
    hub.motion_sensor.reset_yaw_angle()

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
        motor_pair.move_tank(2, 'cm', 0, 10)
        if (Gcolor_1 == 'green') and (Gcolor_3 == 'green'):
            girar_180_der()
        elif (Gcolor_1 == 'green') and (Gcolor_3 != 'green'):
            motor_pair.move_tank(3, 'cm', -15, 50)
            girar_45_izq()
    elif (Gcolor_3 == 'green'):
        motor_pair.move_tank(2, 'cm',10, 0)
        if (Gcolor_1 == 'green') and (Gcolor_3 == 'green'):
            motor_pair.move_tank(20,'cm',10, 10)
            girar_180_izq()
        elif (Gcolor_3 == 'green') and (Gcolor_1 != 'green'):
            motor_pair.move_tank(3, 'cm', 50, -15)
            girar_45_der()

def double_black():
    color_1 = sen_1.get_reflected_light()
    color_2 = sen_2.get_reflected_light()
    color_3 = sen_3.get_reflected_light()
    if (color_1 < 30) and (color_2 < 30) and (color_3 < 30):
        motor_pair.move_tank(2, 'cm', 20, 20)
        green_verification()

def obstacle_detection():
    dist_cm = get_distance()
    color_3 = sen_3.get_reflected_light()
    color_3_c = sen_3.get_color()
    if ((dist_cm) < 6):
        hub.light_matrix.show_image('HAPPY')
        motor_pair.move_tank(4, 'cm', -10, -10)
        girar_num_grados_der(80)
        motor_pair.move_tank(3, 'cm', -6, 15)
        dist_cm = get_distance()
        if (dist_cm > 30):
            hub.light_matrix.show_image('HEART')
            while (color_3 > 50):
                color_3 = sen_3.get_reflected_light()
                motor_pair.start_tank(30, 80)
            motor_pair.start_tank(0, 0)
            girar_num_grados_der(40)
        else:
            hub.light_matrix.show_image('ANGRY')
            girar_num_grados_der(39)
            girar_num_grados_der(39)
            hub.motion_sensor.reset_yaw_angle()
            angle = hub.motion_sensor.get_yaw_angle()
            print("Angulo:", angle)
            while (hub.motion_sensor.get_yaw_angle() > -159):
                motor_pair.start_tank(-35, 40)
                angle = hub.motion_sensor.get_yaw_angle()
                print("Angulo:", angle)
            motor_pair.start_tank(0, 0)
            hub.motion_sensor.reset_yaw_angle()
            while (color_3 > 50):
                color_3 = sen_3.get_reflected_light()
                motor_pair.start_tank(80, 26)
            motor_pair.start_tank(0, 0)
            motor_pair.move_tank(3, 'cm', 10, -10)
            girar_num_grados_der(60)

def get_distance():
    dist_cm = obstacle_detector.get_distance_cm()
    if (dist_cm == None):
        dist_cm = 200
    return dist_cm

while True:
    color_1 = sen_1.get_reflected_light()
    color_2 = sen_2.get_reflected_light()
    color_3 = sen_3.get_reflected_light()
    Gcolor_1 = sen_1.get_color()
    Gcolor_3 = sen_3.get_color()
    dist_cm = get_distance()

    # LINE FOLLOWER
    if Gcolor_1 == 'green' or Gcolor_3 == 'green':
        green_verification()
    elif (color_1 < 30) and (color_3 < 30):
        double_black()
    elif (color_3 < 30):
        motor_pair.start_tank(40, -25)
        double_black()
    elif (color_1 < 30):
        motor_pair.start_tank(-25,40)
    elif (dist_cm < 10):
        obstacle_detection()
    else:
        motor_pair.start_tank(100,100)