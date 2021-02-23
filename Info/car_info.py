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

class Car():

    #def getCarInfo(self, property):
    #    return ac.getCarState(ID, property) 

    def getCarInfo(self, property):
        return property