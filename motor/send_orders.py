# from queue import Queue
# import constant_values
from time import sleep
from motors_movement import *
from servo import *

motor = motors_movement()
gimbal = servo()

def start_sending_orders(orders):
    target = 0
    while 1:
        if not orders.empty():
            try:
                target, value2, value3 = orders.get()
                if target == 10:
                    motor.stop()
                if target == 6:
                    gimbal.move_up()
                    print("gimbal moving up")
                if target == 7:
                    gimbal.move_down()
                    print("gimbal moving down")
            except:
                print("smthin fcked up")
        if target > 1 and target < 6:
            try:
                # ----------------------------------------------------------------------#
                # missing function calculating pwm1 and pwm2 basing on PID and encoders #
                #-----------------------------------------------------------------------#
                pwm1 = 50
                pwm2 = 50 # in final version PID will calculate it
                if target == 2:
                    motor.turn_right(pwm1, pwm2)
                if target == 3:
                    motor.turn_left(pwm1, pwm2)
                if target == 4:
                    motor.move_forth(pwm1, pwm2)
                if target == 5:
                    motor.move_back(pwm1, pwm2)
            except:
                print("smthin fcked up")            
        sleep(1) #just for now
