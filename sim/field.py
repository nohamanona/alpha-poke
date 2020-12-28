

class Field:
    def __init__(self, battle):
        self.battle = battle
        if "field" in dir(self.battle.format):
            fieldScripts = self.battle.format.field
        elif "field" in dir(self.battle.dex.data()["Scripts"]):
            fieldScripts = self.battle.dex.data()["Scripts"].field
        else:
            fieldScripts = None
        if fieldScripts:
            for k, v in field.dic.items():
            setattr(self, k, v)
        self.id = ""

        self.weather = ""
        self.weatherData = {"id": ""}
        self.terrain = ""
        self.terrainData = {"id": ""}
        self.pseudoWeather = {}

    
