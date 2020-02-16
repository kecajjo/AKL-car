# all commands for car
nothing = 0

car = 1

turn_right = 2
turn_left = 3
go_forward = 4
go_backward = 5
stop = 10

gimbal_up = 6
gimbal_down = 7

camer_on = 8
camera_of = 9


SET_SPEED = 2.3

# replies for master
master = 100

port = 7012


# motors
AIN1 = 13
AIN2 = 19
PWMA = 26
BIN1 = 21
BIN2 = 20
PWMB = 16
FREQUENCY = 50

STANDARD_PWM1 = 80
STANDARD_PWM2 = 80

# range sensor
TRIG_PIN = 6
COLLISION_DISTANCE = 15 # actually used in send_orders

# servo
MAX_PWM = 9
MIN_PWM = 3
FREQ = 50
SINGLE_POS_CHANGE = 10
SERVO_PIN = 4


# encoders
ENCODER1_PIN = 23
ENCODER2_PIN = 17

NUM_OF_SAMPLES = 60
WINDOW_LENGTH = 0.7 #(seconds)
TRANSMISSION_FACTOR =1/34 # = 1/36;

# PID

MAX_PWM = 100 # percentage
SAMPLE_TIME = WINDOW_LENGTH # seconds so encoders and PID have same sample rate
PROP = 1
INTEG = 0.0001
DERIV = 0.0001
# MAX_MOTOR_SPEED = 300