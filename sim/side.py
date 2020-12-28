from sim import pokemon


class Side:
    def __init__(self, name, battle, sideNum, team):

        print("Side __init__")

        self.battle = battle
        self.id = ['p1','p2'][sideNum]
        self.n = sideNum

        self.name = name

        self.foe = self.battle.sides[0] if sideNum else self.battle.sides[1]

        self.team = team
        self.pokemon = []

        for i in range(len(self.team)):
            self.pokemon.append(pokemon.Pokemon(self.team[i],self))
            
        # for 

        if self.battle.gameType is "doubles":
            self.active = [None, None]
        elif self.battle.gameType is "triples" or self.battle.gameType is "rotation":
            self.active = [None, None, None]
        else:
            self.active = [None]

        self.slotConditions = []

    # def toJSON()

    # def requestState()
    # def getChoice()
    #def toString()
    # def getRequestData()

    def randomActive(self):
        actives = list(filter(lambda x: x and not x.fainted), self.active)
        if not ren(actives): return None
        return self.battle.sample(actives)

    # def addSideCondition
    # def getSideConditionData
    # def removeSideCondition
    # def addSlotCondition

    def getSlotCondition(self,target, status):
        if target in dir(pokemon.Pokemon):
            target = target.position
        status = self.battle.dex.getEffect(status)
        if not self.slotConditions[target][status.id]:
            retrun None
        return status

    def removeSlotCondition(self, status):
        if target in dir(pokemon.Pokemon):
            target = target.position
        status = self.battle.dex.getEffect(status)
        if not self.slotConditions[target][status.id]:
            return False
        self.battle.singleEvent('End', status, self.slotConditions[target][status.id], self.active[target])
        del self.slotConditions[target][status.id]
        return True

        







        