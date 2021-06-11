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

#---VAR INITIALIZATION---#
ID = 0
HEADER = 4096
SERVER = '127.0.0.1'
PORT = 8081
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
CONFIG_OBJECT = ConfigParser()
FIRST_RUN = False
BUFFER = []

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

def sendData(data):
    if data == DISCONNECT_MESSAGE:
        message = encodeData(data)
        client.send(message)
        BUFFER.clear()

    BUFFER.append(data)

    if len(BUFFER) == 60: # 60fps == 1second
        message = encodeData(BUFFER)
        client.send(message)
        BUFFER.clear()

#---UI---#
def acMain(ac_version):
    appWindow = ac.newApp("Race Stats")
    ac.setSize(appWindow, 300, 350)

    return "Race Stats"

#---Updated Values Every Second---#
def acUpdate(deltaT):
    global BUFFER, FIRST_RUN

    current_state = info.graphics.status

    total_time = abs(info.graphics.sessionTimeLeft)
    total_time_seconds = (total_time / 1000) % 60
    total_time_minutes = (total_time // 1000) // 60

    current_time = "{:.0f}:{:06.3f}".format(total_time_minutes, total_time_seconds)

    data = {
            "METADATA":{
                "TOKEN": CONFIG_OBJECT['AUTH']['token']
            },
            "SESSION_INFO":{
                "SESSION_TRACK":str(info.static.track),
                "SESSION_TRACK_CONFIGURATION":str(info.static.trackConfiguration)
            }
        }

    sendData(data)

#    if FIRST_RUN:
        #data = {
            #"METADATA":{
                #"TOKEN": CONFIG_OBJECT['AUTH']['token']
            #},
            #"SESSION_INFO":{
                #"SESSION_TRACK":str(info.static.track),
                #"SESSION_TRACK_CONFIGURATION":str(info.static.trackConfiguration)
            #}
        #}

        #sendData(data)
        #FIRST_RUN = False

    #if current_state == 2 and current_time != "nan:000nan":
    #    data = {
    #        "TRACK_INFO":{
    #            "TRACK_SECTOR_COUNT":str(info.static.sectorCount),
    #            "TRACK_AIR_DENSITY":str(info.physics.airDensity),
    #            "TRACK_AIR_TEMPERATURE":str(info.physics.airTemp),
    #            "TRACK_ROAD_TEMPERATURE":str(info.physics.roadTemp),
    #            "TRACK_WIND_SPEED":str(info.graphics.windSpeed),
    #            "TRACK_WIND_DIRECTION":str(info.graphics.windDirection),
    #        },
    #        "CAR_INFO":{
    #            "CAR_CURRENT_SPEEDKMH":str(info.physics.speedKmh),
    #            "CAR_CURRENT_RPM":str(info.physics.rpms),
    #            "CAR_CURRENT_GEAR":str(info.physics.gear - 1),
    #            "CAR_GAS_PEDAL":str(info.physics.gas),
    #            "CAR_BRAKE_PEDAL":str(info.physics.brake),
    #            "CAR_CLUTCH_PEDAL":str(info.physics.clutch),
    #            "CAR_STEER_ANGLE":str(info.physics.steerAngle),
    #            "CAR_CURRENT_FUEL":str(info.physics.fuel),
    #            "CAR_MAX_FUEL":str(info.static.maxFuel),
    #            "CAR_AID_FUEL_RATE":str(info.static.aidFuelRate),
    #        },
    #        "TIME_INFO":{
    #            "CURRENT_TIME":str(current_time),
    #        }
    #    }
    #
    #    sendData(data)

#---When Close Game---#
def acShutdown():
    sendData(DISCONNECT_MESSAGE)