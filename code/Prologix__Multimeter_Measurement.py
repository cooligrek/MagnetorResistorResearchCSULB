import pyvisa
import Prologix_GIDP as pg
import matplotlib.pyplot as plt
import time

x_val = []
y_val = []
res_scale = ''

rm = pyvisa.ResourceManager()
multi = rm.open_resource('ASRL6::INSTR')
pg.start_GIDP(multi, 16)

for i in range(30):

    measurement = pg.query_MM_value_GIDP(multi, 'RES', 16)
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
