from Info.car_info import Car
from Properties.car_properties import CarProperties
import ac
import acsys
import sys

#---VAR INITIALIZATION---#
car = Car()
carproperties = CarProperties()
laps = 0
lapcount = 0

#---UI Lable---#
l_lapcount = 0
l_speedms = 0
l_speedmph = 0
l_speedkmh = 0
l_rpm = 0
l_gear = 0

#---Main Code---#
def acMain(ac_version):
    global l_lapcount, l_speedms, l_speedmph, l_speedkmh, l_rpm, l_gear, laps, lapcount

    #---UI---#
    appWindow = ac.newApp("Race Stats")
    ac.setSize(appWindow, 200, 300)

    l_lapcount = ac.addLabel(appWindow, "Lap: 1")
    ac.setPosition(l_lapcount, 3, 30)

    l_speedms = ac.addLabel(appWindow, "MS: 0")
    ac.setPosition(l_speedms, 3, 50)

    l_speedmph = ac.addLabel(appWindow, "MPH: 0")
    ac.setPosition(l_speedmph, 3, 70)

    l_speedkmh = ac.addLabel(appWindow, "KMH: 0")
    ac.setPosition(l_speedkmh, 3, 90)  

    l_rpm = ac.addLabel(appWindow, "RPM: 0")
    ac.setPosition(l_rpm, 3, 110)

    l_gear = ac.addLabel(appWindow, "GEAR: 0")
    ac.setPosition(l_gear, 3, 130)

    return "Race Stats"

#---Updated Values---#
def acUpdate(deltaT):
    global l_lapcount, l_speedms, l_speedmph, l_speedkmh, l_rpm, l_gear, laps, lapcount

    laps = ac.getCarState(0, acsys.CS.LapCount)

    carproperties.SpeedMS = car.get(0, "speedms")
    carproperties.SpeedMPH = car.get(0, "speedmph")
    carproperties.SpeedKMH = car.get(0, "speedkmh")
    carproperties.RPM = car.get(0, "rpm")
    carproperties.GEAR = car.get(0, "gear")

    #---Updating in real time on UI---#
    ac.setText(l_speedms, "MS: {}".format(car.get(0, "speedms")))
    ac.setText(l_speedmph, "MPH: {}".format(car.get(0, "speedmph")))
    ac.setText(l_speedkmh, "KMH: {}".format(car.get(0, "speedkmh")))
    ac.setText(l_rpm, "RPM: {}".format(car.get(0, "rpm")))
    ac.setText(l_gear, "GEAR: {}".format(car.get(0, "gear")))

    #---Updating/Get info when cross the lap---#
    if laps > lapcount:
        lapcount = laps
        ac.setText(l_lapcount, "Laps: {}".format(lapcount))
        
        #---File Log---#
        ac.log("Count Test - {}".format(lapcount))
        ac.log("Speed MS_{}: {}".format(lapcount, carproperties.SpeedMS))
        ac.log("Speed MPH_{}: {}".format(lapcount, carproperties.SpeedMPH))
        ac.log("Speed MKH_{}: {}".format(lapcount, carproperties.SpeedKMH))
        ac.log("Speed RPM_{}: {}".format(lapcount, carproperties.RPM))
        ac.log("Speed Gear_{}: {}".format(lapcount, carproperties.GEAR))