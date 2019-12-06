from time import sleep

# loops simulate function with PID included

class motors_movement():
    
    def move_forth(self,my_queue,speed=50):
        while my_queue.empty():
            print("moving forth")
            sleep(1.5)


    def move_back(self,my_queue,speed=50):
        while my_queue.empty:
            print("moving back")
            sleep(1.5)

    def turn_left(self,my_queue,speed=50):
        while my_queue.empty():
            print("turning left")
            sleep(1.5)

    def turn_right(self,my_queue,speed=50):
        while my_queue.empty():
            print("turning right")
            sleep(1.5)

    def stop(self):
        print("stop")
       