import pyvisa
import matplotlib.pyplot as plt
import time

x_val = []
y_val = []
res_scale = ''

rm = pyvisa.ResourceManager()
rm.list_resources()

multi = rm.open_resource('GPIB::16')

for i in range(30):

    measurement = multi.query('SENS:DATA?')
    x_val.append(i)
    resistance = float(measurement)

    if resistance < 1000:
        resistance = resistance
        res_scale = '\u03A9'
    elif resistance < 1000000:
        resistance = resistance / 1000
        res_scale = 'k\u03A9'
    else:
        resistance = resistance / 1000000
        res_scale = 'M\u03A9'

    y_val.append(resistance)

    time.sleep(1)


avg_resist = sum(y_val) / len(y_val)

print(avg_resist)

plt.ticklabel_format(useOffset=False)
plt.ylabel('Resistance(' + res_scale + ')')
plt.xlabel('Time(s)')
plt.plot(x_val, y_val, color= 'blue')

plt.show()
