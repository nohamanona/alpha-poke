class data:
    def __init__(self, dic = {}):
        self.a = None
        self.b = "b"
        self.c = "c"
        if hasattr(self, 'd'):
            print("abc")
        else:
            print("aaa")

        def print_b(self):
            print("b",self.b)
        data.print_b = print_b

        # exec(dic["print_c"])

    def print_a(self):
        print("a",self.a)

    def print_c(self):
        print("none")

# dd = data()

# a = dd.a or ""
# print(a)
# if (not a):print("true")
# tt = {}
# aa = "b"
# print(dir(dd))
# result = getattr(dd,aa)
# print(result)

dic = {"func1":\
    "print('func1')",
    "func2":\
        "print('func2')",
    "print_c":
"""
def print_c(self):
    print("c", self.c)
    print("in dic func")
data.print_c = print_c
"""}
print("eval")
eval(dic["func1"])


dd2 = data(dic)
dd2.print_b()
dd2.print_c()