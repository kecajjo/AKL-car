# from queue import Queue
# import constant_values
from time import sleep
from motors_movement import *
from servo import *
import PID
import Encoder
from constant_values import *


motor = motors_movement()
gimbal = servo()
encoder1 = Encoder.Encoder(ENCODER1_A_PIN, ENCODER1_B_PIN)
encoder2 = Encoder.Encoder(ENCODER2_A_PIN, ENCODER2_B_PIN)


def start_sending_orders(orders):
    target = 0
    prev_target = 0
    pwm1 = STANDARD_PWM1
    pid = PID.PID(P=0.8, I=0.0, D=0.0)
    while 1:
        if not orders.empty():
            try:
                target, value2, value3 = orders.get()
                if target == 6:
                    gimbal.move_up()
                    print("gimbal moving up")
                if target == 7:
                    gimbal.move_down()
                    print("gimbal moving down")
            except:
                print("smthin fcked up")
        if (target > 1 and target < 6) or target == 10:
            try:
                if target == prev_target:
                    if encoder1.speed is not None and encoder2.speed is not None:
                        speed_abs1 = abs(encoder1.speed)
                        speed_abs2 = abs(encoder2.speed)
                        pwm2 = pid.count_motor_pwm(speed_abs1,speed_abs2)
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
                print("smthin fcked up")            