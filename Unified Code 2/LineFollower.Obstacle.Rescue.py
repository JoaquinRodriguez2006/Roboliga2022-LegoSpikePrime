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

##############################################################
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
    if sen_2.get_reflected_light() > 85:
        break
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

# MOTORES
motor_pair = MotorPair('A', 'C')
motor_pair.set_motor_rotation(1.07 * math.pi, "cm")

def do_wall_pass(alignment_angle, target_corner, rectangle_dimensions, wall_alignment="x", start_corner=(0, 0), sensor_forward=True, searching_step=10, stop_distance=10, init_start_distance=10):
    global motor_pair

    if wall_alignment == "y":
        if start_corner[1] == 1:
            turn_angle = alignment_angle - 90
        elif start_corner[1] == 0:
            turn_angle = alignment_angle - 90

    elif wall_alignment == "x":
        if start_corner[0] == 1:
            turn_angle = alignment_angle - 90
        elif start_corner[0] == 0:
            turn_angle = alignment_angle - 90


    if not sensor_forward:
        turn_angle += 180

    turn_angle = normalize_degs(turn_angle)

    if sensor_forward:
        if wall_alignment == "x":
            start_distance = rectangle_dimensions[0] - init_start_distance
        elif wall_alignment == "y":
            start_distance = rectangle_dimensions[1] - init_start_distance

        while True:
            motor_pair.move(-5)
            rotate_to_degs(turn_angle)
            motor_pair.start(speed=100)
            while True:
                distance = measure_distance()
                if distance > start_distance:
                    break
            motor_pair.stop()
            motor_pair.start(speed=-100)
            while True:
                distance = measure_distance()
                if distance < start_distance or distance < stop_distance:
                    break
            motor_pair.stop()

            distance = measure_distance()
            if wall_alignment == "x":
                if start_corner == (0, 0):
                    robot_position = [rectangle_dimensions[0] - distance, 10]
                elif start_corner == (0, 1):
                    robot_position = [rectangle_dimensions[0] - distance, rectangle_dimensions[1] - 10]
                elif start_corner == (1, 1):
                    robot_position = [distance, rectangle_dimensions[1] - 10]
                elif start_corner == (1, 0):
                    robot_position = [distance, 10]


            else:
                if start_corner == (0, 0):
                    robot_position = [10, rectangle_dimensions[1] - distance]
                elif start_corner == (0, 1):
                    robot_position = [10, distance]
                elif start_corner == (1, 1):
                    robot_position = [rectangle_dimensions[0] - 10, distance]
                elif start_corner == (1, 0):
                    robot_position = [rectangle_dimensions[0] - 10, rectangle_dimensions[1] - distance]


            if distance < stop_distance:
                break
            start_distance -= searching_step

            move_to_corner(robot_position, target_corner, use_dist=False)
            while sen_2.get_reflected_light() > 40:
                pass

            motor_pair.move(max(rectangle_dimensions) + 20, speed=100)
            set_gyro_angle(alignment_angle)

    else:
        start_distance = init_start_distance
        while True:
            motor_pair.move(-5)
            rotate_to_degs(turn_angle)
            motor_pair.start(speed=-100)
            while True:
                distance = measure_distance()
                if distance < start_distance:
                    break
            motor_pair.stop()
            motor_pair.start(speed=100)
            while True:
                distance = measure_distance()
                if wall_alignment == "x":
                    if distance > start_distance or distance > rectangle_dimensions[0] - stop_distance:
                        break
                elif wall_alignment == "y":
                    if distance > start_distance or distance > rectangle_dimensions[1] - stop_distance:
                        break

            motor_pair.stop()

            distance = measure_distance()
            if wall_alignment == "x":
                if start_corner == (0, 0):
                    robot_position = [distance, 10]
                elif start_corner == (0, 1):
                    robot_position = [distance, rectangle_dimensions[1] - 10]
                elif start_corner == (1, 1):
                    robot_position = [rectangle_dimensions[0] - distance, rectangle_dimensions[1] - 10]
                elif start_corner == (1, 0):
                    robot_position = [rectangle_dimensions[0] - distance, 10]


            else:
                if start_corner == (0, 0):
                    robot_position = [10, distance]
                elif start_corner == (0, 1):
                    robot_position = [10, rectangle_dimensions[1] - distance]
                elif start_corner == (1, 1):
                    robot_position = [rectangle_dimensions[0] - 10, rectangle_dimensions[1] - distance]
                elif start_corner == (1, 0):
                    robot_position = [rectangle_dimensions[0] - 10, distance]


            if (wall_alignment == "x" and distance > rectangle_dimensions[0] - stop_distance) or (wall_alignment == "y" and distance > rectangle_dimensions[1] - stop_distance):
                break
            start_distance += searching_step

            move_to_corner(robot_position, target_corner, use_dist=False)
            while sen_2.get_reflected_light() > 40:
                pass

            motor_pair.move(max(rectangle_dimensions) + 20, speed=100)
            set_gyro_angle(alignment_angle)

possible_corners = [(0, 0), (0, 1), (1, 1), (1, 0)]

motor_pair.move(-30)

aligned_degs = align()

#motor_pair.move(-30, speed=100)

rectangle_dimensions = [120, 90]
#rectangle_dimensions, robot_position = measure_and_locate()

#motor_pair.move(30, speed=100)

SEARCHING_STEP = 20

STOP_DISTANCE = 20

if aligned_degs == 270:
    rotate_to_degs(90)
    black_corner = None
    for corner in ((0, 1), (1, 1), (1, 0), (0, 0)):
        turn_corner("left")
        follow_wall_until_limit("right", limit=10)
        if sen_2.get_reflected_light() < 40:
            hub.light_matrix.show_image('HAPPY')
            black_corner = corner
            break


    if black_corner == (1, 1):
        motor_pair.move(max(rectangle_dimensions), speed=100)
        set_gyro_angle(270)
        robot_position = [10, rectangle_dimensions[1]]

        #FIRST WALL
        do_wall_pass(
            alignment_angle=270,
            target_corner=black_corner,
            rectangle_dimensions=rectangle_dimensions,
            wall_alignment="y",
            start_corner=(0, 1),
            sensor_forward=False,
            searching_step=20,
            stop_distance=10,
            init_start_distance=20)

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

        do_wall_pass(
            alignment_angle=0,
            target_corner=black_corner,
            rectangle_dimensions=rectangle_dimensions,
            wall_alignment="x",
            start_corner=(0, 0),
            sensor_forward=True,
            searching_step=20,
            stop_distance=10,
            init_start_distance=40)

        motor_pair.move(max(rectangle_dimensions) + 20, speed=100)
        motor_pair.move(-5)
        rotate_to_degs(180)
        motor_pair.move(-30)


    elif black_corner == (1, 0):
        motor_pair.move(max(rectangle_dimensions), speed=100)
        set_gyro_angle(180)
        robot_position = [rectangle_dimensions[0], rectangle_dimensions[1]]

        #FIRST WALL
        do_wall_pass(
            alignment_angle=180,
            target_corner=black_corner,
            rectangle_dimensions=rectangle_dimensions,
            wall_alignment="x",
            start_corner=(1, 1),
            sensor_forward=True,
            searching_step=20,
            stop_distance=10,
            init_start_distance=20)

        robot_position = [0, rectangle_dimensions[1]]

        hub.speaker.beep(70, 1)

        motor_pair.move(-5)
        rotate_to_degs(270)
        motor_pair.move(10)

        set_gyro_angle(270)

        #SECOND WALL
        do_wall_pass(
            alignment_angle=270,
            target_corner=black_corner,
            rectangle_dimensions=rectangle_dimensions,
            wall_alignment="y",
            start_corner=(0, 1),
            sensor_forward=False,
            searching_step=20,
            stop_distance=10,
            init_start_distance=20)

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

        #FIRST WALL
        do_wall_pass(
            alignment_angle=0,
            target_corner=black_corner,
            rectangle_dimensions=rectangle_dimensions,
            wall_alignment="x",
            start_corner=(0, 0),
            sensor_forward=True,
            searching_step=20,
            stop_distance=15,
            init_start_distance=40)

        rotate_to_degs(0)
        motor_pair.move(20)
        set_gyro_angle(0)
        motor_pair.move(-5)
        rotate_to_degs(90)
        motor_pair.move(15)
        set_gyro_angle(90)

        #SECOND WALL
        do_wall_pass(
            alignment_angle=90,
            target_corner=black_corner,
            rectangle_dimensions=rectangle_dimensions,
            wall_alignment="y",
            start_corner=(1, 0),
            sensor_forward=True,
            searching_step=20,
            stop_distance=15,
            init_start_distance=20)

        move_to_corner(robot_position, (0, 0))
        rotate_to_degs(180)
        motor_pair.move(-30)


elif aligned_degs == 90:
    rotate_to_degs(270)
    black_corner = None
    for corner in ((1, 1), (0, 1), (0, 0), (1, 0)):
        turn_corner("right")
        follow_wall_until_limit("left")
        if sen_2.get_reflected_light() < 40:
            hub.light_matrix.show_image('HAPPY')
            black_corner = corner
    rotate_to_degs(0)


    if black_corner == (1, 1):
        pass


    elif black_corner == (1, 0):
        pass



    elif black_corner == (0, 1):
        motor_pair.move(max(rectangle_dimensions), speed=100)
        set_gyro_angle(90)
        robot_position = [rectangle_dimensions[0], rectangle_dimensions[1]]

        #FIRST WALL
        do_wall_pass(
            alignment_angle=90,
            target_corner=black_corner,
            rectangle_dimensions=rectangle_dimensions,
            wall_alignment="y",
            start_corner=(1, 1),
            sensor_forward=False,
            searching_step=20,
            stop_distance=15,
            init_start_distance=20)

        rotate_to_degs(90)
        motor_pair.move(20)
        set_gyro_angle(90)
        motor_pair.move(-40)
        rotate_to_degs(0)
        motor_pair.move(15)
        set_gyro_angle(0)

        #SECOND WALL
        do_wall_pass(
            alignment_angle=0,
            target_corner=black_corner,
            rectangle_dimensions=rectangle_dimensions,
            wall_alignment="x",
            start_corner=(1, 0),
            sensor_forward=True,
            searching_step=20,
            stop_distance=15,
            init_start_distance=40)