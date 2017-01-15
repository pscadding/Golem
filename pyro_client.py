# saved as greeting-client.py
import sys
import Pyro4
import Pyro4.util
sys.excepthook = Pyro4.util.excepthook

gc = Pyro4.Proxy("PYRONAME:golem.controller@192.168.0.66:9090") # get a Pyro proxy to the greeting object

gc.move_fowards(2)
gc.move_backwards(2)