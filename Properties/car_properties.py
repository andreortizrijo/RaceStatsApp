import ac
import acsys

class CarProperties():

    def __init__(self, speedms = [], speedmph = [], speedkmh = [], rpm = [], gear = []):
        self._speedms = speedms
        self._speedmph = speedmph
        self._speedkmh = speedkmh
        self._rpm = rpm
        self._gear = gear

    @property
    def SpeedMS(self):
        return self._speedms

    @SpeedMS.setter
    def SpeedMS(self, speed):
        self._speedms.append(speed)
        
    @property
    def SpeedMPH(self):
        return self._speedmph

    @SpeedMPH.setter
    def SpeedMPH(self, speed):
        self._speedmph.append(speed)

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
    def GEAR(self):
        return self._gear

    @GEAR.setter
    def GEAR(self, gear):
        self._gear.append(gear)
