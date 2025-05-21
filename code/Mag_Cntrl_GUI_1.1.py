import PySimpleGUI as pgui
import pyvisa
import time
import matplotlib.pyplot as plt



rm = pyvisa.ResourceManager()
rm.list_resources()

magnet = rm.open_resource('GPIB::1')

m_time = 10

def current_popup(window):
    pop_layout = [
        [pgui.Text("Current too high", font=("Helvetica", 10, "bold"))],
        [pgui.Text('')],
        [pgui.Button("OK"), pgui.Button("CANCEL")]
    ]
    win = pgui.Window("Error", pop_layout, modal=True,
        grab_anywhere=True, enable_close_attempted_event=True, margins=(100,15))
    event, value = win.read()
    if event == pgui.WINDOW_CLOSE_ATTEMPTED_EVENT:
        event = "CANCEL"
    win.close()
def null_popup(window):
    pop_layout = [
        [pgui.Text("Input a current", font=("Helvetica", 10, "bold"))],
        [pgui.Text('')],
        [pgui.Button("OK"), pgui.Button("CANCEL")]
    ]
    win = pgui.Window("Error", pop_layout, modal=True,
        grab_anywhere=True, enable_close_attempted_event=True, margins=(100,15))
    event, value = win.read()
    if event == pgui.WINDOW_CLOSE_ATTEMPTED_EVENT:
        event = "CANCEL"
    win.close()

pgui.theme('LightBrown13')

layout = [[pgui.Text("Current Control:", font=("Helvetica",10, "bold"))],

    [pgui.InputText(do_not_clear=True, key='IN1', enable_events=True, size = 15),
     pgui.Button('Set Current')],

    [pgui.Text("Expected Magnetic Field:", font=("Helvetica",10, "bold"))],

     [pgui.InputText(disabled=True, do_not_clear=True, key='INM', enable_events=True, size = 15),
      pgui.Button('Get Estimate')],

    [pgui.Text("Current Reversal Switch Control:", font=("Helvetica",10, "bold"))],

    [pgui.InputText(disabled=True, do_not_clear=True, key='IN2', enable_events=True, size = 15),
     pgui.Button('Check Polarity'),
     pgui.Button('Switch Polarity')],

    [pgui.Text('')],

    [pgui.Text("Current and Voltage Reading:        ", font=("Helvetica", 10, "bold")),
     pgui.Button('Get Reading'),
     pgui.Button('Clear')],

    [pgui.Multiline(disabled=True, size=(50,10), key='IN3', autoscroll=True)],

    [pgui.Text('')],

    [pgui.Text("Time of Measurement:                 ", font=("Helvetica", 10, "bold")),
     pgui.InputText(do_not_clear=True, key='INTI', enable_events=True, size=10),
     pgui.Button('Set Time')],

    [pgui.Text("Resistance Readings:", font=("Helvetica", 10, "bold")),
    pgui.Button('Get Resistance'),
    pgui.Button('Clear Resistance')],

    [pgui.Multiline(disabled=True, size=(50, 10), key='IN4', autoscroll=True)]]

window = pgui.Window('Magnet Control', layout, margins=(30,15))

while True:
    event, values = window.read()
    if event == pgui.WINDOW_CLOSED:
        break
    if event == 'IN1' and values['IN1'] and values['IN1'][-1] not in ('0123456789.'):
        window['IN1'].update(values['IN1'][:-1])

    if event == 'Set Current':

        if values['IN1'] == "":
            null_popup(window)
        else:
            current = float(values['IN1'])

            bit_factor = 0.0063

            bits = int(current // bit_factor) + 14

            if current > 20:
                current_popup(window)
            elif bits < 10:
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
            else:
                current_popup(window)
        window['IN1'].update('')

    if event == 'Get Estimate':

        window['INM'].update('')

        curr_bit_factor = .0063
        current = (float(magnet.query('R1')) + 14) * curr_bit_factor

        mag_field = current*565.6773841 - 132.8380621

        window['INM'].update(str(int(mag_field)) + ' G')


    if event == 'Check Polarity':
        switch_state = magnet.query('TR3')
        if int(switch_state) == 1:
            window['IN2'].update('REVERSE')
        elif int(switch_state) == 0:
            window['IN2'].update('FORWARD')

    if event == 'Switch Polarity':
        window['IN2'].update('')

        switch_state = magnet.query('TR3')

        if int(switch_state) == 1:
            window['IN2'].update('FORWARD')
        else:
            window['IN2'].update('REVERSE')

        magnet.write('TW21')
        time.sleep(1)
        magnet.write('TW20')

    if event == 'Set Time':
        m_time = int(values['INTI'])
        window['INTI'].update('')

    if event == 'Get Reading':
        curr_bit_factor = .0063
        volt_bit_factor = .0037
        current = (float(magnet.query('R1')) + 14)*curr_bit_factor
        voltage = float(magnet.query('R2'))*volt_bit_factor
        window['IN3'].update('Current: ' + str(round(current, 3)) + ' A' + '\t' + '\t' +
        '\t' + 'Voltage: ' + str(round(voltage, 3)) + ' V' + '\n', append=True)

    if event == 'Clear':
        window['IN3'].update('')

    if event == 'Get Resistance':
        x_val = []
        y_val = []

        rm = pyvisa.ResourceManager()
        rm.list_resources()

        multi = rm.open_resource('GPIB::16')

        for i in range(m_time):
            measurement = multi.query('SENS:DATA?')
            x_val.append(i)
            resistance = float(measurement)
            y_val.append(resistance)

            res_scale = ''

            if resistance < 1000:
                res_scale = '\u03A9'
            elif resistance < 1000000:
                resistance = resistance/1000
                res_scale = 'k\u03A9'
            else:
                resistance = resistance/1000000
                res_scale = 'M\u03A9'

            window['IN4'].update('Time: ' + str(i + 1)  + ' s' + '\t' + '\t' + 'Resistance: ' +
                                 str(round(resistance, 3)) + ' ' + res_scale + '\n', append=True)
            window.refresh()
            time.sleep(1)

        avg_resist = sum(y_val) / len(y_val)

        if avg_resist < 1000:
            res_scale = '\u03A9'
        elif avg_resist < 1000000:
            avg_resist = avg_resist / 1000
            res_scale = 'k\u03A9'
        else:
            avg_resist = avg_resist / 1000000
            res_scale = 'M\u03A9'

        window['IN4'].update('Average Resistance: ' + str(round(avg_resist, 3)) + ' ' + res_scale + '\n', append=True)

        #plt.ylabel('Resistance')
        #plt.xlabel('Time(s)')
        #plt.plot(x_val, y_val, color='blue')

        #plt.show()

    if event == 'Clear Resistance':
        window['IN4'].update('')

window.close()