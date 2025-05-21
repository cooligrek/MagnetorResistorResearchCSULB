import pyvisa
import time

rm = pyvisa.ResourceManager()
rm.list_resources()

magnet = rm.open_resource('GPIB::1')
multimeter = rm.open_resource('GPIB::16')

num_data_points = 100
max_current = 15
current = 0
interval = max_current/num_data_points
cur_val = []
res_val = []
mag_val = []
gain_val = []

for i in range(num_data_points):

    current = current + interval

    bit_factor = 0.0063

    bits = int(current // bit_factor) + 14

    if bits < 10:
        output = 'W0000' + str(bits)
        magnet.write(output)
    elif bits < 100:
        output = 'W000' + str(bits)
        magnet.write(output)
    elif bits < 1000:
        output = 'W00' + str(bits)
        magnet.write(output)
    elif bits < 10000:
        output = 'W0' + str(bits)
        magnet.write(output)
    elif bits < 16384:
        output = 'W' + str(bits)
        magnet.write(output)

    time.sleep(2)

    meas_current = (float(magnet.query('R1')) + 14)*bit_factor

    cur_val.append(meas_current)

    mag_val.append(meas_current*565.6773841 - 132.8380621)

    meas_resist = []

    for m in range(5):

        resistance = float(multimeter.query('SENS:DATA?'))
        meas_resist.append(resistance)
        time.sleep(.4)

    avg_resist = sum(meas_resist) / len(meas_resist)

    res_val.append(avg_resist)

    magnet.write('W00000')

for i in range(num_data_points):
    gain = 100*(res_val[i] - res_val[0])/res_val[0]
    gain_val.append(gain)
for i in range(num_data_points):

    print( str(round(cur_val[i], 3)) + ', ' + str(round(mag_val[i], 3)) + ', '
           + str(round(res_val[i], 3)) + ', ' + str(round(gain_val[i], 5)))


