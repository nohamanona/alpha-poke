import dex

class Battle:
    def __init__(self, ver):
        self.a = "a in Battle class"
        self.ver = ver
        self.dex = dex.Dex(self.ver,self)

        for k, v in self.dex.clsScript.dic.items():
            setattr(self, k, v)

if __name__ == "__main__":
    Bat = Battle(1)
    Bat.script()
    Bat.script2()
    print(Bat.a)