import pyvisa
import Prologix_GIDP as pg
import time


rm = pyvisa.ResourceManager()  #Setting up the resource manager to access VISA library
rm.list_resources()

print(rm.list_resources())

test = rm.open_resource('ASRL6::INSTR')

pg.start_GIDP(test, 1)

print("response:", pg.query_GIDP(test, 'MEAS?', 16))

