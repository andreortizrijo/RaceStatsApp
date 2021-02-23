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

class Track():

    def getTrackName(self):
        trackname = info.static.track
        if trackname:
            trackname = trackname.replace('ks', '')
            trackname = trackname.replace('_', '')
        else:
            trackname = 'No information about track name.'

        return trackname
    
    def getTrackConfig(self):
        trackconfig = info.static.trackConfiguration
        if trackconfig:
            trackconfig = trackconfig.replace('ks', '')
            trackconfig = trackconfig.replace('_', '')
        else:
            trackconfig = 'No information about track configuration.'

        return trackconfig

    def getTrackInfo(self, property):
        return property
    
    # The highest number = higher lvl of difficulty on curves
    #def getTrackSPlineLength(self):
        #return info.static.trackSPlineLength