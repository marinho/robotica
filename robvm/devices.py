# -*- coding: utf-8 -*-
from chemicals import Si, C, Cu, WrongChemical

class BaseElement(object):
    _made_from = None # Accepts just someones
    _can_made_from = []

    def __init__(self, **kwargs):
        # Sets attributes set from named args
        for k,v in kwargs.items():
            setattr(self, k, v)

    def get_made_from(self):
        return self._made_from

    def set_made_from(self, chemical):
        if chemical not in self._can_made_from:
            raise WrongChemical()

        self._made_from = chemical

    made_from = property(get_made_from, set_made_from)

class Wire(BaseElement):
    cable = None

    def connect_to(self, wire, cable=None):
        # Sets the cable
        cable = cable or self.cable
        self.cable = cable or Cable()

        # Sets the other side of cable
        wire.cable = self.cable

SIGNAL_POSITIVE = '+'
SIGNAL_NEGATIVE = '-'

class In(Wire):
    pass

class Out(Wire):
    pass

class Cable(Wire):
    _can_made_from = (Cu,)
    weight = None
    langth = None

class Board(BaseElement):
    _can_made_from = (C,)
    devices = None

    def __init__(self, *args, **kwargs):
        super(Board, self).__init__(*args, **kwargs)

        if not self.devices:
            self.devices = {}

    def append_device(self, device, name):
        self.devices[name] = device

    def __getitem__(self, name):
        return self.devices[name]

    def __setitem__(self, name, device):
        self.append_device(device, name)

# Devices

class Device(BaseElement):
    """http://en.wikipedia.org/wiki/Electronic_device"""
    pass

RESISTOR_TYPE_FIXED = 'f'       # potenciometros
RESISTOR_TYPE_VOLATILE = 'v'    # reostatos

class Resistor(Device):
    """Transforms eletric power to thermal power (joule effect). Can be made
    from carbon or silicon. They can be fixed or volatiles.

    It has 2 wires.
    
    http://en.wikipedia.org/wiki/Resistor"""

    _can_made_from = (Si, C,)
    type = RESISTOR_TYPE_FIXED # Can be RESISTOR_TYPE_VOLATILE, also

    # Eletrical characteristics
    resistance = None
    tolerance = None
    temperature_coefficient = None
    noise = None
    inductance = None
    critical_resistance = None

    wire_1 = Wire()
    wire_2 = Wire()

    def flow(self, voltage, wire=-1):
        """Just returns the result of A = V / R"""
        return voltage / self.resistance

class Transistor(Device):
    """http://en.wikipedia.org/wiki/Transistor"""

    wire_1 = Wire()
    wire_2 = Wire()
    wire_3 = Wire()

class Capacitor(Device):
    """http://en.wikipedia.org/wiki/Capacitor"""

    wire_1 = Wire()
    wire_2 = Wire()

class Diode(Transistor):
    """http://en.wikipedia.org/wiki/Diode"""
    pass

class Led(Diode):
    """http://en.wikipedia.org/wiki/Led"""
    pass

class IC(Device):
    """This is a integrated circuit - or just a chip - and it just works
    as a Python code that responds to externa requests, not trying to be
    itself an electronic device like the board does.

    Just inherit this class and write the code of what it have to do.

    - http://en.wikipedia.org/wiki/Integrated_circuit
    - http://pt.wikipedia.org/wiki/Circuito_integrado
    """
    
    wires = None
    wires_count = 0

    def __init__(self, *args, **kwargs):
        super(IC, self).__init__(*args, **kwargs)

        # Make the wires
        if not self.wires:
            self.wires = [Wire() for n in range(self.wires_count)]

class Battery(Device):
    voltage = None

