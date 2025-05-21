import pyvisa
import time


def start_GIDP(resource, address, baudRate=9600, dataBits=8, timeout = 2000):

    resource.baud_rate = baudRate           # Set Baud rate
    resource.data_bits = dataBits
    resource.parity = pyvisa.constants.Parity.none
    resource.stop_bits = pyvisa.constants.StopBits.one
    resource.timeout = timeout

    resource.write("++mode 1")          # Set to controller mode
    resource.write("++auto 0")          # Turn off auto read
    resource.write(f"++addr {address}") # Set GPIB address of your instrument
    resource.write("++eos 3")           # CR + LF (return cursor to start of line + put cursor down to next line)
    resource.write("++eoi 1")           # End of line signal

    resource.write('*CLS')              # Clear
    resource.write("*RST")              # Reset
    resource.write(':OUTP ON')          # Output On

def query_GIDP(resource, query, address):

    resource.write(f"++addr {address}")
    resource.write(query)
    time.sleep(0.1)
    resource.write("++read eoi")
    return resource.read()

def query_MM_value_GIDP(resource, value, address):

    #resource.write(f"++addr {address}")
    resource.write(f':FORM:ELEM {value}')
    resource.write(f'MEAS:{value}?')
    time.sleep(0.1)
    resource.write("++read eoi")
    return resource.read().strip()

