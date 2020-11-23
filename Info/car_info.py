import ac
import acsys

car_properties_API = {
            "speedms" : acsys.CS.SpeedMS,
            "speedmph" : acsys.CS.SpeedMPH,
            "speedkmh" : acsys.CS.SpeedKMH,
            "rpm" : acsys.CS.RPM,
            "gear" : acsys.CS.Gear
        }

class Car():

    def get(self, id, type):
        return int(ac.getCarState(id, car_properties_API[type]))