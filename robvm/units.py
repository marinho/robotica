from decimal import Decimal

ohm = 'ohm'
volt = 'volt'
ampere = 'ampere'      # 1 coulomb per second
coulomb = 'coulomb'     # 6.241506 x 10^18 eletrons
watt = 'watt'
unknown = 'unknown'
second = 'second'
joule = 'joule'
ampere_hour = 'ampere-hour'      # 1 coulomb per second
hour = 'hour'

# Ohm's Law: R = V/I = U/I or just V = IR

cm = 10
mm = 1

class InvalidValue(Exception):
    pass

class Value(Decimal):
    unit = unknown
    exp = '1'
    
    def __new__(cls, value):
        unit = unknown
        exp = '1'

        if isinstance(value, basestring):
            if ' ' in value:
                value, unit = value.split(' ')
            elif 'x' in value:
                value, exp = value.split('x')
        else:
            unit = cls.unit
        
        # Stores the metry unit
        obj = Decimal.__new__(cls, value)
        obj.unit = unit
        obj.exp = exp
        
        return obj

    def __repr__(self):
        return self.as_string()

    def as_string(self):
        exp = self.exp != '1' and 'x'+self.exp or ''
        unit = self.unit != unknown and self.unit or ''

        return ('%s%s %s'%(self, exp, unit)).strip()

    def as_eletrons(self):
        if self.unit != coulomb:
            raise InvalidValue('Invalid unit. Should be coulomb and is '+self.unit)

        val = Value(self * Decimal('6.242'))
        val.exp = '10^18'

        return val

    def __div__(self, value):
        result = super(Value, self).__div__(value)
        unit = self.unit

        if isinstance(value, Value):
            # I = Q / t
            if self.unit == coulomb and value.unit == second:
                unit = ampere
        
            # t = Q / I
            if self.unit == coulomb and value.unit == ampere:
                unit = second
        
            # V = W / Q
            if self.unit == watt and value.unit == coulomb:
                unit = volt
        
            # Q = W / V
            if self.unit == watt and value.unit == volt:
                unit = coulomb
        
            # Useful life (in hours) = Ah / A
            if self.unit == ampere_hour and value.unit == ampere:
                unit = hour
         
            # R = V / I
            if self.unit == volt and value.unit == ampere:
                unit = ohm
        
            # I = V / R
            if self.unit == volt and value.unit == ohm:
                unit = ampere
        
        return Value('%s %s'%(result, unit))

    def __mul__(self, value):
        result = super(Value, self).__mul__(value)
        unit = self.unit

        # Defines the unit
        if isinstance(value, Value):
            # Q = t * I
            if self.unit == second and value.unit == ampere:
                unit = coulomb
        
            # W = Q * V
            if self.unit == coulomb and value.unit == volt:
                unit = watt
        
            # V = R * I
            if self.unit == ohm and value.unit == ampere:
                unit = volt

            # Exponential
            exp1 = self.exp.split('^')
            exp2 = value.exp.split('^')
            exp = str(Decimal(exp1[0])) # + Decimal(exp2[0]))
            if len(exp1) > 1 and len(exp2) > 1:
                exp += '^'+str(Decimal(exp1[1]) + Decimal(exp2[1]))
            elif len(exp1) > 1:
                exp += '^'+Decimal(exp1[1])
            elif len(exp2) > 1:
                exp += '^'+Decimal(exp2[1])
        else:
            exp = self.exp
        
        val = Value('%s %s'%(result, unit))
        val.exp = exp

        return val

