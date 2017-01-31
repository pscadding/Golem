import pygame
import time

class DirectInput(object):

    deadZone = 0.2

    def __init__(self, gc):

        self.gc = gc

        pygame.init()
        # Initialize the joysticks
        pygame.joystick.init()

        joystick_count = pygame.joystick.get_count()
        self.joystick = None
        for i in range(joystick_count):
            j = pygame.joystick.Joystick(i)
            if "Xbox" in j.get_name():
                j.init()
                self.joystick = j

        self.direction_axis = 0
        self.trigger_axis = 2

    def run(self):
        randt = lambda x: abs(int(x * 100))
        while True:
            pygame.event.get()
            direction = self.dead_zone(self.joystick.get_axis(self.direction_axis))
            drive = -self.dead_zone(self.joystick.get_axis(self.trigger_axis))
            left  = -direction
            right = direction
            left += drive
            right += drive

            # get the maximum absolute value
            maximum = max(abs(left),abs(right))
            if maximum > 1:
                print("normalizing")
                left = left / maximum
                right = right / maximum


            print("left",left)
            print("right",right)

            # drive_turn_offset = 0.2

            # if drive < 0:
            #     drive = -drive
            #     move_args = [int(drive * 100), 0, int(drive * 100), 0]
            # else:
            #     move_args = [0,int(drive * 100), 0, int(drive * 100)]

            move_args = [0, 0, 0, 0]

            if left > 0:
                move_args[2] = randt(left)
            else:
                move_args[3] = randt(left)

            if right > 0:
                move_args[0] = randt(right)
            else:
                move_args[1] = randt(right)


            # print(move_args)
            self.gc.move(*move_args)

    def dead_zone(self,value):
        if value <= self.deadZone and value >= -self.deadZone:
            return 0
        return value

    # pygame.quit()