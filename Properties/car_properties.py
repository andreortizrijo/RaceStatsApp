import ac
import acsys
import collections

class TraitsDict(collections.MutableMapping, dict):
    def __getitem__(self, key):
        return dict.__getitem__(self,key)

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        dict.__delitem__(self, key)

    def __iter__(self):
        return dict.__iter__(self)

    def __len__(self):
        return dict.__len__(self)

    def __contains__(self, x):
        return dict.__contains__(self, x)

class CarProperties():
    def __init__(self, id = 0, speedkmh = [], rpm = [], gear = [], gas = [], brake = [], clutch = [], steerangle = [], turbo = [], fuel = []):
        self._tyre = TraitsDict({})
        self._id = id
        self._speedkmh = speedkmh
        self._rpm = rpm
        self._gear = gear
        self._gas = gas
        self._brake = brake
        self._clutch = clutch
        self._steerangle = steerangle
        self._turbo = turbo
        self._fuel = fuel

    @property
    def Id(self):
        return self._id

    @property
    def SpeedKMH(self):
        return self._speedkmh

    @SpeedKMH.setter
    def SpeedKMH(self, speed):
        self._speedkmh.append(speed)

    @property
    def RPM(self):
        return self._rpm

    @RPM.setter
    def RPM(self, rpm):
        self._rpm.append(rpm)

    @property
    def Gear(self):
        return self._gear

    @Gear.setter
    def Gear(self, gear):
        self._gear.append(gear)

    @property
    def Gas(self):
        return self._gas
    
    @Gas.setter
    def Gas(self, gas):
        self._gas.append(gas)

    @property
    def Brake(self):
        return self._brake
    
    @Brake.setter
    def Brake(self, brake):
        self._brake.append(brake)
    
    @property
    def Clutch(self):
        return self._clutch
    
    @Clutch.setter
    def Clutch(self, clutch):
        self._clutch.append(clutch)

    @property
    def SteerAngle(self):
        return self._steerangle
    
    @SteerAngle.setter
    def SteerAngle(self, steerangle):
        self._steerangle.append(steerangle)

    @property
    def TurboBoost(self):
        return self._turbo
    
    @TurboBoost.setter
    def TurboBoost(self, turbo):
        self._turbo.append(turbo)

    @property
    def Fuel(self):
        return self._fuel
    
    @Fuel.setter
    def Fuel(self, fuel):
        self._fuel.append(fuel)