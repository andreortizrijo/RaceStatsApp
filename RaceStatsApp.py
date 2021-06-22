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
WHEEL_SLIP = [0] * 4
TYRE_RADIUS = [0] * 4
TYRE_WEAR = [0] * 4
ACCG = [0] * 3
WHEEL_LOAD = [0] * 4
WHEEL_PRESSURE = [0] * 4
TYRE_DIRTY_LEVEL = [0] * 4
TYRE_INNER_TEMPERATURE = [0] * 4
TYRE_MIDDLE_TEMPERATURE = [0] * 4
TYRE_OUTER_TEMPERATURE = [0] * 4
TYRE_CORE_TEMPERATURE = [0] * 4
CAMBER_RAD = [0] * 4
SUSPENSSION_TRAVEL = [0] * 4
DAMAGE = [0] * 4
BRAKE_TEMPERATURE = [0] * 4

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

    if len(BUFFER) == 10:
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
    global BUFFER, FIRST_RUN, WHEEL_SLIP, TYRE_RADIUS, TYRE_WEAR, ACCG, WHEEL_LOAD, WHEEL_PRESSURE, TYRE_DIRTY_LEVEL, TYRE_INNER_TEMPERATURE, TYRE_MIDDLE_TEMPERATURE, TYRE_OUTER_TEMPERATURE, TYRE_CORE_TEMPERATURE, CAMBER_RAD, SUSPENSSION_TRAVEL, DAMAGE, BRAKE_TEMPERATURE

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
            WHEEL_SLIP = setArray(WHEEL_SLIP, PHYSICS.wheelSlip, 4)
            TYRE_RADIUS = setArray(TYRE_RADIUS, STATIC.tyreRadius, 4)
            TYRE_WEAR = setArray(TYRE_WEAR, PHYSICS.tyreWear, 4)
            ACCG = setArray(ACCG, PHYSICS.accG, 3)
            WHEEL_LOAD = setArray(WHEEL_LOAD, PHYSICS.wheelLoad, 4)
            WHEEL_PRESSURE = setArray(WHEEL_PRESSURE, PHYSICS.wheelsPressure, 4)
            TYRE_DIRTY_LEVEL = setArray(TYRE_DIRTY_LEVEL, PHYSICS.tyreDirtyLevel, 4)
            TYRE_INNER_TEMPERATURE = setArray(TYRE_INNER_TEMPERATURE, PHYSICS.tyreTempI, 4)
            TYRE_MIDDLE_TEMPERATURE = setArray(TYRE_MIDDLE_TEMPERATURE, PHYSICS.tyreTempM, 4)
            TYRE_OUTER_TEMPERATURE = setArray(TYRE_OUTER_TEMPERATURE, PHYSICS.tyreTempO, 4)
            TYRE_CORE_TEMPERATURE = setArray(TYRE_CORE_TEMPERATURE, PHYSICS.tyreCoreTemperature, 4)
            CAMBER_RAD = setArray(CAMBER_RAD, PHYSICS.camberRAD, 4)
            SUSPENSSION_TRAVEL = setArray(SUSPENSSION_TRAVEL, PHYSICS.suspensionTravel, 4)
            DAMAGE = setArray(DAMAGE, PHYSICS.carDamage, 4)
            BRAKE_TEMPERATURE = setArray(BRAKE_TEMPERATURE, PHYSICS.brakeTemp, 4)

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
                    "CAR_FUEL":str(PHYSICS.fuel),
                    "CAR_MAX_FUEL":str(STATIC.maxFuel),
                    "CAR_AID_FUEL_RATE":str(STATIC.aidFuelRate),
                    "CAR_TYRE_RADIUS":str(TYRE_RADIUS),
                    "CAR_TYRE_WEAR":str(TYRE_WEAR),
                    "CAR_AID_TYRE_RATE":str(STATIC.aidTireRate),
                    "CAR_AID_STABILITY":str(STATIC.aidStability),
                    "CAR_AID_AUTO_CLUTCH":str(STATIC.aidAutoClutch),
                    "CAR_AID_AUTO_BLIP":str(STATIC.aidAutoBlip),
                    "CAR_HAS_DRS":str(STATIC.hasDRS),
                    "CAR_HAS_ERS":str(STATIC.hasERS),
                    "CAR_HAS_KERS":str(STATIC.hasKERS),
                    "CAR_ACCG":str(ACCG),
                    "CAR_WHEEL_SLIP":str(WHEEL_SLIP),
                    "CAR_WHEEL_LOAD":str(WHEEL_LOAD),
                    "CAR_WHEEL_PRESSURE":str(WHEEL_PRESSURE),
                    "CAR_TYRE_DIRTY_LEVEL":str(TYRE_DIRTY_LEVEL),
                    "CAR_TYRE_INNER_TEMPERATURE":str(TYRE_INNER_TEMPERATURE),
                    "CAR_TYRE_MIDDLE_TEMPERATURE":str(TYRE_MIDDLE_TEMPERATURE),
                    "CAR_TYRE_OUTER_TEMPERATURE":str(TYRE_OUTER_TEMPERATURE),
                    "CAR_TYRE_CORE_TEMPERATURE":str(TYRE_CORE_TEMPERATURE),
                    "CAR_CAMBER_RAD":str(CAMBER_RAD),
                    "CAR_SUSPENSION_TRAVEL":str(SUSPENSSION_TRAVEL),
                    "CAR_DAMAGE":str(DAMAGE),
                    "CAR_TURBO_BOOST":str(PHYSICS.turboBoost),
                    "CAR_FINAL_FF":str(PHYSICS.finalFF),
                    "CAR_BRAKE_TEMPERATURE":str(BRAKE_TEMPERATURE),
                    "CAR_AI_CONTROLL":str(PHYSICS.isAIControlled),
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