from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
import hub as advancedHub
import time
import math
import random
from math import *

hub = PrimeHub()

# Izquierda: 1
# Medio: 2
# Derecha: 3

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

global ant


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
ant = 0

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

    if r1 + 20 < g1+5 >= b1 and g1 < 205:
        col_1 = 'green'
    elif r1 > 600 and g1 > 600 and b1 > 600:
        col_1 = 'plateado'
    else:
        col_1 = 'no'

    if r3 + 20 < g3+5 >= b3 and g3 < 205:
        col_3 = 'green'
    elif r3 > 600 and g3 > 600 and b3 > 600:
        col_3 = 'plateado'
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
    while (hub.motion_sensor.get_yaw_angle() < 88):
        motor_pair.start_tank(80,-80)
    motor_pair.start_tank(0,0)
    # wait_for_seconds(1)
    angle = hub.motion_sensor.get_yaw_angle()
    print('Angulo:', angle)

def giro_90_izq():
    motor_pair.start_tank(0,0)
    # wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    while (hub.motion_sensor.get_yaw_angle() > -88):
        motor_pair.start_tank(-80,80)
    motor_pair.start_tank(0,0)
    # wait_for_seconds(1)
    angle = hub.motion_sensor.get_yaw_angle()
    print('Angulo:', angle)

def giro_180_der():
    giro_90_der()
    giro_90_der()
    motor_pair.move_tank(0.7,'cm',80,-80)

def giro_180_izq():
    giro_90_izq()
    giro_90_izq()
    motor_pair.move_tank(0.7,'cm',-80,80)

def girar_num_grados_der(num):
    hub.motion_sensor.reset_yaw_angle()
    while (hub.motion_sensor.get_yaw_angle() < num):
        motor_pair.start_tank(90, -85)
    motor_pair.start_tank(0, 0)
    hub.motion_sensor.reset_yaw_angle()

def verifica_l_giro():
    manzana = 0
    update()
    if luz_1 < 35 and luz_2 < 35 and luz_3 < 35:
        motor_pair.move_tank(4,'cm',80,80)
    elif luz_3 < 35 and not luz_2 < 30:
        motor_pair.move_tank(0.5,'cm',80,80)
        if col_1 == 'green' or col_3 == 'green':
            verifica_verde()
        else:
            motor_pair.move_tank(0.5,'cm',-80,-80)
            hub.motion_sensor.reset_yaw_angle()
            while (hub.motion_sensor.get_yaw_angle() > -29):
                update()
                motor_pair.start_tank(-80,80)
                if luz_2 < 35:
                    motor_pair.start_tank(0,0)
                    mostrar(l_der)
                    # motor_pair.move_tank(2.5,'cm',30,30)
                    update()
                    buscar_linea("izq")
                    motor_pair.move_tank(1.7,'cm',50,30)
                    if col_1 == 'green' or col_3 == 'greeen':
                        motor_pair.move_tank(1.5,'cm',80,80)
                    manzana = 1
                    break
            motor_pair.start_tank(0,0)
            # mostrar(equis,2)
            # mostrar(nada)
            if manzana == 0:
                hub.motion_sensor.reset_yaw_angle()
                while hub.motion_sensor.get_yaw_angle() < 29:
                    motor_pair.start_tank(80,-80)
                motor_pair.move_tank(0.3,'cm',-80,-80)
                update()
                if not luz_2 < 35:
                    hub.motion_sensor.reset_yaw_angle()
                    while (hub.motion_sensor.get_yaw_angle() < 29):
                        update()
                        motor_pair.start_tank(80,-80)
                        if luz_2 < 35:
                            motor_pair.start_tank(0,0)
                            mostrar(l_izq)
                            # motor_pair.move_tank(2.5,'cm',30,30)
                            update()
                            buscar_linea("der")
                            motor_pair.move_tank(1.7,'cm',30,50)
                            if col_1 == 'green' or col_3 == 'greeen':
                                motor_pair.move_tank(1.5,'cm',80,80)
                            manzana = 1
                            break
                    motor_pair.start_tank(0,0)
                    # mostrar(equis_d,2)
                    # mostrar(nada)
                    if manzana == 0:
                        hub.motion_sensor.reset_yaw_angle()
                        while hub.motion_sensor.get_yaw_angle() > -29:
                            motor_pair.start_tank(-80,80)
                        motor_pair.move_tank(1,'cm',-80,-80)
                        update()
                        correccion = luz_1 - luz_3
                        correccion = int(correccion * 1)
                        motor_pair.move_tank(2,'cm',-45 - correccion,-45 + correccion)
                        # motor_pair.move_tank(2,'cm',-30,-30)
                        if correccion < 0:
                            motor_pair.move_tank(1,'cm',-80,80)
                        else:
                            motor_pair.move_tank(1,'cm',80,-80)
                else:
                    motor_pair.move_tank(1,'cm',-50,-50)
                    update()
                    correccion = luz_1 - luz_3
                    correccion = int(correccion * 1)
                    motor_pair.move_tank(2,'cm',-45 - correccion,-45 + correccion)
                    # motor_pair.move_tank(2,'cm',-30,-30)
                    if correccion < 0:
                        motor_pair.move_tank(1,'cm',-80,80)
                    else:
                        motor_pair.move_tank(1,'cm',80,-80)
    else:
        manzana = 0
    manzana = 0

def verifica_doble_negro():
    motor_pair.start_tank(0,0)
    # wait_for_seconds(1)
    mostrar(cruz_l)
    motor_pair.move_tank(0.4,'cm',80,80)
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
            motor_pair.move_tank(1.5,'cm',-80,80)
        else:
            motor_pair.move_tank(1.5,'cm',80,-80)
        # motor_pair.move_tank(2,'cm',-30,-30)
        mostrar(nada,0)

def verifica_verde():
    motor_pair.start_tank(0,0)
    mostrar(verde_l)
    update()
    # if not col_1 == 'green' and not col_3 == 'green':
    #    motor_pair.move_tank(0.6,'cm',80,80)
    update()
    if col_1 == 'green' and col_3 == 'green':
        mostrar(verde)
        mostrar(flecha_atras,0)
        giro_180_der()
        motor_pair.move_tank(0.5,'cm',80,80)
        update()
        # if color_3 == 'green' or color_1 == 'green':
        #    motor_pair.move_tank(1.5,'cm',50,50)
        # buscar_linea('der')
    elif col_3 == 'green' and not col_1 == 'green':
        motor_pair.move_tank(0.5,'cm',80,-20)
        # motor_pair.move_tank(0.9,'cm',-80,80)
        update()
        if col_1 == 'green' and col_3 == 'green':
            mostrar(verde)
            mostrar(flecha_atras,0)
            giro_180_der()
            motor_pair.move_tank(0.5,'cm',80,80)
            update()
        else:
            motor_pair.move_tank(0.5,'cm',-80,20)
            if col_3 == 'green' and not col_1 == 'green':
                mostrar(verde)
                mostrar(flecha_der,0)
                # motor_pair.move_tank(0.9,'cm',-100,0)
                # motor_pair.move_tank(0.5,'cm',-80,-80)
                # motor_pair.move_tank(1,'cm',50,50)
                motor_pair.move_tank(4.5,'cm',25,50)
                giro_90_der()
                # motor_pair.move_tank(2,'cm',30,30)
                buscar_linea('der')
                motor_pair.move_tank(2.3,'cm',80,80)
                update()
                if luz_2 > 30:
                    motor_pair.move_tank(0.8,'cm',-80,-80)
                update()
                if col_3 == 'green' or col_1 == 'green':
                    motor_pair.move_tank(1,'cm',80,80)
            else:
                mostrar(nada,0)
                motor_pair.move_tank(2,'cm',-30,-10)
    elif col_1 == 'green' and not col_3 == 'green':
        motor_pair.move_tank(0.5,'cm',-20,80)
        # motor_pair.move_tank(0.9,'cm',80,-80)
        update()
        if col_3 == 'green' and col_1 == 'green':
            mostrar(verde)
            mostrar(flecha_atras,0)
            giro_180_izq()
            update()
        else:
            motor_pair.move_tank(0.5,'cm',20,-80)
            if col_1 == 'green' and not col_3 == 'green':
                mostrar(verde)
                mostrar(flecha_izq,0)
                # motor_pair.move_tank(0.9,'cm',0,-100)
                # motor_pair.move_tank(0.5,'cm',-80,-80)
                # motor_pair.move_tank(1,'cm',50,50)
                motor_pair.move_tank(4.5,'cm',50,25)
                giro_90_izq()
                # motor_pair.move_tank(2,'cm',30,30)
                buscar_linea('izq')
                motor_pair.move_tank(2.3,'cm',50,50)
                update()
                if luz_2 > 30:
                    motor_pair.move_tank(0.8,'cm',-50,-50)
                    update()
                if col_3 == 'green' or col_1 == 'green':
                    motor_pair.move_tank(1,'cm',50,50)
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
        motor_pair.move_tank(0.5,'cm',80,0)
        while luz_1 > 23 and luz_2 > 23:
            update()
            motor_pair.start_tank(80,-80)
        motor_pair.start_tank(0,0)
        # mostrar(equis)
        if luz_2 < 30:
            motor_pair.move_tank(0.7,'cm',-80,80)
        else:
            motor_pair.move_tank(2.5,'cm',-80,80)
        # while luz_1 > 28:
        #    update()
        #    motor_pair.start_tank(40,40)
        # motor_pair.move_tank(0.6,'cm',-10,50)
    elif direccion == 'izq':
        # motor_pair.move_tank(0.8,'cm',-50,50)
        motor_pair.move_tank(0.5,'cm',0,80)
        while luz_3 > 23 and luz_2 > 23:
            update()
            motor_pair.start_tank(-80,80)
        # mostrar(equis)
        if luz_2 < 30:
            motor_pair.move_tank(0.7,'cm',80,-80)
        else:
            motor_pair.move_tank(2.5,'cm',80,-80)
        # while luz_3 > 28:
        #    update()
        #    motor_pair.start_tank(40,40)
        # motor_pair.move_tank(0.6,'cm',50,-10)
    else:
        mostrar(nada,0)
    update()
    mostrar(nada)
    # motor_pair.move_tank(0.8,'cm',50,50)
    # if col_1 == 'green' or col_3 == 'green':
    #    motor_pair.move_tank(2,'cm',50,50)
    # mostrar(nada,0)

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
    global ant
    dist_cm = get_distance()
    if dist_cm > 5:
        motor_pair.start_tank(50, 50)
        dist_cm = get_distance()
    dist_cm = get_distance()
    color_2 = sen_2.get_reflected_light()
    girar_num_grados_der(14)
    color_2 = sen_2.get_reflected_light()
    while (color_2 > 19):
        color_2 = sen_2.get_reflected_light()
        motor_pair.start_tank(-95, 95)
    motor_pair.start_tank(0, 0)
    while ((dist_cm) < 10):
        dist_cm = get_distance()
        print(dist_cm)
        motor_pair.start_tank(-80, -80)
    motor_pair.start_tank(0, 0)
    motor_pair.move_tank(1, 'cm', -100, -100)
    if (ant == 0):
        ant = 1
        girar_num_grados_der(45)
        dist_cm = get_distance()
        if (dist_cm > 20):
            hub.light_matrix.show_image('HAPPY')
            girar_num_grados_der(35)
            dist_cm = get_distance()
            if (dist_cm > 20):
                motor_pair.move_tank(3.5, 'cm', -47, 100) # Antes estaba en 24
                motor_pair.move_tank(17, 'cm', 45, 100)
                hub.light_matrix.show_image('HEART')
                timer.reset()
                color_1 = sen_1.get_reflected_light()
                while (color_1 > 20): # Antes estaba en 45
                    color_1 = sen_1.get_reflected_light()
                    motor_pair.start_tank(37, 100)
                    if (timer.now() > 1):
                        color_1 = sen_1.get_reflected_light()
                        while (color_1 > 20):
                            color_1 = sen_1.get_reflected_light()
                            motor_pair.start_tank(32, 100)
                            timer.reset()
                motor_pair.start_tank(0, 0)
                hub.light_matrix.show_image('DIAMOND')
                motor_pair.move_tank(4, 'cm', 100, 100)
                color_2 = sen_2.get_reflected_light()
                while color_2 > 20:
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(100, -100)
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(3, 'cm', 100, 100)
            else:
                color_2 = sen_2.get_reflected_light()
                hub.light_matrix.show_image('ANGRY')
                hub.motion_sensor.reset_yaw_angle()
                while (hub.motion_sensor.get_yaw_angle() > -159):
                    motor_pair.start_tank(-95, 100)
                hub.motion_sensor.reset_yaw_angle()
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(3.5, 'cm', 100, 60)
                motor_pair.move_tank(17, 'cm', 100, 40)
                hub.light_matrix.show_image('HEART')
                timer.reset()
                color_2 = sen_2.get_reflected_light()
                while (color_2 > 20): # Antes estaba en 45
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(100, 38)
                    if (timer.now() > 1.5):
                        color_2 = sen_2.get_reflected_light()
                        while (color_2 > 20):
                            color_2 = sen_2.get_reflected_light()
                            motor_pair.start_tank(100, 23) # Antes eran 80/18
                            timer.reset()
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(6, 'cm', 100, 100)
                color_2 = sen_2.get_reflected_light()
                while color_2 > 20:
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(-100, 100)
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(3, 'cm', 100, 100)
        else:
            color_2 = sen_2.get_reflected_light()
            hub.light_matrix.show_image('ANGRY')
            hub.motion_sensor.reset_yaw_angle()
            while (hub.motion_sensor.get_yaw_angle() > -109):
                motor_pair.start_tank(-95, 100)
            hub.motion_sensor.reset_yaw_angle()
            motor_pair.start_tank(0, 0)
            motor_pair.move_tank(4.8, 'cm', 100, 90)
            motor_pair.move_tank(13, 'cm', 95, 41)
            hub.light_matrix.show_image('HEART')
            timer.reset()
            color_2 = sen_2.get_reflected_light()
            while (color_2 > 20): # Antes estaba en 45
                color_2 = sen_2.get_reflected_light()
                motor_pair.start_tank(100, 40)
                if (timer.now() > 1.5):
                    color_2 = sen_2.get_reflected_light()
                    while (color_2 > 20):
                        color_2 = sen_2.get_reflected_light()
                        motor_pair.start_tank(100, 20) # Antes eran 80/18
                        timer.reset()
            motor_pair.start_tank(0, 0)
            motor_pair.move_tank(6, 'cm', 100, 100)
            color_2 = sen_2.get_reflected_light()
            while color_2 > 20:
                color_2 = sen_2.get_reflected_light()
                motor_pair.start_tank(-100, 100)
            motor_pair.start_tank(0, 0)
            motor_pair.move_tank(3, 'cm', 100, 100)

    elif (ant == 1):
        ant = 0
        hub.motion_sensor.reset_yaw_angle()
        while (hub.motion_sensor.get_yaw_angle() > -45):
            motor_pair.start_tank(-95, 100)
        hub.motion_sensor.reset_yaw_angle()
        motor_pair.start_tank(0, 0)
        dist_cm = get_distance()
        if (dist_cm > 20):
            hub.light_matrix.show_image('HAPPY')
            hub.motion_sensor.reset_yaw_angle()
            while (hub.motion_sensor.get_yaw_angle() > -35):
                motor_pair.start_tank(-95, 100)
            hub.motion_sensor.reset_yaw_angle()
            dist_cm = get_distance()
            if (dist_cm > 20):
                motor_pair.move_tank(3, 'cm', 96, -40) # Antes estaba en 24
                motor_pair.move_tank(17, 'cm', 95, 36)
                hub.light_matrix.show_image('HEART')
                timer.reset()
                color_2 = sen_2.get_reflected_light()
                while (color_2 > 20): # Antes estaba en 45
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(95, 36)
                    if (timer.now() > 1.2):
                        color_2 = sen_2.get_reflected_light()
                        while (color_2 > 20):
                            color_2 = sen_2.get_reflected_light()
                            motor_pair.start_tank(95, 25)
                            timer.reset()
                motor_pair.start_tank(0, 0)
                hub.light_matrix.show_image('DIAMOND')
                motor_pair.move_tank(6, 'cm', 100, 100)
                color_2 = sen_2.get_reflected_light()
                while color_2 > 20:
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(-100, 100)
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(3, 'cm', 100, 100)
            else:
                color_2 = sen_2.get_reflected_light()
                hub.light_matrix.show_image('ANGRY')
                hub.motion_sensor.reset_yaw_angle()
                while (hub.motion_sensor.get_yaw_angle() < 170):
                    motor_pair.start_tank(100, -95)
                hub.motion_sensor.reset_yaw_angle()
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(4, 'cm', -46, 100)
                motor_pair.move_tank(13, 'cm', 43, 100)
                hub.light_matrix.show_image('HEART')
                timer.reset()
                color_2 = sen_2.get_reflected_light()
                while (color_2 > 20): # Antes estaba en 45
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(40, 80)
                    if (timer.now() > 1.5):
                        color_2 = sen_2.get_reflected_light()
                        while (color_2 > 20):
                            color_2 = sen_2.get_reflected_light()
                            motor_pair.start_tank(17, 80) # Antes eran 80/18
                            timer.reset()
                motor_pair.start_tank(0, 0)
                hub.light_matrix.show_image('DIAMOND')
                motor_pair.move_tank(6, 'cm', 100, 100)
                color_2 = sen_2.get_reflected_light()
                while color_2 > 20:
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(100, -100)
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(3, 'cm', 100, 100)
        else:
            color_2 = sen_2.get_reflected_light()
            hub.light_matrix.show_image('ANGRY')
            hub.motion_sensor.reset_yaw_angle()
            while (hub.motion_sensor.get_yaw_angle() < 125):
                angle = hub.motion_sensor.get_yaw_angle()
                motor_pair.start_tank(100, -95)
                print(angle)
            hub.motion_sensor.reset_yaw_angle()
            motor_pair.start_tank(0, 0)
            motor_pair.move_tank(3, 'cm', 38, 100)
            motor_pair.move_tank(17, 'cm', 35, 95)
            hub.light_matrix.show_image('HEART')
            timer.reset()
            color_2 = sen_2.get_reflected_light()
            while (color_2 > 20): # Antes estaba en 45
                color_2 = sen_2.get_reflected_light()
                motor_pair.start_tank(35, 100)
                if (timer.now() > 1.2):
                    color_2 = sen_2.get_reflected_light()
                    while (color_2 > 20):
                        color_2 = sen_2.get_reflected_light()
                        motor_pair.start_tank(26, 100) # Antes eran 80/18
                        timer.reset()
            motor_pair.start_tank(0, 0)
            hub.light_matrix.show_image('DIAMOND')
            motor_pair.move_tank(6, 'cm', 100, 100)
            color_2 = sen_2.get_reflected_light()
            while color_2 > 20:
                color_2 = sen_2.get_reflected_light()
                motor_pair.start_tank(100, -100)
            motor_pair.start_tank(0, 0)
            motor_pair.move_tank(3, 'cm', 100, 100)
    mostrar(nada)


#################################### Funciones de Rescate #######################################
def normalize_degs(ang):
    ang = ang % 360
    if ang < 0:
        ang += 360
    if ang == 360:
        ang = 0
    return ang

# Converts from radians to degrees
def radsToDegs(rad):
    return rad * 180 / pi

# Converts a number from a range of value to another
def map_vals(val, in_min, in_max, out_min, out_max):
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def get_degs_from_coords(coords):
    rads = atan2(coords[0], coords[1])
    return radsToDegs(rads)

# Gets the distance to given coordinates
def get_distance_from_coords(position):
    return sqrt((position[0] ** 2) + (position[1] ** 2))

# hub = PrimeHub()

rectangle_dimensions = [0, 0]


"""
motor_pair = MotorPair("A", "C")
motor_pair.set_motor_rotation(1.07*pi)

distancia= DistanceSensor("E")

sen_1 = ColorSensor("B")
sen_2 = ColorSensor("D")
sen_3 = ColorSensor("F")
"""

def measure_distance():
    dist = distancia.get_distance_cm()
    if dist is None:
        return 10000000
    return dist



initial_rotation = hub.motion_sensor.get_yaw_angle() + 180


def get_rotation():
    global initial_rotation
    return normalize_degs(hub.motion_sensor.get_yaw_angle() + 180 - initial_rotation)

def rotate_to_degs(degs, orientation="closest", max_speed=100):
    print("turn to degs:", degs)
    degs = normalize_degs(degs)
    accuracy = 2
    init_rotation = get_rotation()
    initial_diff = round(init_rotation - degs)
    while True:
        diff = get_rotation() - degs
        print("degs", degs)
        print("raw_rot", hub.motion_sensor.get_yaw_angle())
        print("rot", get_rotation())
        moveDiff = max(round(get_rotation()), degs) - min(get_rotation(), degs)
        if diff > 180 or diff < -180:
            moveDiff = 360 - moveDiff
        speedFract = int(min(map_vals(moveDiff, accuracy, 90, 20, 100), max_speed))
        if accuracy * -1 < diff < accuracy or 360 - accuracy < diff < 360 + accuracy:
            break
        else:
            if orientation == "closest":
                if 180 > initial_diff > 0 or initial_diff < -180:
                    direction = "right"
                else:
                    direction = "left"
            elif orientation == "farthest":
                if 180 > initial_diff > 0 or initial_diff < -180:
                    direction = "left"
                else:
                    direction = "right"
            else:
                direction = orientation

            if direction == "right":
                motor_pair.start_tank(speedFract * -1, speedFract)
            elif direction == "left":
                motor_pair.start_tank(speedFract, speedFract * -1)
    motor_pair.stop()

def get_90_degs_distances():
    distance_sensor_radious = 4
    dists = {}

    for i in (0, 90, 180, 270):
        rotate_to_degs(i)
        dists[i] = measure_distance() + distance_sensor_radious

    return dists

def measure_and_locate():
    dists = get_90_degs_distances()

    robot_position = [dists[90], dists[0]]

    rectangle_dims = [robot_position[0] + dists[270], robot_position[1] + dists[180]]

    return rectangle_dims, robot_position

def move_to(robot_position, robot_destination, use_dist=True):
    direction = get_degs_from_coords([robot_position[0] - robot_destination[0], (robot_position[1] - robot_destination[1]) * -1])
    distance = get_distance_from_coords([robot_destination[0] - robot_position[0], robot_destination[1] - robot_position[1]])
    rotate_to_degs(direction)
    if use_dist:
        motor_pair.move(distance * -1, speed=100)
    else:
        motor_pair.start(speed=-100)
    return robot_destination

def search_silver():
    motor_pair.start(speed=-100)
    while True:
        if sen_1.get_reflected_light() > 85 and sen_3.get_reflected_light() > 85:
            break

    motor_pair.move(-20, speed=100)

def set_gyro_angle(angle):
    global initial_rotation
    wait_for_seconds(0.2)
    initial_rotation = normalize_degs(hub.motion_sensor.get_yaw_angle() + 180 - angle)
    wait_for_seconds(0.2)

def align():
    global initial_rotation
    initial_rotation = hub.motion_sensor.get_yaw_angle() + 180

    dist90 = 0

    dist270 = 0

    rotate_to_degs(90)

    dist90 = measure_distance()

    rotate_to_degs(270)

    dist270 = measure_distance()

    rot_degs = 270

    print("dist 90:", dist90, ": dist 270:", dist270)

    if dist90 > dist270:
        rotate_to_degs(90)
        rot_degs = 90

    motor_pair.move(30, speed=100)
    motor_pair.stop()
    wait_for_seconds(0.1)
    initial_rotation = normalize_degs(hub.motion_sensor.get_yaw_angle() + 180- rot_degs)
    wait_for_seconds(0.1)
    motor_pair.move(-8, speed=100)

    return rot_degs

def go_to_closest_wall():
    dists = get_90_degs_distances()
    min_dist_degs = min(dists, key=dists.get)
    rotate_to_degs(min_dist_degs)
    motor_pair.start(speed=-100)
    while measure_distance() > 5:
        pass


def follow_wall_until_limit(wall, limit=5):
    if wall == "right":
        motor_pair.move(-4, steering=-80)
        motor_pair.start_tank(-100, -100)
    elif wall == "left":
        motor_pair.move(-4, steering=80)
        motor_pair.start_tank(-100, -100)

    while measure_distance() > limit:
        pass

    motor_pair.stop()

def turn_corner(direction):
    if direction == "left":
        motor_pair.move(-14, steering=100)
    elif direction == "right":
        motor_pair.move(-14, steering=-100)

def move_to_corner(robot_position, corner, use_dist=True):
    global rectangle_dimensions
    corner_pos = [corner[0] * rectangle_dimensions[0], corner[1] * rectangle_dimensions[1]]
    return move_to(robot_position, corner_pos, use_dist)

########################################################################################################
########################################################################################################

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
    if col_1 == 'plateado' or col_3 == 'plateado':
        break
    if dist_cm < 7:
        obstacle_detection()
    else:
        update()
        if col_1 == 'green' or col_3 == 'green':
            print('a')
            verifica_verde()
        elif luz_1 < 30 and luz_3 < 30:
            verifica_doble_negro()
        elif luz_1 > 50 and luz_2 > 50 and luz_3 > 50:
            motor_pair.start_tank(90,90)
        # elif hub.motion_sensor.get_roll_angle() > 1 or hub.motion_sensor.get_roll_angle() < -1:
        #    mostrar(equis)
        #    loma_burro()
        else:
            if luz_1 < 26 or luz_3 < 26:
                salida = int(4 * proporcional + ki * integral + kd * derivada)
                motor_pair.start_tank(60 + salida, 60 - salida)
            # elif luz_1 < 25 or luz_3 < 25:
            #    salida = int(3 * proporcional + ki * integral + kd * derivada)
            #    motor_pair.start_tank(75 + salida, 75 - salida)
            else:
                salida = int(1.4 * proporcional + ki * integral + kd * derivada)
                motor_pair.start_tank(90 + salida, 90 - salida)
            mostrar(nada)

########################################################################################################################
########################################################################################################################


possible_corners = [(0, 0), (0, 1), (1, 1), (1, 0)]

motor_pair = MotorPair("A", "C")
motor_pair.set_motor_rotation(1.07*pi)

motor_pair.move(-30, speed=100)

aligned_degs = align()

motor_pair.move(-30, speed=100)

rectangle_dimensions, robot_position = measure_and_locate()

motor_pair.move(30, speed=100)

SEARCHING_STEP = 20


if aligned_degs == 270:
    rotate_to_degs(90)
    black_corner = None
    for corner in ((0, 1), (1, 1), (1, 0), (0, 0)):
        turn_corner("left")
        follow_wall_until_limit("right")
        if sen_2.get_reflected_light() < 40:
            hub.light_matrix.show_image('HAPPY')
            black_corner = corner
            break


    if black_corner == (1, 1):
        motor_pair.move(max(rectangle_dimensions), speed=100)
        set_gyro_angle(270)
        robot_position = [10, rectangle_dimensions[1]]
        start_distance = 20

        #FIRST WALL
        while True:
            motor_pair.move(-5)
            rotate_to_degs(0)
            motor_pair.start(speed=100)
            while measure_distance() < start_distance:
                pass
            motor_pair.stop()

            distance = measure_distance()
            robot_position = [10, rectangle_dimensions[1] - distance]
            if distance > rectangle_dimensions[1] - SEARCHING_STEP:
                break
            start_distance += SEARCHING_STEP

            move_to_corner(robot_position, black_corner, use_dist=False)
            while sen_2.get_reflected_light() > 40:
                pass
            motor_pair.move(max(rectangle_dimensions) + 20, speed=100)
            set_gyro_angle(270)

        motor_pair.move(-10)
        rotate_to_degs(270)
        motor_pair.move(15)
        set_gyro_angle(270)
        motor_pair.move(-30)
        rotate_to_degs(0)
        motor_pair.move(15)
        set_gyro_angle(0)

        robot_position = [30, 10]
        start_distance = rectangle_dimensions[0] - 30

        #SECOND WALL

        while True:
            motor_pair.move(-5)
            rotate_to_degs(270)
            motor_pair.start(speed=-100)
            while measure_distance() > start_distance:
                pass
            motor_pair.stop()

            distance = measure_distance()
            robot_position = [rectangle_dimensions[0] - distance, 0]
            if distance < SEARCHING_STEP:
                break
            start_distance -= SEARCHING_STEP

            move_to_corner(robot_position, black_corner, use_dist=False)
            while sen_2.get_reflected_light() > 40:
                pass
            motor_pair.move(max(rectangle_dimensions) + 20, speed=100)
            set_gyro_angle(0)

        motor_pair.move(max(rectangle_dimensions) + 20, speed=100)
        motor_pair.move(-5)
        rotate_to_degs(180)
        motor_pair.move(-30)




    elif black_corner == (1, 0):
        motor_pair.move(max(rectangle_dimensions), speed=50)
        set_gyro_angle(180)
        robot_position = [rectangle_dimensions[0], rectangle_dimensions[1]]
        start_distance = rectangle_dimensions[0] - 20

        #FIRST WALL

        while True:
            motor_pair.move(-5)
            rotate_to_degs(90)
            motor_pair.start(speed=-100)
            while measure_distance() > start_distance:
                pass
            motor_pair.stop()

            distance = measure_distance()
            robot_position = [distance , rectangle_dimensions[1] - 5]
            if distance < SEARCHING_STEP:
                break
            start_distance -= SEARCHING_STEP

            move_to_corner(robot_position, black_corner, use_dist=False)
            while sen_2.get_reflected_light() > 40:
                pass
            motor_pair.move(max(rectangle_dimensions) + 20, speed=100)
            set_gyro_angle(180)

        robot_position = [0, rectangle_dimensions[1]]
        start_distance = 20

        hub.speaker.beep(70, 1)

        motor_pair.move(-5)
        rotate_to_degs(270)
        motor_pair.move(10)

        set_gyro_angle(270)

        #SECOND WALL
        while True:
            motor_pair.move(-5)
            rotate_to_degs(0)
            motor_pair.start(speed=100)
            while measure_distance() < start_distance:
                pass
            motor_pair.stop()

            distance = measure_distance()
            robot_position = [0, rectangle_dimensions[1] - distance]
            if distance > rectangle_dimensions[1] - SEARCHING_STEP:
                break
            start_distance += SEARCHING_STEP

            move_to_corner(robot_position, black_corner, use_dist=False)
            while sen_2.get_reflected_light() > 40:
                pass
            motor_pair.move(max(rectangle_dimensions) + 20, speed=100)
            set_gyro_angle(270)

        motor_pair.move(40)



    elif black_corner == (0, 1):
        motor_pair.move(30)
        rotate_to_degs(270)
        motor_pair.move(20)
        set_gyro_angle(270)
        motor_pair.move(-5)
        rotate_to_degs(0)

        motor_pair.start(speed=100)
        while measure_distance() < rectangle_dimensions[1] - SEARCHING_STEP:
            pass
        motor_pair.stop()
        rotate_to_degs(270)
        motor_pair.move(-30)
        rotate_to_degs(0)
        motor_pair.move(15)
        set_gyro_angle(0)

        robot_position = [30, 10]
        start_distance = rectangle_dimensions[0] - 30

        #FIRST WALL

        while True:
            motor_pair.move(-5)
            rotate_to_degs(270)
            motor_pair.start(speed=100)
            while measure_distance() < start_distance:
                pass
            motor_pair.start(speed=-100)
            while measure_distance() > start_distance:
                pass
            motor_pair.stop()

            distance = measure_distance()
            robot_position = [rectangle_dimensions[0] - distance, 0]
            if distance < SEARCHING_STEP:
                break
            start_distance -= SEARCHING_STEP
            if start_distance < 0:
                break

            move_to_corner(robot_position, black_corner, use_dist=False)
            while sen_2.get_reflected_light() > 40:
                pass
            motor_pair.move(max(rectangle_dimensions) + 20, speed=100)
            set_gyro_angle(0)

        start_distance = rectangle_dimensions[1] - 20
        rotate_to_degs(0)
        motor_pair.move(20)
        set_gyro_angle(0)
        motor_pair.move(-5)
        rotate_to_degs(90)
        motor_pair.move(15)
        set_gyro_angle(90)

        #SECOND WALL
        while True:
            motor_pair.move(-5)
            rotate_to_degs(0)
            motor_pair.start(speed=100)
            while measure_distance() < start_distance:
                pass

            motor_pair.start(speed=-100)
            while measure_distance() > start_distance:
                pass
            motor_pair.stop()

            distance = measure_distance()
            robot_position = [rectangle_dimensions[0] - 5, rectangle_dimensions[1] - distance]
            if distance < SEARCHING_STEP:
                break
            start_distance -= SEARCHING_STEP
            if start_distance < 0:
                break

            move_to_corner(robot_position, black_corner, use_dist=False)
            while sen_2.get_reflected_light() > 40:
                pass
            motor_pair.move(max(rectangle_dimensions) + 20, speed=100)
            set_gyro_angle(90)

        move_to_corner(robot_position, (0, 0))
        rotate_to_degs(180)
        motor_pair.move(-30)

elif aligned_degs == 90:
    rotate_to_degs(270)
    black_corner = 0
    for corner in ((1, 1), (0, 1), (0, 0), (1, 0)):
        turn_corner("right")
        follow_wall_until_limit("left")
        if sen_2.get_reflected_light() < 40:
            hub.light_matrix.show_image('HAPPY')
            black_corner = corner
    rotate_to_degs(0)
    align()
