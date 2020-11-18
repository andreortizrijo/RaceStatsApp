from Commands.carinfo import Car
import ac
import acsys
import sys

#---VAR INITIALIZATION---#
getcar = Car()
lapCount = 0
#----Arrays--#
a_speedMS = []
a_speedMPH = []
a_speedKMH = []
a_rpm = []
a_gear = []

#---Main Code---#
def acMain(ac_version):
    #---UI---#
    appWindow = ac.newApp("Race Stats")
    
    return "Race Stats"

#---Updated Values---#
def acUpdate(deltaT):
    global lapCount, a_speedMS, a_speedMPH, a_speedKMH, a_rpm, a_gear

    laps = ac.getCarState(0, acsys.CS.LapCount)

    a_speedMS.append(getcar.speedMS())
    a_speedMPH.append(getcar.speedMPH())
    a_speedKMH.append(getcar.speedKMH())
    a_rpm.append(getcar.rmp())
    a_gear.append(getcar.gear())

    #---Get info when cross the lap---#
    if laps > lapCount:
        lapCount = laps

        ac.log("Speed MS: {}".format(a_speedMS))
        ac.log("Speed MPH: {}".format(a_speedMPH))
        ac.log("Speed MKH: {}".format(a_speedKMH))
        ac.log("Speed RPM: {}".format(a_rpm))
        ac.log("Speed Gear: {}".format(a_gear))