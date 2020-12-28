def script():
    print("script in script.py")

class Script:
    def __init__(self, battle):
        # self.a = "a in class script"
        self.battle = battle
        self.script2 = script
        self.dic = {
            # "a" : self.a,
            "script" : self.script,
            "script2" : self.script2
        }

    def script(self):
        print("script in class script")
        print(self.battle.a)