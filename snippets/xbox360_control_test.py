import pygame
import time

pygame.init()
# Initialize the joysticks
pygame.joystick.init()

joystick_count = pygame.joystick.get_count()
joystick = None
for i in range(joystick_count):
    j = pygame.joystick.Joystick(i)
    j.init()
    if "Xbox" in j.get_name():
        j.init()
        joystick = j

direction_axis = 0
trigger_axis = 2


while True:
    # joystick.init()
    pygame.event.get()


    direction = joystick.get_axis(direction_axis)
    drive = joystick.get_axis(trigger_axis)

    # print("direction",direction)
    # print("backwards",backwards)
    print("direction",direction)
    time.sleep(0.1)



# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()