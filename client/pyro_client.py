# saved as greeting-client.py
import sys
import os
import Pyro4
import Pyro4.util
sys.excepthook = Pyro4.util.excepthook
sys.path.append( os.path.dirname(os.path.dirname(__file__)))


basic_address = "PYRONAME:{0}@192.168.0.66:9090"
gc = Pyro4.Proxy(basic_address.format("golem.controller")) # get a Pyro proxy to the Golem object

import voice_control
import direct_input

vc = voice_control.VoiceControl(gc)
di = direct_input.DirectInput(gc)

di.run()
# def direct_control():
#     t = time.time()
#     i = 10
#     while time.time() - t < 3:
#         if i < 100:
#             i += 0.4
#         gc.move(int(i),0,int(i),0)
#     gc.stop()
#
# direct_control()




# gc.move_forwards(2,"normal")
# gc.move_left(1,"slow")
# gc.move_right(1,"normal")
# gc.move_left(1,"fast")
# gc.move_forwards(1,"normal")
# gc.move_forwards(1,"fast")

# gc.move_forwards(2,"slow")
# gc.move_forwards(2,"normal")
# gc.move_forwards(2,"fast")
