import ac, acsys, os, sys
import platform, socket, pickle

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
SESSION_FIRST = True
IS_RACING = False
BUFFER = []

#---SHARED MEMORY API---#
STATIC = info.static
GRAPHICS = info.graphics
PHYSICS = info.physics

#---ROOT DIRECTORY---#
PATH = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
CONFIG_OBJECT = ConfigParser()
CONFIG_OBJECT.read(os.path.join(PATH, 'config.ini'))

#---SOCKET COMMUNICATION---#
HEADER = 4096
SERVER = '127.0.0.1'
PORT = 8081
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect(ADDR)

def dump_data(data): 
    message = pickle.dumps(data)
    message_buffer = message
    message = str(len(message)).encode(FORMAT)
    message += b' ' *(HEADER - len(message)) + message_buffer
    
    return message

def send_data(data, is_racing):
    if data == DISCONNECT_MESSAGE:
        message = dump_data(data)
        client.send(message)

    BUFFER.append(data)

    if is_racing == True:
        message = dump_data(BUFFER)
        client.send(message)
        BUFFER.clear()

    if len(BUFFER) == 5:
        message = dump_data(BUFFER)
        client.send(message)
        BUFFER.clear()
 
def format_time(time):
    time_seconds = (time / 1000) % 60
    time_minutes = (time // 1000) // 60
    current_time = "{:.0f}:{:06.3f}".format(time_minutes, time_seconds)

    return current_time

def set_array(array, type, length):
    for i in range(length):
        array[i] = type[i]

    return array

#---UI---#
def acMain(ac_version):
    appWindow = ac.newApp('RaceStats')
    ac.setSize(appWindow, 280, 70)
    ac.setBackgroundOpacity(appWindow, 0)

    racing_checkbox = ac.addCheckBox(appWindow, 'TURN ON IF YOU ARE RACING!')
    ac.setPosition(racing_checkbox, 3, 35)
    ac.addOnCheckBoxChanged(racing_checkbox, racing_checkbox_onclick)

    return "Race Stats"

def racing_checkbox_onclick(*args):
    global IS_RACING

    if IS_RACING:
        IS_RACING = False
    else:
        IS_RACING = True

#---RUNNING---#
def acUpdate(deltaT):
    global BUFFER, IS_RACING, SESSION_FIRST
    global STATIC, PHYSICS, GRAPHICS

    session_state = GRAPHICS.status

    time = format_time(abs(GRAPHICS.sessionTimeLeft))
    best_lap = format_time(ac.getCarState(ID, acsys.CS.BestLap))

    if SESSION_FIRST:
        session_data = {
            "METADATA":{
                "TOKEN":CONFIG_OBJECT['AUTH']['token']
            },
            "SESSION_INFO":{
                "SESSION_TRACK":str(STATIC.track),
                "SESSION_TRACK_CONFIGURATION":str(STATIC.trackConfiguration)
            }
        }

        #send_data(session_data, IS_RACING)
        SESSION_FIRST = False

    if IS_RACING:
        track_data = {
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
        }
        #send_data(track_data, IS_RACING)

        car_data = {
            "METADATA":{
                "TOKEN":CONFIG_OBJECT['AUTH']['token']
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
            }
        }
        #send_data(car_data, IS_RACING)

        time_data = {
            "METADATA":{
                "TOKEN":CONFIG_OBJECT['AUTH']['token']
            },
            "TIME_INFO":{
                "TIME_CURRENT_TIME":str(time),
                "TIME_BEST_TIME":str(best_lap)
            }
        }
        #send_data(time_data, IS_RACING)

#def acShutdown():
    #send_data(DISCONNECT_MESSAGE, False)