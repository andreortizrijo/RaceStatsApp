import ac, acsys

player_properties_API = {
    "bestlaptime" : acsys.CS.BestLap,
    "lastlaptime" : acsys.CS.LastLap
}

class Player():

    def get(self, id, property):
        time = ac.getCarState(id, player_properties_API[property])

        lapminutes = (time // 1000) // 60
        lapseconds = (time / 1000) % 60

        if time == 0:
            result = "–:––.–––"
            result = "–:––.–––"
        else:
            result = "{:.0f}:{:06.3f}".format(lapminutes, lapseconds)

        return result