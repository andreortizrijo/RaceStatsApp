import ac
import acsys

def speedMS():
    return int(ac.getCarState(0, acsys.CS.SpeedMS))

def speedMPH():
    return int(ac.getCarState(0, acsys.CS.SpeedMPH))

def speedKMH():
    return int(ac.getCarState(0, acsys.CS.SpeedKMH))

def rmp():
    return int(ac.getCarState(0, acsys.CS.RPM))

def gear():
    return ac.getCarState(0, acsys.CS.Gear)