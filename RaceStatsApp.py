from Info.car_info import Car
from Info.track_info import Track
from Properties.car_properties import CarProperties
import ac, acsys
import os, sys
import platform
import threading

if platform.architecture()[0] == "64bit":
    libdir = 'third_party/lib64'
else:
    libdir = 'third_party/lib'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), libdir))
os.environ['PATH'] = os.environ['PATH'] + ";."

from third_party.sim_info import info

#---VAR INITIALIZATION---#
car = Car()
track = Track()
carproperties = CarProperties()
laps = 0
lapcount = 0

tyretemperature = 0
tyrepressure = 0
fuel = 0

wheeltemperaturefl = []
wheeltemperaturefr = []
wheeltemperaturerl = []
wheeltemperaturerr = []

wheelpressurefl = []
wheelpressurefr = []
wheelpressurerl = []
wheelpressurerr = []

def crossLap():
    carproperties._tyre["WheelTemperatureFL"] = wheeltemperaturefl
    carproperties._tyre["WheelTemperatureFR"] = wheeltemperaturefr
    carproperties._tyre["WheelTemperatureRL"] = wheeltemperaturerl
    carproperties._tyre["WheelTemperatureRR"] = wheeltemperaturerr

    carproperties._tyre["WheelPressureFL"] = wheelpressurefl
    carproperties._tyre["WheelPressureFR"] = wheelpressurefr
    carproperties._tyre["WheelPressureRL"] = wheelpressurerl
    carproperties._tyre["WheelPressureRR"] = wheelpressurerr

#---Main Code---#
def acMain(ac_version):
    appWindow = ac.newApp("Race Stats")
    ac.setSize(appWindow, 300, 350)

    return "Race Stats"

#---Updated Values---#
def acUpdate(deltaT):
    global laps, lapcount

    laps = ac.getCarState(carproperties.Id, acsys.CS.LapCount)

    tyretemperature = info.physics.tyreCoreTemperature
    tyrepressure = info.physics.wheelsPressure

    #---Update Array Values every second---#
    carproperties.SpeedKMH = car.get(carproperties.Id, "speedkmh")
    carproperties.RPM = car.get(carproperties.Id, "rpm")
    carproperties.Gear = car.get(carproperties.Id, "gear") - 1

    carproperties.Gas = car.get(carproperties.Id, "gas")
    carproperties.Brake = car.get(carproperties.Id, "brake")
    carproperties.Clutch = car.get(carproperties.Id, "clutch")

    carproperties.SteerAngle = car.get(carproperties.Id, "steerangle")
    carproperties.TurboBoost = car.get(carproperties.Id, "turbo")
    carproperties.Fuel = info.physics.fuel

    wheeltemperaturefl.append(tyretemperature[0])
    wheeltemperaturefr.append(tyretemperature[1])
    wheeltemperaturerl.append(tyretemperature[2])
    wheeltemperaturerr.append(tyretemperature[3])

    wheelpressurefl.append(tyrepressure[0])
    wheelpressurefr.append(tyrepressure[1])
    wheelpressurerl.append(tyrepressure[2])
    wheelpressurerr.append(tyrepressure[3])

    track.getName(carproperties.Id)

    #---Get info when cross the lap---#
    if laps > lapcount:
        lapcount = laps
        
        # t1 = threading.Thread(target=crossLap)
        # t1.start()