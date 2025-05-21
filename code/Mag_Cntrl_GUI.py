import PySimpleGUI as pgui
import pyvisa
import time

rm = pyvisa.ResourceManager()
rm.list_resources()

magnet = rm.open_resource('GPIB::1')

def current_popup(window):
    pop_layout = [
        [pgui.Text("Current too high")],
        [pgui.Button("OK"), pgui.Button("CANCEL")]
    ]
    win = pgui.Window("Error", pop_layout, modal=True,
        grab_anywhere=True, enable_close_attempted_event=True)
    event, value = win.read()
    if event == pgui.WINDOW_CLOSE_ATTEMPTED_EVENT:
        event = "CANCEL"
    win.close()
def null_popup(window):
    pop_layout = [
        [pgui.Text("Input a current")],
        [pgui.Button("OK"), pgui.Button("CANCEL")]
    ]
    win = pgui.Window("Error", pop_layout, modal=True,
        grab_anywhere=True, enable_close_attempted_event=True)
    event, value = win.read()
    if event == pgui.WINDOW_CLOSE_ATTEMPTED_EVENT:
        event = "CANCEL"
    win.close()

pgui.theme('Reddit')

layout = [[
    pgui.InputText(do_not_clear=True, key='IN1', enable_events=True, size = 15),
    pgui.Button('Set Current')],

    [pgui.InputText(do_not_clear=True, key='IN2', enable_events=True, size = 15),
    pgui.Button('Switch Polarity')]]


window = pgui.Window('Magnet Control', layout, margins=(75,50))

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

            bit_factor = 0.00628

            bits = int(current // bit_factor)

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
        
    if event == 'Switch Polarity':
        magnet.write('TW21')
        time.sleep(1)
        magnet.write('TW20')

window.close()