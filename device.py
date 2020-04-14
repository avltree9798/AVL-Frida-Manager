import frida
class Device(object):
    @staticmethod
    def getDevices():
        return frida.enumerate_devices()

    @classmethod
    def __init__(self, id, name, type, frida_device):
        self.id = id
        self.name = name
        self.type = type
        self.frida_device = frida_device
    
    @classmethod
    def processes(self):
        return self.frida_device.enumerate_processes()

    @classmethod
    def attach(self, process):
        return self.frida_device.attach(process.pid)