import ac
import acsys

class Car():

    @staticmethod
    def speedMS():
        return int(ac.getCarState(0, acsys.CS.SpeedMS))

    @staticmethod
    def speedMPH():
        return int(ac.getCarState(0, acsys.CS.SpeedMPH))

    @staticmethod
    def speedKMH():
        return int(ac.getCarState(0, acsys.CS.SpeedKMH))

    @staticmethod
    def rmp():
        return int(ac.getCarState(0, acsys.CS.RPM))

    @staticmethod
    def gear():
        return ac.getCarState(0, acsys.CS.Gear)