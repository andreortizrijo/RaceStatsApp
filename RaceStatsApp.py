from Info.car_info import Car
from Info.track_info import Track
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
HEADER = 4096
SERVER = '192.168.1.22'
PORT = 8081
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

ID = 0
CAR = Car()
TRACK = Track()

buffer = []
first_run = True

def encodeData(data): 
    message = pickle.dumps(data)
    message_buffer = message

    message = str(len(message)).encode(FORMAT)
    message += b' ' *(HEADER - len(message)) + message_buffer
    return message

def sendData(data):
    if data == DISCONNECT_MESSAGE:
        message = encodeData(data)
        client.send(message)
        buffer.clear()

    buffer.append(data)

    if len(buffer) == 60: # 60fps == 1second
        message = encodeData(buffer)
        client.send(message)
        buffer.clear()

#---UI---#
def acMain(ac_version):
    appWindow = ac.newApp("Race Stats")
    ac.setSize(appWindow, 300, 350)

    return "Race Stats"

#---Updated Values Every Second---#
def acUpdate(deltaT):
    global buffer, first_run

    # Retrive the Time data from the AC Session and formta it
    totalTime = abs(info.graphics.sessionTimeLeft)
    totalTime_seconds = (totalTime / 1000) % 60
    totalTime_minutes = (totalTime // 1000) // 60

    if first_run:
        data = {
            "SESSION_INFO":{
                "SESSION_TRACK":str(TRACK.getTrackInfo(info.static.track)),
                "SESSION_TRACK_CONFIGURATION":str(TRACK.getTrackInfo(info.static.trackConfiguration))
            }
        }

        sendData(data)
        first_run = False

    # Send data to server socket
    data = {
        "TRACK_INFO":{
            "TRACK_SECTOR_COUNT":str(TRACK.getTrackInfo(info.static.sectorCount)),
            "TRACK_AIR_DENSITY":str(TRACK.getTrackInfo(info.physics.airDensity)),
            "TRACK_AIR_TEMPERATURE":str(TRACK.getTrackInfo(info.physics.airTemp)),
            "TRACK_ROAD_TEMPERATURE":str(TRACK.getTrackInfo(info.physics.roadTemp)),
            "TRACK_WIND_SPEED":str(TRACK.getTrackInfo(info.graphics.windSpeed)),
            "TRACK_WIND_DIRECTION":str(TRACK.getTrackInfo(info.graphics.windDirection)),
        },
        "CAR_INFO":{
            "CAR_CURRENT_SPEEDKMH":str(CAR.getCarInfo(info.physics.speedKmh)),
            "CAR_CURRENT_RPM":str(CAR.getCarInfo(info.physics.rpms)),
            "CAR_CURRENT_GEAR":str(CAR.getCarInfo(info.physics.gear) - 1),
            "CAR_GAS_PEDAL":str(CAR.getCarInfo(info.physics.gas)),
            "CAR_BRAKE_PEDAL":str(CAR.getCarInfo(info.physics.brake)),
            "CAR_CLUTCH_PEDAL":str(CAR.getCarInfo(info.physics.clutch)),
            "CAR_STEER_ANGLE":str(CAR.getCarInfo(info.physics.steerAngle)),
            "CAR_CURRENT_FUEL":str(CAR.getCarInfo(info.physics.fuel)),
            "CAR_MAX_FUEL":str(CAR.getCarInfo(info.static.maxFuel)),
            "CAR_AID_FUEL_RATE":str(CAR.getCarInfo(info.static.aidFuelRate)),
        },
        "TIME_INFO":{
            "CURRENT_TIME":str("{:.0f}:{:06.3f}".format(totalTime_minutes, totalTime_seconds)),
        }
    }

    sendData(data)

#---When Close Game---#
def acShutdown():
    sendData(DISCONNECT_MESSAGE)