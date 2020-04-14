from tkinter import *
from device import Device
from time import sleep

devices = []
selected_device = None
lbProcessList = None
processes = []
codeEditor = None

def update_process():
    global selected_device
    global processes
    if selected_device == None:
        print("Please select a device first")
    else:
        lbProcessList.delete(0, END)
        processes = []
        for p in selected_device.processes():
            processes.append(p)
            lbProcessList.insert(END, "%d - %s" %(p.pid, p.name))

def on_listbox_select(evt):
    global selected_device
    w = evt.widget
    index = int(w.curselection()[0])
    selected_device = devices[index]
    update_process()

def my_message_handler(message, payload):
    print(message, payload)

def hook_process(evt):
    global selected_device
    global processes
    global codeEditor
    w = evt.widget
    index = int(w.curselection()[0])
    selected_process = processes[index]
    print("Attaching to pid %d"%selected_process.pid)
    session = selected_device.attach(selected_process)
    code = codeEditor.get("1.0",END)
    sleep(1)
    script = session.create_script(code)
    script.on("message", my_message_handler)
    script.load()

if __name__ == "__main__":
    root = Tk()
    root.geometry("800x550")
    lDeviceList = Label(root, text="Device list", bg='#3E4149', fg='#fff')
    lDeviceList.place(x=0, y=0)
    listbox = Listbox(root, width=40, height=10)
    lProcessList = Label(root, text="Running Process", bg='#3E4149', fg='#fff')
    lProcessList.place(x=0,y=200)
    lbProcessList = Listbox(root, width=40, height=15)
    listbox.place(x=0, y=20)
    lbProcessList.place(x=0, y=220)
    listbox.bind("<<ListboxSelect>>", on_listbox_select)
    lbProcessList.bind("<<ListboxSelect>>", hook_process)
    btnRefresh = Button(root, text="Refresh Process", command=update_process, highlightbackground='#3E4149')
    btnRefresh.place(x=0, y=480)
    lbCodeEditor = Label(root, text="Code Editor", bg='#3E4149', fg='#fff')
    lbCodeEditor.place(x=350, y=0)
    codeEditor = Text(root, width=60, height=35)
    codeEditor.place(x=350, y=20)
    for d in Device.getDevices():
        listbox.insert(END, d.name)
        devices.append(Device(d.id, d.name, d.type, d))
    root.title("AVL Frida Manager")
    root.configure(bg='#3E4149')
    root.mainloop()
