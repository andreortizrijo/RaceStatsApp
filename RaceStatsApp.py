from Info.car_info import Car
from Info.track_info import Track
from Info.player_info import Player
import ac, acsys, os, sys
import platform, socket, pickle, time

if platform.architecture()[0] == "64bit":
    libdir = 'third_party/lib64'
else:
    libdir = 'third_party/lib'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), libdir))
os.environ['PATH'] = os.environ['PATH'] + ";."

from third_party.sim_info import info

#---VAR INITIALIZATION---#
HEADER = 30
SERVER = '192.168.1.18'
PORT = 8081
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

ID = 0
CAR = Car()
TRACK = Track()
PLAYER = Player()

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

#---HANDLERS---#
def send(msg):
    message = pickle.dumps(msg)

    enconded_message = message
    message_length = len(message)
    message = str(message_length).encode(FORMAT)
    message += b' ' *(HEADER - len(message)) + enconded_message

    client.send(message)

#---UI---#
def acMain(ac_version):
    appWindow = ac.newApp("Race Stats")
    ac.setSize(appWindow, 300, 350)

    return "Race Stats"

#---Updated Values Every Second---#
def acUpdate(deltaT):
    global laps, lapcount, lp, totalTime

    # Get session state
    status = info.graphics.status

    laps = ac.getCarState(ID, acsys.CS.LapCount)
    lp = info.graphics.currentTime

    tyretemperature = info.physics.tyreCoreTemperature
    wheeltemperaturefl.append(tyretemperature[0])

    tyrepressure = info.physics.wheelsPressure
    wheelpressurefl.append(tyrepressure[0])

    TRACK.getName(ID)

    totalTime = abs(info.graphics.sessionTimeLeft)
    totalTime_seconds = (totalTime / 1000) % 60
    totalTime_minutes = (totalTime // 1000) // 60

    # Send data to server socket
    data = {
        "TRACK_INFO":{
            "TRACK_NAME":str(TRACK.getName(ID))
        },
        "CAR_INFO":{
            "CURRENT_SPEEDKMH":str(CAR.get(ID, 'speedkmh')),
            "CURRENT_RPM":str(CAR.get(ID, 'rpm')),
            "CURRENT_GEAR":str(CAR.get(ID, 'gear') - 1),
            "GAS_PEDAL":str(CAR.get(ID, 'gas')),
            "BRAKE_PEDAL":str(CAR.get(ID, 'brake')),
            "CLUTCH_PEDAL":str(CAR.get(ID, 'clutch')),
            "STEER_ANGLE":str(CAR.get(ID, 'steerangle'))
        },
        "TIME_INFO":{
            "CURRENT_TIME":str("{:.0f}:{:06.3f}".format(totalTime_minutes, totalTime_seconds))
        }
    }

    send(data)

    # Get info when cross the lap
    if laps > lapcount:
        lapcount = laps

        if status != 1:
            ac.log(str("{:.0f}:{:06.3f}".format(totalTime_minutes, totalTime_seconds)))

        ac.log(str(info.graphics.lastTime))
        ac.log(str(info.graphics.bestTime))

#---When Close Game---#
def acShutdown():
    send(DISCONNECT_MESSAGE)