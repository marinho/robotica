class Device(object):
    # Abstract
    pass

class Terminal(Device):
    connection = None

    def connect_to(self, terminal):
        self.connection = terminal

class DeviceWithTerminals(Device):
    # Abstract
    terminals = None

class Wire(DeviceWithTerminals):
    def __init__(self):
        self.terminals = {
            0: Terminal(),
            1: Terminal(),
            }

class Resistor(DeviceWithTerminals):
    resistance = None

    def __init__(self, resistance):
        self.terminals = {
            0: Terminal(),
            1: Terminal(),
            }

        self.resistance = resistance

