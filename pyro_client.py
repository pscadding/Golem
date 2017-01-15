# saved as greeting-client.py
import sys
import Pyro4
import Pyro4.util
Pyro4.config.HOST = "192.168.0.66"
sys.excepthook = Pyro4.util.excepthook

name = "123" # input("What is your name? ").strip()

gc = Pyro4.Proxy("PYRONAME:golem.controller@192.168.0.66:9090") # get a Pyro proxy to the greeting object

# print(gc.move_foward(0.01))   # call method normally