import ac, acsys

car_properties_API = {
            "speedkmh" : acsys.CS.SpeedKMH,
            "rpm" : acsys.CS.RPM,
            "gear" : acsys.CS.Gear,
            "gas" : acsys.CS.Gas,
            "brake" : acsys.CS.Brake,
            "clutch" : acsys.CS.Clutch,
            "steerangle" : acsys.CS.Steer,
            "turbo" : acsys.CS.TurboBoost,
        }

class Car():

    def get(self, id, property):
        return ac.getCarState(id, car_properties_API[property])