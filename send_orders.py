# from queue import Queue
# import constant_values
from time import sleep
from motors_movement import *
from servo import *
from PID import *
from Encoder import *
from constant_values import *


motor = motors_movement()
gimbal = servo()
encoder1 = Encoder(ENCODER1_A_PIN, ENCODER1_B_PIN)
encoder2 = Encoder(ENCODER2_A_PIN, ENCODER2_B_PIN)


def start_sending_orders(orders):
    target = 0
    prev_target = 0
    pwm1 = STANDARD_PWM1
    pid = PID(P=0.8, I=0.0, D=0.0)
    pid.setSampleTime(SAMPLE_TIME)
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
                print("\n\nsmthin fcked up\n\n")
        if (target > 1 and target < 6) or target == 10:
            try:
                if target == prev_target:
                    if encoder1.speed is not None and encoder2.speed is not None:
                        print('speed1: {:3f}\t'.format(encoder1.speed))
                        print('speed2: {:3f}\t'.format(encoder2.speed))
                        speed_abs1 = abs(encoder1.speed)
                        speed_abs2 = abs(encoder2.speed)
                        pwm2 = pid.count_motor_pwm(speed_abs1,speed_abs2)
                        print('pwm2 from PID: {:3f}\t'.format(pwm2))
                else:
                    pid.clear() # clearing pid after changing order
                    encoder1.clear() # same goes for encoders
                    encoder2.clear()
                    pwm1 = STANDARD_PWM1 # setting pwm for both motors after changing order
                    pwm2 = STANDARD_PWM2

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
                print("\n\nsmthin fcked up\n\n")
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