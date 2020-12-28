from sim import dex

dex = dex.Dex

# dex.includeFormats()

# FORMAT = dex.getFormat("gen7OU",True)
# dex = dex.forFormat(FORMAT)

class AAA:
    def __init__(self):
        self.a = 0

        if 'a' in dir(AAA):
            print("ok")

aaa = AAA()
print(aaa.a)
