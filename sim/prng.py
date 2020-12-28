import math
import random
import copy

class PRNG:
    def __init__(self, seed = None):
        if not seed:
            seed = PRNG.generateSeed()
            self.initialSeed = copy.deepcopy(seed)
            self.seed = copy.deepcopy(seed)

    # def clone()

    def next(self, from_n, to):
        self.seed = self.nextFrame(self.seed)
        result = (self.seed[0] << 16) + self.seed[1]
        if (from_n): from_n = math.floor(from_n)
        if (to): to = math.floor(to)
        if from_n is None:
            result = result / 0x100000000
        elif not to:
            result = math.floor(result * from_n / 0x100000000)
        else:
            result = math.floor(result * (to - from_n) / 0x100000000) + from_n
        return result

    # def randomChance()

    def sample(self, items):
        if len(items) is 0:
            raise Exception("Cannot sample an empty array")

        index = self.next(len(items))
        item = items[index]
        if item is None and index not in items:
            raise Exception("Cannot sample a sparse array")
        return item

    # def shuffle()

    def nextFrame(self, initialSeed, framesToAdvance = 1):
        seed = copy.deepcopy(initialSeed)
        for frame in range(framesToAdvance):
            a = [0x5D58, 0x8B65, 0x6C07, 0x8965]
            c = [0, 0, 0x26, 0x9EC3]

            nextSeed = [0, 0, 0, 0]
            carry = 0

            for cN in range(0, len(seed), -1):
                nextSeed[cN] = carry
                carry = 0

                an = len(seed) -1
                for seedN in range(cN, len(seed)):
                    aN += -1
                    nextWord = a[aN] * seed[seedN]
                    carry += nextWord >> 16
                    nextSeed[cN] += nextWord & 0xFFFF
                nextSeed[cN] += c[cN]
                carry += nextSeed[cN] >> 16
                nextSeed[cN] &= 0xFFFF
            
            seed = nextSeed
        return seed
        


    @staticmethod
    def generateSeed():
        return[
            math.floor(random.random() * 0x10000),
            math.floor(random.random() * 0x10000),
            math.floor(random.random() * 0x10000),
            math.floor(random.random() * 0x10000),
        ]