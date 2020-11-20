from Commands.carinfo import Car
import ac
import acsys
import sys

#---VAR INITIALIZATION---#
getcar = Car()
laps = 0
lapCount = 0
l_lapcount = 0
l_speed = 0
l_rpm = 0
l_gear = 0
#----Arrays--#
a_speedMS = []
a_speedMPH = []
a_speedKMH = []
a_rpm = []
a_gear = []

#---Main Code---#
def acMain(ac_version):
    global l_lapcount, l_speed, l_rpm, l_gear, laps, lapCount

    #---UI---#
    appWindow = ac.newApp("Race Stats")
    
    ac.setSize(appWindow, 200, 300)

    l_lapcount = ac.addLabel(appWindow, "Lap: 1")
    ac.setPosition(l_lapcount, 3, 30)
    l_speed = ac.addLabel(appWindow, "KMH: 0")
    ac.setPosition(l_speed, 3, 50)
    l_rpm = ac.addLabel(appWindow, "RPM: 0")
    ac.setPosition(l_rpm, 3, 70)
    l_gear = ac.addLabel(appWindow, "GEAR: 0")
    ac.setPosition(l_gear, 3, 90)

    return "Race Stats"

#---Updated Values---#
def acUpdate(deltaT):
    global laps, lapCount, l_lapcount, l_speed, l_rpm, l_gear, a_speedMS, a_speedMPH, a_speedKMH, a_rpm, a_gear

    laps = ac.getCarState(0, acsys.CS.LapCount) + 1

    a_speedMS.append(getcar.speedMS())
    a_speedMPH.append(getcar.speedMPH())
    a_speedKMH.append(getcar.speedKMH())
    a_rpm.append(getcar.rmp())
    a_gear.append(getcar.gear())

    ac.setText(l_speed, "KMH: {}".format(getcar.speedKMH()))
    ac.setText(l_rpm, "RPM: {}".format(getcar.rmp()))
    ac.setText(l_gear, "GEAR: {}".format(getcar.gear()))

    #---Get info when cross the lap---#
    if laps > lapCount:
        lapCount = laps
        ac.setText(l_lapcount, "Laps: {}".format(lapCount))
        ac.log("Speed MS: {}".format(a_speedMS))
        ac.log("Speed MPH: {}".format(a_speedMPH))
        ac.log("Speed MKH: {}".format(a_speedKMH))
        ac.log("Speed RPM: {}".format(a_rpm))
        ac.log("Speed Gear: {}".format(a_gear))