import r_control as rc
import d_send as dn
import dm
from tkinter import *
from tkinter import ttk

# Vars
DEVICE_ID = "a84041e081893e7f"
on = "Green"
off = "Red"
indicator_h = 50
indicator_w = 150

# Get initial status of service
service_running = rc.send(rc.status)
pump_running = False
emergency = False

def switch_service():
    global service_running
    if service_running:
        controller_name.set("Start Controller")
        print("Service stopped")
        s.configure('Controller.TFrame', background='red', borderwidth=5, relief='raised')
        service_running = False # The service will be stopped
    else:
        controller_name.set("Stop Controller")
        print("Service started")
        s.configure('Controller.TFrame', background='green', borderwidth=5, relief='raised')
        service_running = True	# The service will be started


def switch_pump():
    global pump_running
    if pump_running:
        pump_name.set("Start Pump")
        print("Pump stopped")
        s.configure('Pump.TFrame', background='red', borderwidth=5, relief='raised')
        pump_running = False
    else:
        pump_name.set("Stop Pump")
        print("Pump Started")
        s.configure('Pump.TFrame', background='green', borderwidth=5, relief='raised')
        pump_running = True
    # dn.switch(DEVICE_ID, dm.r2Off)
 

""" 	
        If we have an emergency we want to run the following, but am unsure how to go about that at this stage.
        Have left it here for later.
"""

def emergency():
    if emergency: emer.grid(column=2, row=4, padx=10, pady=5, sticky=W)
    else: emer.grid_remove()
 

# Will this change my tab space problem?

# Confirgure main window
root = Tk()
root.title("Pump Controller Interface")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.rowconfigure(0, minsize=790, weight=1)
root.columnconfigure(0, minsize=300, weight=1)

# Indicator labels
ttk.Label(mainframe, text="Controller\nActive").grid(column=1, row=1, sticky=(E, W))
ttk.Label(mainframe, text="Pump\nActive").grid(column=1, row=2, sticky=(E, W))
ttk.Label(mainframe, text="Tank\nFull").grid(column=1, row=3, sticky=(E, W))
ttk.Label(mainframe, text="Emergency").grid(column=1, row=4, sticky=(E, W))

# Style 
s = ttk.Style()
s.configure('Controller.TFrame', background='green', borderwidth=5, relief='raised')
s.configure('Pump.TFrame', background='red', borderwidth=5, relief='raised')
s.configure('Level.TFrame', background='green', borderwidth=5, relief='raised')
s.configure('Emergency.TFrame', background='red', borderwidth=5, relief='raised')

# Indicators
ttk.Frame(mainframe, width=indicator_w, height=indicator_h, style='Controller.TFrame').grid(column=2, row=1, padx=10, pady=5, sticky=W)
ttk.Frame(mainframe, width=indicator_w, height=indicator_h, style='Pump.TFrame').grid(column=2, row=2, padx=10, pady=5, sticky=W)
Frame(mainframe, width=indicator_w, height=indicator_h, bg=on).grid(column=2, row=3, padx=10, pady=5, sticky=W)
emer = ttk.Frame(mainframe, width=indicator_w, height=indicator_h, style='Emergency.TFrame')

# Controller button
controller_name = StringVar()
controller_name.set("Stop Controller" if service_running else "Start Controller")
btn_service = ttk.Button(mainframe, textvariable=controller_name, command=switch_service).grid(column=1, row=5)

# Pump switch button
pump_name = StringVar()
pump_name.set("Stop Pump" if pump_running else "Start Pump")
btn_pump = ttk.Button(mainframe, textvariable=pump_name, command=switch_pump).grid(column=1, row=6)

root.mainloop()
