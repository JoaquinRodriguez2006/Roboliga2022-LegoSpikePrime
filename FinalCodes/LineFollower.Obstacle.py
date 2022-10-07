from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
import hub as advancedHub
import time
import math
import random
from math import *

hub = PrimeHub()

# global color_1
# global color_2
# global color_3

global luz_1
global luz_2
global luz_3

global r1,g1,b1,ov1
global r2,g2,b2,ov2
global r3,g3,b3,ov3

global col_1
global col_3

global dist_cm

global flag_detection


# MOTORES
motor_pair = MotorPair('C', 'A')
motor_pair.set_motor_rotation(1.07 * math.pi, "cm")

# SENSORES
sen_1 = ColorSensor("B")
sen_2 = ColorSensor("D")
sen_3 = ColorSensor("F")
distancia = DistanceSensor('E')

# AYUDAS
timer = Timer()
flag_detection = False

# PID
error = 0
error_previo = 0
integral = 0
derivada = 0
proporcional = 0
kp = 3.95    # 3.95 antes
ki = 0.02
kd = 0.4
salida = 0

# DISPLAY
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

flecha_der = [
    [_,_,H,_,_],
    [_,_,_,H,_],
    [H,H,H,H,H],
    [_,_,_,H,_],
    [_,_,H,_,_],
]

flecha_izq = [
    [_,_,H,_,_],
    [_,H,_,_,_],
    [H,H,H,H,H],
    [_,H,_,_,_],
    [_,_,H,_,_],
]

flecha_atras = [
    [_,_,H,_,_],
    [_,_,H,_,_],
    [H,_,H,_,H],
    [_,H,H,H,_],
    [_,_,H,_,_],
]

flecha_frente = [
    [_,_,H,_,_],
    [_,H,H,H,_],
    [H,_,H,_,H],
    [_,_,H,_,_],
    [_,_,H,_,_],
]

blanco_h = [
    [_,_,H,_,_],
    [_,_,_,_,_],
    [H,_,_,_,H],
    [_,_,_,_,_],
    [_,_,H,_,_],
]

blanco_l = [
    [_,_,L,_,_],
    [_,_,_,_,_],
    [L,_,_,_,L],
    [_,_,_,_,_],
    [_,_,L,_,_],
]

cruz_h = [
    [_,_,H,_,_],
    [_,_,H,_,_],
    [H,H,H,H,H],
    [_,_,H,_,_],
    [_,_,H,_,_],
]

l_izq = [
    [_,_,H,_,_],
    [_,_,H,_,_],
    [H,H,H,_,_],
    [_,_,H,_,_],
    [_,_,H,_,_],
]

l_der = [
    [_,_,H,_,_],
    [_,_,H,_,_],
    [_,_,H,H,H],
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

equis = [
    [H,_,_,_,H],
    [_,H,_,H,_],
    [_,_,H,_,_],
    [_,H,_,H,_],
    [H,_,_,_,H],
]

equis_d = [
    [_,H,H,H,_],
    [H,H,_,H,H],
    [H,_,H,_,H],
    [H,H,_,H,H],
    [_,H,H,H,_],
]

verde = [
    [H,_,_,_,H],
    [H,_,_,_,H],
    [_,H,_,H,_],
    [_,H,_,H,_],
    [_,_,H,_,_],
]

verde_l = [
    [L,_,_,_,L],
    [L,_,_,_,L],
    [_,L,_,L,_],
    [_,L,_,L,_],
    [_,_,L,_,_],
]

buscar = [
    [H,H,H,_,_],
    [H,_,_,H,_],
    [H,H,H,_,_],
    [H,_,_,H,_],
    [H,H,H,_,_],
]

derecha = [
    [H,H,H,_,_],
    [H,_,_,H,_],
    [H,_,_,_,H],
    [H,_,_,H,_],
    [H,H,H,_,_],
]

izquierda = [
    [H,H,H,H,H],
    [_,_,H,_,_],
    [_,_,H,_,_],
    [_,_,H,_,_],
    [H,H,H,H,H],
]

# FUNCIONES

def matrix_to_image(matrix):
    return advancedHub.Image(":".join(["".join([str(n) for n in r]) for r in matrix]))

def mostrar(img,sec = 0):
    display = matrix_to_image(nada)
    advancedHub.display.show(display)
    display = matrix_to_image(img)
    advancedHub.display.show(display)
    wait_for_seconds(sec)

def update():
    # global color_1
    # global color_2
    # global color_3

    global luz_1
    global luz_2
    global luz_3

    global r1,g1,b1,ov1
    global r3,g3,b3,ov3

    global col_1
    global col_3

    r1,g1,b1,ov1 = sen_1.get_rgb_intensity()
    r3,g3,b3,ov3 = sen_3.get_rgb_intensity()

    global dist_cm

    luz_1 = sen_1.get_reflected_light()
    luz_2 = sen_2.get_reflected_light()
    luz_3 = sen_3.get_reflected_light()

    # color_1 = sen_1.get_color()
    # color_2 = sen_2.get_color()
    # color_3 = sen_3.get_color()

    if r1 + 25 < g1 >= b1:
        col_1 = 'green'
    else:
        col_1 = 'no'

    if r3 + 25 < g3 >= b3:
        col_3 = 'green'
    else:
        col_3 = 'no'

    dist_cm = distancia.get_distance_cm()

    if dist_cm == None:
        dist_cm = 200

def get_distance():
    dist_cm = distancia.get_distance_cm()
    if (dist_cm == None):
        dist_cm = 200
    return dist_cm

def giro_90_der():
    motor_pair.start_tank(0,0)
    # wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    while (hub.motion_sensor.get_yaw_angle() < 87):
        motor_pair.start_tank(50,-50)
    motor_pair.start_tank(0,0)
    # wait_for_seconds(1)
    angle = hub.motion_sensor.get_yaw_angle()
    print('Angulo:', angle)

def giro_90_izq():
    motor_pair.start_tank(0,0)
    # wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    while (hub.motion_sensor.get_yaw_angle() > -87):
        motor_pair.start_tank(-50,50)
    motor_pair.start_tank(0,0)
    # wait_for_seconds(1)
    angle = hub.motion_sensor.get_yaw_angle()
    print('Angulo:', angle)

def giro_180_der():
    giro_90_der()
    giro_90_der()
    motor_pair.move_tank(0.7,'cm',50,-50)

def giro_180_izq():
    giro_90_izq()
    giro_90_izq()
    motor_pair.move_tank(0.7,'cm',-50,50)

def girar_num_grados_der(num):
    hub.motion_sensor.reset_yaw_angle()
    while (hub.motion_sensor.get_yaw_angle() < num):
        motor_pair.start_tank(40, -35)
    motor_pair.start_tank(0, 0)
    hub.motion_sensor.reset_yaw_angle()

def verifica_l_giro():
    manzana = 0
    update()
    if luz_1 < 35 and luz_2 < 35 and luz_3 < 35:
        motor_pair.move_tank(4,'cm',50,50)
    elif luz_3 < 35 and not luz_2 < 30:
        motor_pair.move_tank(0.5,'cm',50,50)
        if col_1 == 'green' or col_3 == 'green':
            verifica_verde()
        else:
            motor_pair.move_tank(1,'cm',-50,-50)
            hub.motion_sensor.reset_yaw_angle()
            while (hub.motion_sensor.get_yaw_angle() > -31):
                update()
                motor_pair.start_tank(-50,50)
                if luz_2 < 35:
                    motor_pair.start_tank(0,0)
                    mostrar(l_der)
                    # motor_pair.move_tank(2.5,'cm',30,30)
                    update()
                    motor_pair.move_tank(1,'cm',50,30)
                    if col_1 == 'green' or col_3 == 'greeen':
                        motor_pair.move_tank(1.5,'cm',50,50)
                    buscar_linea("der")
                    manzana = 1
                    break
            motor_pair.start_tank(0,0)
            # mostrar(equis,2)
            # mostrar(nada)
            if manzana == 0:
                hub.motion_sensor.reset_yaw_angle()
                while hub.motion_sensor.get_yaw_angle() < 31:
                    motor_pair.start_tank(50,-50)
                motor_pair.move_tank(0.3,'cm',-10,-10)
                update()
                if not luz_2 < 35:
                    hub.motion_sensor.reset_yaw_angle()
                    while (hub.motion_sensor.get_yaw_angle() < 31):
                        update()
                        motor_pair.start_tank(50,-50)
                        if luz_2 < 35:
                            motor_pair.start_tank(0,0)
                            mostrar(l_izq)
                            # motor_pair.move_tank(2.5,'cm',30,30)
                            update()
                            motor_pair.move_tank(1,'cm',30,50)
                            if col_1 == 'green' or col_3 == 'greeen':
                                motor_pair.move_tank(1.5,'cm',50,50)
                            buscar_linea("izq")
                            manzana = 1
                            break
                    motor_pair.start_tank(0,0)
                    # mostrar(equis_d,2)
                    # mostrar(nada)
                    if manzana == 0:
                        hub.motion_sensor.reset_yaw_angle()
                        while hub.motion_sensor.get_yaw_angle() > -31:
                            motor_pair.start_tank(-50,50)
                        motor_pair.move_tank(1,'cm',-50,-50)
                        update()
                        correccion = luz_1 - luz_3
                        correccion = int(correccion * 1)
                        motor_pair.move_tank(2,'cm',-45 - correccion,-45 + correccion)
                        # motor_pair.move_tank(2,'cm',-30,-30)
                        if correccion < 0:
                            motor_pair.move_tank(1,'cm',-50,50)
                        else:
                            motor_pair.move_tank(1,'cm',50,-50)
                else:
                    motor_pair.move_tank(1,'cm',-50,-50)
                    update()
                    correccion = luz_1 - luz_3
                    correccion = int(correccion * 1)
                    motor_pair.move_tank(2,'cm',-45 - correccion,-45 + correccion)
                    # motor_pair.move_tank(2,'cm',-30,-30)
                    if correccion < 0:
                        motor_pair.move_tank(1,'cm',-50,50)
                    else:
                        motor_pair.move_tank(1,'cm',50,-50)
    else:
        manzana = 0
    manzana = 0

def verifica_doble_negro():
    motor_pair.start_tank(0,0)
    # wait_for_seconds(1)
    mostrar(cruz_l)
    motor_pair.move_tank(0.4,'cm',50,50)
    update()
    if col_1 == 'green' or col_3 == "green":
        verifica_verde()
    elif luz_1 < 27 and luz_3 < 27:
        mostrar(cruz_h)
        mostrar(nada,0)
        verifica_l_giro()
    else:
        correccion = luz_1 - luz_3
        correccion = int(correccion * 2.5)
        motor_pair.move_tank(2,'cm',-45 - correccion,-45 + correccion)
        if correccion > 0:
            motor_pair.move_tank(1.5,'cm',-50,50)
        else:
            motor_pair.move_tank(1.5,'cm',50,-50)
        # motor_pair.move_tank(2,'cm',-30,-30)
        mostrar(nada,0)

def verifica_verde():
    motor_pair.start_tank(0,0)
    mostrar(verde_l)
    update()
    if not col_1 == 'green' and not col_3 == 'green':
        motor_pair.move_tank(0.4,'cm',-50,-50)
    update()
    if col_1 == 'green' and col_3 == 'green':
        mostrar(verde)
        mostrar(flecha_atras,0)
        giro_180_der()
        motor_pair.move_tank(0.5,'cm',50,50)
        update()
        # if color_3 == 'green' or color_1 == 'green':
        #     motor_pair.move_tank(1.5,'cm',50,50)
        # buscar_linea('der')
    elif col_3 == 'green' and not col_1 == 'green':
        motor_pair.move_tank(0.9,'cm',-50,50)
        update()
        if col_1 == 'green' and col_3 == 'green':
            mostrar(verde)
            mostrar(flecha_atras,0)
            giro_180_der()
            motor_pair.move_tank(1,'cm',50,50)
            update()
            # if color_3 == 'green' or color_1 == 'green':
            #     motor_pair.move_tank(2,'cm',50,50)
            # buscar_linea('der')
        elif col_3 == 'green' and not col_1 == 'green':
            mostrar(verde)
            mostrar(flecha_der,0)
            motor_pair.move_tank(0.9,'cm',-100,0)
            motor_pair.move_tank(5.5,'cm',27,50)
            giro_90_der()
            # motor_pair.move_tank(2,'cm',30,30)
            motor_pair.move_tank(0.5,'cm',50,50)
            update()
            if col_3 == 'green' or col_1 == 'green':
                motor_pair.move_tank(1.5,'cm',50,50)
            buscar_linea('der')
        else:
            mostrar(nada,0)
            motor_pair.move_tank(2,'cm',-30,-10)
    elif col_1 == 'green' and not col_3 == 'green':
        motor_pair.move_tank(0.9,'cm',50,-50)
        update()
        if col_3 == 'green' and col_1 == 'green':
            mostrar(verde)
            mostrar(flecha_atras,0)
            giro_180_izq()
            update()
            # if color_3 == 'green' or color_1 == 'green':
            #     motor_pair.move_tank(1.5,'cm',50,50)
            # buscar_linea('izq')
        elif col_1 == 'green' and not col_3 == 'green':
            mostrar(verde)
            mostrar(flecha_izq,0)
            motor_pair.move_tank(0.9,'cm',0,-100)
            motor_pair.move_tank(5.5,'cm',50,27)
            giro_90_izq()
            # motor_pair.move_tank(2,'cm',30,30)
            motor_pair.move_tank(0.5,'cm',50,50)
            update()
            if col_3 == 'green' or col_1 == 'green':
                motor_pair.move_tank(1.5,'cm',50,50)
            buscar_linea('izq')
        else:
            mostrar(nada,0)
            motor_pair.move_tank(2,'cm',-10,-30)
    else:
        mostrar(nada,0)
        motor_pair.move_tank(2,'cm',-50,-50)
    mostrar(nada,0)

def buscar_linea(direccion):
    motor_pair.start_tank(0,0)
    mostrar(buscar)
    if direccion == 'der':
        # motor_pair.move_tank(0.8,'cm',50,-50)
        motor_pair.move_tank(1,'cm',50,0)
        while luz_1 > 23 and luz_2 > 23:
            update()
            motor_pair.start_tank(40,-30)
        motor_pair.move_tank(0.8,'cm',-70,70)
        # while luz_1 > 28:
        #     update()
        #     motor_pair.start_tank(40,40)
        # motor_pair.move_tank(0.6,'cm',-10,50)
    elif direccion == 'izq':
        # motor_pair.move_tank(0.8,'cm',-50,50)
        motor_pair.move_tank(1,'cm',0,50)
        while luz_3 > 23 and luz_2 > 23:
            update()
            motor_pair.start_tank(-30,40)
        motor_pair.move_tank(0.8,'cm',70,-70)
        # while luz_3 > 28:
        #     update()
        #     motor_pair.start_tank(40,40)
        # motor_pair.move_tank(0.6,'cm',50,-10)
    else:
        mostrar(nada,0)
    update()
    if col_1 == 'green' or col_3 == 'green':
        motor_pair.move_tank(2,'cm',50,50)
    mostrar(nada,0)

def loma_burro():
    update()
    error = luz_1 - luz_3
    proporcional = error
    salida = int(1.7 * proporcional)
    motor_pair.start_tank(30 + salida, 30 - salida)
    update()
    if luz_1 < 16:
        while luz_2 > 25:
            motor_pair.start_tank(-40,40)
            update()
        motor_pair.move_tank(1,'cm',50,50)
    elif luz_3 < 16:
        while luz_2 > 25:
            motor_pair.start_tank(40,-40)
            update()
        motor_pair.move_tank(1,'cm',50,50)
    else:
        mostrar(equis)

def find_line_after_obstacle(direction):
    luz_3 = sen_3.get_reflected_light()
    luz_1 = sen_1.get_reflected_light()
    if direction == 'right':
        luz_3 = sen_3.get_reflected_light()
        while (luz_3 < 45):
            luz_3 = sen_3.get_reflected_light()
            motor_pair.start_tank(-10, 10)
        motor_pair.start_tank(0, 0)

    elif direction == 'left':
        luz_1 = sen_1.get_reflected_light()
        while (luz_1 < 45):
            luz_1 = sen_1.get_reflected_light()
            motor_pair.start_tank(10, -10)
        motor_pair.start_tank(0, 0)

def obstacle_detection():
    dist_cm = get_distance()
    if dist_cm > 5:
        motor_pair.start_tank(50, 50)
        dist_cm = get_distance()
    dist_cm = get_distance()
    color_2 = sen_2.get_reflected_light()
    while ((dist_cm) < 9):
        dist_cm = get_distance()
        print(dist_cm)
        motor_pair.start_tank(-10, -10)
    motor_pair.start_tank(0, 0)
    motor_pair.move_tank(1, 'cm', -10, -10)
    """while (hub.motion_sensor.get_yaw_angle() < 25):
        angle = hub.motion_sensor.get_yaw_angle()
        motor_pair.start_tank(40, -35)
        print(angle)"""
    girar_num_grados_der(20)
    color_2 = sen_2.get_reflected_light()
    while (color_2 > 17):
        color_2 = sen_2.get_reflected_light()
        motor_pair.start_tank(-20, 20)
    motor_pair.start_tank(0, 0) 
    girar_num_grados_der(45)
    dist_cm = get_distance()
    if (dist_cm > 20):
        hub.light_matrix.show_image('HAPPY')
        girar_num_grados_der(35)
        dist_cm = get_distance()
        if (dist_cm > 20):
            motor_pair.move_tank(3.5, 'cm', -30, 76) # Antes estaba en 24
            motor_pair.move_tank(14, 'cm', 29, 75)
            hub.light_matrix.show_image('HEART')
            timer.reset()
            color_2 = sen_2.get_reflected_light()
            while (color_2 > 20): # Antes estaba en 45
                color_2 = sen_2.get_reflected_light()
                motor_pair.start_tank(29, 75)
                if (timer.now() > 1.6):
                    color_2 = sen_2.get_reflected_light()
                    while (color_2 > 20):
                        color_2 = sen_2.get_reflected_light()
                        motor_pair.start_tank(22, 75)
                        timer.reset()
            motor_pair.start_tank(0, 0)
            hub.light_matrix.show_image('DIAMOND')
            motor_pair.move_tank(6, 'cm', 60, 60)
            color_2 = sen_2.get_reflected_light()
            """hub.motion_sensor.reset_yaw_angle()
            while (hub.motion_sensor.get_yaw_angle() < 90):
                angle = hub.motion_sensor.get_yaw_angle()
                print(angle)
                motor_pair.start_tank(40, -35)
            motor_pair.start_tank(0, 0)
            buscar_linea('izq')
            """
            while color_2 > 20:
                color_2 = sen_2.get_reflected_light()
                motor_pair.start_tank(30, -30)
            motor_pair.start_tank(0, 0)
            
        else:
            color_2 = sen_2.get_reflected_light()
            hub.light_matrix.show_image('ANGRY')
            hub.motion_sensor.reset_yaw_angle()
            while (hub.motion_sensor.get_yaw_angle() > -159):
                motor_pair.start_tank(-35, 40)
            hub.motion_sensor.reset_yaw_angle()
            motor_pair.start_tank(0, 0)
            motor_pair.move_tank(3.5, 'cm', 60, 20)
            motor_pair.move_tank(13, 'cm', 80, 30)
            hub.light_matrix.show_image('HEART')
            timer.reset()
            color_2 = sen_2.get_reflected_light()
            while (color_2 > 20): # Antes estaba en 45
                color_2 = sen_2.get_reflected_light()
                motor_pair.start_tank(80, 30)
                if (timer.now() > 1.5):
                    color_2 = sen_2.get_reflected_light()
                    while (color_2 > 20):
                        color_2 = sen_2.get_reflected_light()
                        motor_pair.start_tank(80, 20) # Antes eran 80/18
                        timer.reset()
            motor_pair.start_tank(0, 0)
            color_2 = sen_2.get_reflected_light()
            hub.motion_sensor.reset_yaw_angle()
            while (hub.motion_sensor.get_yaw_angle() < 70):
                angle = hub.motion_sensor.get_yaw_angle()
                print(angle)
                motor_pair.start_tank(40, -35)
            motor_pair.start_tank(0, 0)
            buscar_linea('der')
            """while color_2 > 20:
                color_2 = sen_2.get_reflected_light()
                motor_pair.start_tank(30, -30)
            motor_pair.start_tank(0, 0)"""
    else:
        color_2 = sen_2.get_reflected_light()
        hub.light_matrix.show_image('ANGRY')
        hub.motion_sensor.reset_yaw_angle()
        while (hub.motion_sensor.get_yaw_angle() > -109):
            motor_pair.start_tank(-35, 40)
        hub.motion_sensor.reset_yaw_angle()
        motor_pair.start_tank(0, 0)
        motor_pair.move_tank(3.5, 'cm', 60, 45)
        motor_pair.move_tank(13, 'cm', 75, 38)
        hub.light_matrix.show_image('HEART')
        timer.reset()
        color_2 = sen_2.get_reflected_light()
        while (color_2 > 20): # Antes estaba en 45
            color_2 = sen_2.get_reflected_light()
            motor_pair.start_tank(80, 30)
            if (timer.now() > 1.5):
                color_2 = sen_2.get_reflected_light()
                while (color_2 > 20):
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(80, 20) # Antes eran 80/18
                    timer.reset()
        motor_pair.start_tank(0, 0)
        color_2 = sen_2.get_reflected_light()
        hub.motion_sensor.reset_yaw_angle()
        while (hub.motion_sensor.get_yaw_angle() < 70):
            angle = hub.motion_sensor.get_yaw_angle()
            print(angle)
            motor_pair.start_tank(40, -35)
        motor_pair.start_tank(0, 0)
        buscar_linea('der')
        """while color_2 > 20:
            color_2 = sen_2.get_reflected_light()
            motor_pair.start_tank(30, -30)
        motor_pair.start_tank(0, 0)"""
    mostrar(nada)

while True:
    update()
    if luz_3 < 30:
        error = luz_1 - (luz_3 / 20)
    elif luz_1 < 30:
        error = (luz_1 / 20) - luz_3
    else:
        error = luz_1 - luz_3 
    proporcional = error
    integral = integral + error * 0.04
    derivada = (error - error_previo) / 0.04
    salida = int(kp * proporcional + ki * integral + kd * derivada)
    error_previo = error

    if dist_cm < 10:
        obstacle_detection()
    else:
        if col_1 == 'green' or col_3 == 'green':
            verifica_verde()
        elif luz_1 < 30 and luz_3 < 30:
            verifica_doble_negro()
        elif luz_1 > 50 and luz_2 > 50 and luz_3 > 50:
            motor_pair.start_tank(50,50)
        # elif hub.motion_sensor.get_roll_angle() > 1 or hub.motion_sensor.get_roll_angle() < -1:
        #     mostrar(equis)
        #    loma_burro()
        else:
            if luz_1 < 17 or luz_3 < 17:
                salida = int(4 * proporcional + ki * integral + kd * derivada)
                motor_pair.start_tank(60 + salida, 60 - salida)
            elif luz_1 < 24 or luz_3 < 24:
                salida = int(3 * proporcional + ki * integral + kd * derivada)
                motor_pair.start_tank(60 + salida, 60 - salida)
            else:
                salida = int(1.8 * proporcional + ki * integral + kd * derivada)
                motor_pair.start_tank(60 + salida, 60 - salida)
        