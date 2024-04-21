import r_control as rc
# import d_send as dn
# import dm
import tkinter as tk

DEVICE_ID = "a84041e081893e7f"

def stop_service():
	rc.controller(rc.stop)

def start_service():
	rc.controller(rc.start)

def pump_off():
	dn.switch(DEVICE_ID, dm.r2Off)

def pump_on():
	dn.switch(DEVICE_ID, dm.r2On)


window  = tk.Tk()
window.title("Pump Controller")
window.rowconfigure(0, minsize=790, weight=1)
window.columnconfigure(0, minsize=300, weight=1)

frm_indicators = tk.Frame(window)

# Inner components
lbl_controller_service = tk.Label(master=frm_indicators, text="Controller\nService")
frm_controller_status = tk.Frame(master=frm_indicators, width=25, height=25, bg="Green")
lbl_controller_service.grid(row=0, column=0)
frm_controller_status.grid(row=0, column=1)

lbl_pump_active = tk.Label(master=frm_indicators, text="Pump\nActive")
frm_pump_status = tk.Frame(master=frm_indicators, width=25, height=25, bg="Green")
lbl_pump_active.grid(row=1, column=0)
frm_pump_status.grid(row=1, column=1)

lbl_tank_switch = tk.Label(master=frm_indicators, text="Tank\nSwitch")
frm_tank_status = tk.Frame(master=frm_indicators, width=25, height=25, bg="Green")
lbl_tank_switch.grid(row=2, column=0)
frm_tank_status.grid(row=2, column=1)

lbl_emergency_switch = tk.Label(master=frm_indicators, text="Emergency\nSwitch")
lbl_emergency_status = tk.Frame(master=frm_indicators, width=25, height=25, bg="Green")
lbl_emergency_switch.grid(row=3, column=0)
lbl_emergency_status.grid(row=3, column=1)

frm_indicators.grid(row=0, column=0, sticky="ns")


window.mainloop()
