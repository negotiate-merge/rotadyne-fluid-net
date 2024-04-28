import r_control as rc
import d_send as dn
import dm
from tkinter import *
from tkinter import ttk
import threading
from functools import partial
import gui_controller as gc


# Vars
DEVICE_ID = "a84041e081893e7f"
indicator_h = 50
indicator_w = 150

# 'global' (not technically) object for application wide status tracking
status = {
    'service_running': False,
    'pump_running': False,
    'tank_full': False,
    'emergency': False,
}

# Get initial status of remote service
rc.send(rc.status, status)

# Get paho.mqqt.Client object, run in it's own thread
mqttc = gc.run(status)
mqttc.loop_start()

# Poll for node uplink - get current node state via mqttc message read
dn.switch(DEVICE_ID, dm.poll_uplink)

print("Gui output:\n", status)

# Update indicators at 3000ms intervals
def update_indicators(status):
    # print("Status from update_indicators:\n", status)
    # Service
    if status['service_running']:
        s.configure('Controller.TFrame', background='green')
        controller_name.set("Stop Controller")
    else:
        s.configure('Controller.TFrame', background='red')
        controller_name.set("Start Controller")

    # Pump
    if status['pump_running']: 
        s.configure('Pump.TFrame', background='green')
        pump_name.set("Stop Pump")
    else: 
        s.configure('Pump.TFrame', background='red')
        pump_name.set("Start Pump")

    # Tank level
    if status['tank_full']: s.configure('Level.TFrame', background='green')
    else: s.configure('Level.TFrame', background='red')
    # Emergency
    if status['emergency']:
        s.configure('Emergency.TFrame', background='red')
    else: 
        s.configure('Emergency.TFrame', background='#f0f0f0')
    mainframe.after(3000, update_indicators, status)


def switch_service(status):
    ''' All rc.send calls will update status['service_running'] '''
    if status['service_running']:
        t = threading.Thread(target=rc.send, args=(rc.stop, status,))
        t.start(); t.join()
    else:
        t = threading.Thread(target=rc.send, args=(rc.start, status,))
        t.start(); t.join()
    dn.switch(DEVICE_ID, dm.poll_uplink)


def switch_pump(status):
    # Switch pump off if running
    if status['pump_running']:
        dn.switch(DEVICE_ID, dm.r2Off)
        pump_name.set("Start Pump")
        print("Pump stopped")
        # status['pump_running'] = False
    # Switch pump on if not running
    else:
        dn.switch(DEVICE_ID, dm.r2On)
        pump_name.set("Stop Pump")
        print("Pump Started")
        # status['pump_running'] = True


# Configure main window
root = Tk()
root.title("Pump Controller Interface")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.rowconfigure(0, minsize=400, weight=1)
root.columnconfigure(0, minsize=300, weight=1)

# Indicator labels
ttk.Label(mainframe, text="Controller\nActive").grid(column=1, row=1, sticky=(E, W))
ttk.Label(mainframe, text="Pump\nActive").grid(column=1, row=2, sticky=(E, W))
ttk.Label(mainframe, text="Tank\nFull").grid(column=1, row=3, sticky=(E, W))
ttk.Label(mainframe, text="Emergency").grid(column=1, row=4, sticky=(E, W))

# Indicator panel styling
s = ttk.Style()
s.configure('Controller.TFrame', background='#f0f0f0', borderwidth=5, relief='raised')
s.configure('Pump.TFrame', background='#f0f0f0', borderwidth=5, relief='raised')
s.configure('Level.TFrame', background='#f0f0f0', borderwidth=5, relief='raised')
s.configure('Emergency.TFrame', background='#f0f0f0', borderwidth=5, relief='raised')

# Indicator Panels
ttk.Frame(mainframe, width=indicator_w, height=indicator_h, style='Controller.TFrame').grid(column=2, row=1, padx=10, pady=5, sticky=E)
ttk.Frame(mainframe, width=indicator_w, height=indicator_h, style='Pump.TFrame').grid(column=2, row=2, padx=10, pady=5, sticky=E)
ttk.Frame(mainframe, width=indicator_w, height=indicator_h, style='Level.TFrame').grid(column=2, row=3, padx=10, pady=5, sticky=E)
ttk.Frame(mainframe, width=indicator_w, height=indicator_h, style='Emergency.TFrame').grid(column=2, row=4, padx=10, pady=5, sticky=E)

# Controller button
controller_name = StringVar()
# controller_name.set("Trigger Controller")
btn_service = ttk.Button(mainframe, textvariable=controller_name, command=partial(switch_service, status)).grid(column=1, row=5)

# Pump switch button
pump_name = StringVar()
# pump_name.set("Stop Pump" if status['pump_running'] else "Start Pump")
# pump_name.set("Pump Switch")
btn_pump = ttk.Button(mainframe, textvariable=pump_name, command=partial(switch_pump, status)).grid(column=1, row=6)

update_indicators(status)
root.mainloop()
