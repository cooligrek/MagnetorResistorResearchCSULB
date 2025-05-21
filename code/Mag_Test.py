import pyvisa


rm = pyvisa.ResourceManager()  #Setting up the resource manager to access VISA library
rm.list_resources()

magnet = rm.open_resource('GPIB::1')

print(magnet.write('W05100'))


