from Info.car_info import Car
from Info.track_info import Track
from Info.player_info import Player
from Properties.car_properties import CarProperties
import ac, acsys, os, sys
import platform, socket

if platform.architecture()[0] == "64bit":
    libdir = 'third_party/lib64'
else:
    libdir = 'third_party/lib'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), libdir))
os.environ['PATH'] = os.environ['PATH'] + ";."

from third_party.sim_info import info

#---VAR INITIALIZATION---#
HEADER = 64
PORT = 8080
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = '127.0.0.1'

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(ADDR)

car = Car()
track = Track()
player = Player()
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
    global laps, lapcount, lp, totalTime

    status = info.graphics.status

    laps = ac.getCarState(carproperties.Id, acsys.CS.LapCount)
    lp = info.graphics.currentTime

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

    totalTime = abs(info.graphics.sessionTimeLeft)
    totalTime_seconds = (totalTime / 1000) % 60
    totalTime_minutes = (totalTime // 1000) // 60

    #---Get info when cross the lap---#
    if laps > lapcount:
        lapcount = laps

        if status != 1:
            ac.log(str("{:.0f}:{:06.3f}".format(totalTime_minutes, totalTime_seconds)))

        ac.log(str(info.graphics.lastTime))
        ac.log(str(info.graphics.bestTime))