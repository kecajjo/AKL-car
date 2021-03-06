# from queue import Queue
# import constant_values
from time import sleep
from motors_movement import *
from servo import *
from PID import *
from Encoder import *
from constant_values import *
from grove_ultrasonic import *



motor = motors_movement()
gimbal = servo()
encoder1 = Encoder(ENCODER1_PIN)
encoder2 = Encoder(ENCODER2_PIN)
distance_grove = Measurement()


def start_sending_orders(orders):
    target = 0
    prev_target = 0
    pwm1 = STANDARD_PWM1
    pwm2 = STANDARD_PWM2
    pid1 = PID(P=PROP, I=INTEG, D=DERIV)
    pid2 = PID(P=PROP, I=INTEG, D=DERIV)
    pid1.setSampleTime(SAMPLE_TIME)
    pid2.setSampleTime(SAMPLE_TIME)
    while 1:
        if not orders.empty():
            try:
                target, value2, value3 = orders.get()
                print_order(target)
                if target == 6:
                    gimbal.move_up()
                if target == 7:
                    gimbal.move_down()
            except:
                print("\n\nsend_orders \t error: 1\n\n")
        if (target > 1 and target < 6) or target == 10:
    
            if target == prev_target:
                try:
                    set_point = SET_SPEED
                    if target == 10: # to be removed later
                        set_point = 0 # to be removed later
                    print('speed1, speed 2: {:3.2f} {:3.2f}'.format(encoder1.speed,encoder2.speed), end='\t')
                    print('error1, error2: {:3.2f} {:3.2f}'.format(encoder1.speed-set_point,encoder2.speed-set_point), end='\t')
                    # speed_abs1 = abs(encoder1.speed)
                    # speed_abs2 = abs(encoder2.speed)
                    ############################
                    #  to do:                  #
                    #  handle problem when     #
                    #  1 encoder stops working #
                    ############################

                    #####################################
                    # WATCH OUT (to be checked)         #
                    # it does make difference which     #
                    # encoder is on which pin           #
                    #####################################
                    
                    # if speed_abs1 != 0 and speed_abs2 != 0:
                    #     pwm2 = pid.count_motor_pwm(encoder1.speed,encoder2.speed)
                    # else:
                    #     pwm2 = 0
                    pwm1 = pid1.count_motor_pwm(set_point,encoder1.speed, pwm1)
                    pwm2 = pid2.count_motor_pwm(set_point,encoder2.speed, pwm2)
                    print('pwm1, pwm2 from PID: {:3.2f} {:3.2f}'.format(pwm1,pwm2))
                except:
                    print("\n\nsend_orders \t error: 2.1\n\n")
            else:
                try:

                    ############################
                    #  to do:                  #
                    #  fix encoders/pid clear  #
                    #  cose not working at all #
                    ############################
                    # print('{} {}' .format(target,prev_target))
                    pwm1 = STANDARD_PWM1 # setting pwm for both motors after changing order
                    pwm2 = STANDARD_PWM2
                    pid.clear() # clearing pid after changing order
                    encoder1.clear() # same goes for encoders
                    encoder2.clear()
                except:
                    print("\n\nsend_orders \t error: 2.2\n\n")
            try:
                if target == 2:
                    motor.turn_right(pwm1,pwm2)
                if target == 3:
                    motor.turn_left(pwm1,pwm2)
                if target == 4:
                    motor.move_forth(pwm1,pwm2)
                if target == 5:
                    motor.move_back(pwm1,pwm2)
                if target == 10:
                    motor.stop()
                prev_target = target # changing prev_target only if target affects motors
            except:
                print("\n\nsend_orders \t error: 3\n\n")

        distance_grove.distance()
        # print('distance: {:3.2f}' .format(distance_grove.distance_cm))
        if target == 4 and distance_grove.distance_cm < COLLISION_DISTANCE:
            motor.stop()
            target = 10
            prev_target = 10
            print("STOPPED IN CASE OF COLLISION")
        sleep(0.001) # not sure if it should be there    

def print_order(target):
    if target == 6:
        print("\ngimbal moving up\n")
    elif target == 7:
        print("\ngimbal moving down\n")
    elif target == 2:
        print("\nturning right\n")
    elif target == 3:
        print("\nturning left\n")
    elif target == 4:
        print("\nmoving forward\n")
    elif target == 5:
        print("\nmoving back\n")
    elif target == 10:
        print("\nstop\n")
    else:
        print("\n\nUNKNOWN COMMAND\n\n")