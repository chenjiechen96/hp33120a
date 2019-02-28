import tkinter as tk
from tkinter import *
from tkinter import messagebox
import serial
import serial.tools.list_ports
import instruments as ik

window = tk.Tk()
window.title('HP-33120A Function Generator')
window.geometry('350x350')


def serial_port_check():
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) <= 0:
        port_info.set('The serial port cannot find!')
    else:
        port_info.set(port_list)


port_info = tk.StringVar()
port_check_x = 0
port_check_y = 0
SerialPortCheckButton = tk.Button(window, text='Serial Port Check', width=13, height=1, command=serial_port_check)
SerialPortCheckButton.place(x=port_check_x, y=port_check_y)
SerialPortCheckResults = tk.Label(window, textvariable=port_info, bg='light gray', width=25, height=2)
SerialPortCheckResults.place(x=port_check_x+100, y=port_check_y)

port_set = StringVar()
port_set_x = 0
port_set_y = 60
PortSet = tk.Label(window, text='Port:', width=3)
PortSet.place(x=port_set_x, y=port_set_y)
PortInput = tk.Entry(window, width=3, textvariable=port_set)
PortInput.place(x=port_set_x+30, y=port_set_y)
PortInput.insert(END, '70')

addr_set = StringVar()
addr_set_x = 60
addr_set_y = 60
AddrSet = tk.Label(window, text='Addr:', width=3)
AddrSet.place(x=addr_set_x, y=addr_set_y)
AddrInput = tk.Entry(window, width=3, textvariable=addr_set)
AddrInput.place(x=addr_set_x+30, y=addr_set_y)
AddrInput.insert(END, '10')

baud_set = StringVar()
baud_set_x = 0
baud_set_y = 90
BaudSet = tk.Label(window, text='Baud:', width=3)
BaudSet.place(x=baud_set_x, y=baud_set_y)
BaudInput = tk.Entry(window, width=10, textvariable=baud_set)
BaudInput.place(x=baud_set_x+30, y=baud_set_y)
BaudInput.insert(END, '9600')

freq_set = StringVar()
freq_set_x = 0
freq_set_y = 120
FreqSet = tk.Label(window, text='Freq:', width=3)
FreqSet.place(x=freq_set_x, y=freq_set_y)
FreqInput = tk.Entry(window, width=10, textvariable=freq_set)
FreqInput.place(x=freq_set_x+30, y=freq_set_y)
FreqUnit = tk.Label(window, text='MHz', width=3)
FreqUnit.place(x=freq_set_x+100, y=freq_set_y)
FreqInput.insert(END, '12.8')

power_set = StringVar()
power_set_x = 0
power_set_y = 150
PowerSet = tk.Label(window, text='Pwr:', width=3)
PowerSet.place(x=power_set_x, y=power_set_y)
PowerInput = tk.Entry(window, width=10, textvariable=power_set)
PowerInput.place(x=power_set_x+30, y=power_set_y)
PowerUnit = tk.Label(window, text='dBm', width=3)
PowerUnit.place(x=power_set_x+100, y=power_set_y)
PowerInput.insert(END, '0.0')


def serial_port_verify():
    serial_port = 'COM%s' % port_set.get()
    #print(SerialPort)
    try:
        ser = serial.Serial(serial_port, int(baud_set.get()), timeout=1)
        #port_open.set('Port opened')
        ser.close()
        inst = ik.generic_scpi.SCPIInstrument.open_gpibusb(serial_port, int(addr_set.get()), timeout=3, write_timeout=3)
        port_open.set(inst.name)
    except:
        port_open.set('Port check error')


port_open = StringVar()
port_open.set('Wait for verification')
port_verify_x = 0
port_verify_y = 190
SerialPortVerifyButton = tk.Button(window, text='Serial Port Verify', width=13, height=1, command=serial_port_verify)
SerialPortVerifyButton.place(x=port_verify_x, y=port_verify_y)
SerialPortVerifyResults = tk.Label(window, textvariable=port_open, bg='light gray', width=35, height=2)
SerialPortVerifyResults.place(x=port_verify_x+100, y=port_verify_y)


def func_set():
    waveform1 = func_sel.get()
    #print(waveform1)


func_sel = tk.StringVar()
func_sel.set('SIN')
func_sel_x = 180
func_sel_y = 60
FuncLabel = tk.Label(window, bg='light grey', width=15, text='Waveform Select:')
FuncLabel.place(x=func_sel_x, y=func_sel_y)
FuncSel1 = tk.Radiobutton(window, text='Sinusoid', variable=func_sel, value='SIN', command=func_set)
FuncSel1.place(x=func_sel_x, y=func_sel_y+20)
FuncSel2 = tk.Radiobutton(window, text='Square', variable=func_sel, value='SQU', command=func_set)
FuncSel2.place(x=func_sel_x, y=func_sel_y+40)
FuncSel3 = tk.Radiobutton(window, text='Triangle', variable=func_sel, value='TRI', command=func_set)
FuncSel3.place(x=func_sel_x, y=func_sel_y+60)
FuncSel4 = tk.Radiobutton(window, text='Ramp', variable=func_sel, value='RAMP', command=func_set)
FuncSel4.place(x=func_sel_x, y=func_sel_y+80)


def devise_set():
    serial_port = 'COM%s' % port_set.get()
    freq_sel = float(freq_set.get())
    freq_sel *= 1.0E+6
    power_sel = float(power_set.get())
    if func_sel.get() == 'TRI' or func_sel.get() == 'RAMP':
        if freq_sel > 1.0E5:
            messagebox.showerror('Error', 'The frequency at this waveform cannot be than 100 KHz!!!')
    elif freq_sel < 0 or freq_sel > 1.5E+7:
        messagebox.showerror('Error', 'Frequency out of range!!!')
    else:
        if power_sel > 20:
            messagebox.showwarning('Warning', 'The power seems high!')
        try:
            inst = ik.generic_scpi.SCPIInstrument.open_gpibusb(serial_port, int(addr_set.get()), timeout=3, write_timeout=3)
            inst.sendcmd('APPL:%s %f, %f, 0' % (func_sel.get(), freq_sel, power_sel))
            outresult.set('Frequency was set to %s MHz\nWaveform is %s' % (freq_set.get(), func_sel.get()))
        except:
            outresult.set('Error')


def devise_set5():
    serial_port = 'COM%s' % port_set.get()
    power_sel = float(power_set.get())
    if func_sel.get() == 'TRI' or func_sel.get() == 'RAMP':
        messagebox.showerror('Error', 'The frequency at this waveform cannot be than 100 KHz!!!')
    else:
        if power_sel > 20:
            messagebox.showwarning('Warning', 'The power seems high!')
        try:
            inst = ik.generic_scpi.SCPIInstrument.open_gpibusb(serial_port, int(addr_set.get()), timeout=3, write_timeout=3)
            inst.sendcmd('APPL:%s 5.0E+6, %f, 0' % (func_sel.get(), power_sel))
            outresult.set('Frequency was set to 5 MHz\nWaveform is %s' % func_sel.get())
        except:
            outresult.set('Error')


def devise_set10():
    serial_port = 'COM%s' % port_set.get()
    power_sel = float(power_set.get())
    if func_sel.get() == 'TRI' or func_sel.get() == 'RAMP':
        messagebox.showerror('Error', 'The frequency at this waveform cannot be than 100 KHz!!!')
    else:
        if power_sel > 20:
            messagebox.showwarning('Warning', 'The power seems high!')
        try:
            inst = ik.generic_scpi.SCPIInstrument.open_gpibusb(serial_port, int(addr_set.get()), timeout=3, write_timeout=3)
            inst.sendcmd('APPL:%s 1.0E+7, %f, 0' % (func_sel.get(), power_sel))
            outresult.set('Frequency was set to 10 MHz\nWaveform is %s' % func_sel.get())
        except:
            outresult.set('Error')


def devise_set13():
    serial_port = 'COM%s' % port_set.get()
    power_sel = float(power_set.get())
    if func_sel.get() == 'TRI' or func_sel.get() == 'RAMP':
        messagebox.showerror('Error', 'The frequency at this waveform cannot be than 100 KHz!!!')
    else:
        if power_sel > 20:
            messagebox.showwarning('Warning', 'The power seems high!')
        try:
            inst = ik.generic_scpi.SCPIInstrument.open_gpibusb(serial_port, int(addr_set.get()), timeout=3, write_timeout=3)
            inst.sendcmd('APPL:%s 1.28E+7, %f, 0' % (func_sel.get(), power_sel))
            outresult.set('Frequency was set to 12.8 MHz\nWaveform is %s' % func_sel.get())
        except:
            outresult.set('Error')


set_button_x = 10
set_button_y = 250
SetButton1 = tk.Button(window, text='Set', width=7, height=2, command=devise_set)
SetButton1.place(x=set_button_x, y=set_button_y)
SetButton5 = tk.Button(window, text='5MHz', width=7, height=2, command=devise_set5)
SetButton5.place(x=set_button_x+90, y=set_button_y)
SetButton10 = tk.Button(window, text='10MHz', width=7, height=2, command=devise_set10)
SetButton10.place(x=set_button_x+180, y=set_button_y)
SetButton13 = tk.Button(window, text='12.8MHz', width=7, height=2, command=devise_set13)
SetButton13.place(x=set_button_x+270, y=set_button_y)

outresult = StringVar()
set_result_x = 60
set_result_y = 300
SetResult = tk.Label(window, textvariable=outresult, bg='light grey', width=30, height=2)
SetResult.place(x=set_result_x, y=set_result_y)

window.mainloop()