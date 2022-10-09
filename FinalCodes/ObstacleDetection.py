def obstacle_detection():
    dist_cm = get_distance()
    if dist_cm > 5:
        motor_pair.start_tank(50, 50)
        dist_cm = get_distance()
    dist_cm = get_distance()
    color_2 = sen_2.get_reflected_light()
    while ((dist_cm) < 10):
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
    opciones_de_giro = [1, 2]
    op = random.choice(opciones_de_giro)
    if op == 1:
        op_ant = 1
        girar_num_grados_der(45)
        dist_cm = get_distance()
        if (dist_cm > 20):
            hub.light_matrix.show_image('HAPPY')
            girar_num_grados_der(35)
            dist_cm = get_distance()
            if (dist_cm > 20):
                motor_pair.move_tank(3.5, 'cm', -30, 78) # Antes estaba en 24
                motor_pair.move_tank(15, 'cm', 32, 78)
                hub.light_matrix.show_image('HEART')
                timer.reset()
                color_2 = sen_2.get_reflected_light()
                while (color_2 > 20): # Antes estaba en 45
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(29, 75)
                    if (timer.now() > 1):
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
                motor_pair.move_tank(3, 'cm', 60, 60)
                while color_2 > 20:
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(30, -30)
                motor_pair.start_tank(0, 0)
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
            motor_pair.move_tank(3, 'cm', 60, 60)
            while color_2 > 20:
                color_2 = sen_2.get_reflected_light()
                motor_pair.start_tank(30, -30)
            motor_pair.start_tank(0, 0)
    elif (op == 2):
        hub.motion_sensor.reset_yaw_angle()
        while (hub.motion_sensor.get_yaw_angle() > -44):
            motor_pair.start_tank(-35, 40)
        hub.motion_sensor.reset_yaw_angle()
        motor_pair.start_tank(0, 0)
        dist_cm = get_distance()
        if (dist_cm > 20):
            hub.light_matrix.show_image('HAPPY')
            hub.motion_sensor.reset_yaw_angle()
            while (hub.motion_sensor.get_yaw_angle() > -35):
                motor_pair.start_tank(-35, 40)
            hub.motion_sensor.reset_yaw_angle()
            dist_cm = get_distance()
            if (dist_cm > 20):
                motor_pair.move_tank(5, 'cm', 76, 35) # Antes estaba en 24
                motor_pair.move_tank(16, 'cm', 75, 32)
                hub.light_matrix.show_image('HEART')
                timer.reset()
                color_2 = sen_2.get_reflected_light()
                while (color_2 > 20): # Antes estaba en 45
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(75, 24)
                    if (timer.now() > 1.6):
                        color_2 = sen_2.get_reflected_light()
                        while (color_2 > 20):
                            color_2 = sen_2.get_reflected_light()
                            motor_pair.start_tank(75, 18)
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
                    motor_pair.start_tank(-30, 30)
                motor_pair.start_tank(0, 0)

            else:
                color_2 = sen_2.get_reflected_light()
                hub.light_matrix.show_image('ANGRY')
                hub.motion_sensor.reset_yaw_angle()
                while (hub.motion_sensor.get_yaw_angle() > 159):
                    motor_pair.start_tank(35, -40)
                hub.motion_sensor.reset_yaw_angle()
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(3.5, 'cm', 20, 60)
                motor_pair.move_tank(13, 'cm', 30, 80)
                hub.light_matrix.show_image('HEART')
                timer.reset()
                color_2 = sen_2.get_reflected_light()
                while (color_2 > 20): # Antes estaba en 45
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(30, 80)
                    if (timer.now() > 1.5):
                        color_2 = sen_2.get_reflected_light()
                        while (color_2 > 20):
                            color_2 = sen_2.get_reflected_light()
                            motor_pair.start_tank(17, 80) # Antes eran 80/18
                            timer.reset()
                motor_pair.start_tank(0, 0)
                color_2 = sen_2.get_reflected_light()
                hub.motion_sensor.reset_yaw_angle()
                while (hub.motion_sensor.get_yaw_angle() < 70):
                    angle = hub.motion_sensor.get_yaw_angle()
                    print(angle)
                    motor_pair.start_tank(-35, 40)
                motor_pair.start_tank(0, 0)
                while color_2 > 20:
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(30, -30)
                motor_pair.start_tank(0, 0)
        else:
            color_2 = sen_2.get_reflected_light()
            hub.light_matrix.show_image('ANGRY')
            hub.motion_sensor.reset_yaw_angle()
            while (hub.motion_sensor.get_yaw_angle() > 109):
                motor_pair.start_tank(-35, 40)
            hub.motion_sensor.reset_yaw_angle()
            motor_pair.start_tank(0, 0)
            motor_pair.move_tank(3.5, 'cm', 45, 60)
            motor_pair.move_tank(13, 'cm', 38, 75)
            hub.light_matrix.show_image('HEART')
            timer.reset()
            color_2 = sen_2.get_reflected_light()
            while (color_2 > 20): # Antes estaba en 45
                color_2 = sen_2.get_reflected_light()
                motor_pair.start_tank(30, 80)
                if (timer.now() > 1.5):
                    color_2 = sen_2.get_reflected_light()
                    while (color_2 > 20):
                        color_2 = sen_2.get_reflected_light()
                        motor_pair.start_tank(30, 80) # Antes eran 80/18
                        timer.reset()
            motor_pair.start_tank(0, 0)
            color_2 = sen_2.get_reflected_light()
            hub.motion_sensor.reset_yaw_angle()
            while (hub.motion_sensor.get_yaw_angle() < 70):
                angle = hub.motion_sensor.get_yaw_angle()
                print(angle)
                motor_pair.start_tank(-35, 40)
            motor_pair.start_tank(0, 0)
            while color_2 > 20:
                color_2 = sen_2.get_reflected_light()
                motor_pair.start_tank(30, -30)
            motor_pair.start_tank(0, 0)
    mostrar(nada)