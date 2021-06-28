import ac, acsys, os, sys
import platform, socket, pickle, time

if platform.architecture()[0] == "64bit":
    libdir = 'third_party/lib64'
else:
    libdir = 'third_party/lib'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), libdir))
os.environ['PATH'] = os.environ['PATH'] + ";."

from configparser import ConfigParser
from third_party.sim_info import info
from array import array

#---VAR INITIALIZATION---#
ID = 0
HEADER = 4096
SERVER = '127.0.0.1'
PORT = 8081
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
CONFIG_OBJECT = ConfigParser()
FIRST_RUN = True
BUFFER = []
STATIC = info.static
GRAPHICS = info.graphics
PHYSICS = info.physics

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
CONFIG_OBJECT.read(os.path.join(path, 'config.ini'))

def encodeData(data): 
    message = pickle.dumps(data)
    message_buffer = message
    message = str(len(message)).encode(FORMAT)
    message += b' ' *(HEADER - len(message)) + message_buffer
    
    return message

def sendData(data, first_run):
    if data == DISCONNECT_MESSAGE:
        message = encodeData(data)
        client.send(message)
        return

    BUFFER.append(data)

    if first_run == True:
        message = encodeData(BUFFER)
        client.send(message)
        BUFFER.clear()

    if len(BUFFER) == 60:
        message = encodeData(BUFFER)
        client.send(message)
        BUFFER.clear()
 
def formatTime(time):
    time_seconds = (time / 1000) % 60
    time_minutes = (time // 1000) // 60
    current_time = "{:.0f}:{:06.3f}".format(time_minutes, time_seconds)

    return current_time

def setArray(array, type, length):
    for i in range(length):
        array[i] = type[i]

    return array

#---UI---#
def acMain(ac_version):
    return "Race Stats"

def acUpdate(deltaT):
    global BUFFER, FIRST_RUN, STATIC, PHYSICS, GRAPHICS

    current_state = GRAPHICS.status

    time = formatTime(abs(GRAPHICS.sessionTimeLeft))
    best_lap = formatTime(ac.getCarState(ID, acsys.CS.BestLap))

    if FIRST_RUN:
        data = {
            "METADATA":{
                "TOKEN":CONFIG_OBJECT['AUTH']['token']
            },
            "SESSION_INFO":{
                "SESSION_TRACK":str(STATIC.track),
                "SESSION_TRACK_CONFIGURATION":str(STATIC.trackConfiguration)
            }
        }

        sendData(data, FIRST_RUN)
        FIRST_RUN = False

    if current_state == 2:
        if time != "nan:000nan":
            data = {
                "METADATA":{
                    "TOKEN":CONFIG_OBJECT['AUTH']['token']
                },
                "TRACK_INFO":{
                    "TRACK_SPLINE_LENGTH":str(STATIC.trackSPlineLength),
                    "TRACK_SECTOR_COUNT":str(STATIC.sectorCount),
                    "TRACK_AIR_DENSITY":str(PHYSICS.airDensity),
                    "TRACK_AIR_TEMPERATURE":str(PHYSICS.airTemp),
                    "TRACK_ROAD_TEMPERATURE":str(PHYSICS.roadTemp),
                    "TRACK_WIND_SPEED":str(GRAPHICS.windSpeed),
                    "TRACK_WIND_DIRECTION":str(GRAPHICS.windDirection),
                    "TRACK_SURFACE_GRIP":str(GRAPHICS.surfaceGrip),
                },
                "CAR_INFO":{
                    "CAR_MODEL":str(STATIC.carModel),
                    "CAR_SPONSER":str(STATIC.carSkin),
                    "CAR_SPEEDKMH":str(PHYSICS.speedKmh),
                    "CAR_RPM":str(PHYSICS.rpms),
                    "CAR_GEAR":str(PHYSICS.gear - 1),
                    "CAR_GAS_PEDAL":str(PHYSICS.gas),
                    "CAR_BRAKE_PEDAL":str(PHYSICS.brake),
                    "CAR_CLUTCH_PEDAL":str(PHYSICS.clutch),
                    "CAR_STEER_ANGLE":str(PHYSICS.steerAngle),
                    "CAR_TYRE_COMPOUND":str(GRAPHICS.tyreCompound)
                },
                "TIME_INFO":{
                    "TIME_CURRENT_TIME":str(time),
                    "TIME_BEST_TIME":str(best_lap)
                }
            }

            sendData(data, FIRST_RUN)

def acShutdown():
    sendData(DISCONNECT_MESSAGE, False)