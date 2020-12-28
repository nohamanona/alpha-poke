from importlib import import_module
import script1

class Dex:
    def __init__(self, ver, battle):
        self.a = "a in dex"
        self.ver = ver
        self.battle = battle
        self.mod = "script"+ str(self.ver)

        self.script_module = import_module("mod."+self.mod)
        self.clsScript = self.script_module.Script(self.battle)