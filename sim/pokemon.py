import random
import copy
from sim import dex_data

toID = dex_data.Tools.getId

class Pokemon:
    def __init__(self, setpoke, side):

        print("> Pokemon Class __init__")
        self.side = side
        self.battle = side.battle

        print("setpoke",setpoke["species"])
        self.baseSpecies = self.battle.dex.getSpecies(setpoke["species"])

        self.set = setpoke

        self.species = self.baseSpecies

        self.name = setpoke["name"]

        self.level = setpoke["level"]

        self.gender = setpoke["gender"] if "gender" in setpoke else ("M" if random.random() *2 < 1 else "F")

        self.baseMoveSlots = []
        self.moveSlots = []
        if(not self.set["moves"]):
            raise Exception("Setpoke" +  self.name + "has no moves")

        for moveid in self.set["moves"]:
            print("movdid",moveid)
            move = self.battle.dex.getMove(moveid)
            if move.id == None: continue
            # if "hiddenpower" 未実装
            self.baseMoveSlots.append({
                "move":move.name,
                "id":move.id,
                "pp":move.pp if move.noPPBoosts or move.isZ else move.pp * 8/5,
                "maxpp":move.pp if move.noPPBoosts or move.isZ else move.pp * 8/5,
                "target":move.target,
                "disabled":False,
                "disableSource":"",
                "used":False
            })
        
        self.position = 0
        level = "" if self.level == 100 else ", L" + str(self.level)
        gender = "" if self.gender == "" else ", " + self.gender
        if "shiny" in self.set:
            shiny = ", shiny" if self.set["shiny"] else ""
        else: shiny = ""

        print(self.species, type(level), type(shiny))
        self.details = self.species.name + level + gender + shiny
        print(self.details)
        input()
        print("set",self.set)

        self.status = ""
        self.statusData = {}
        self.volatiles = {}
        self.showCure = False


        if "evs" not in self.set:
            self.set["evs"] = {"hp": 0, "atk":0, "def":0, "spa": 0, "spd":0, "spe":0}
        if "ivs" not in self.set:
            self.set["ivs"] = {"hp": 31, "atk": 31, "def":31, "spa": 31, "spd": 31, "spe": 31}
        
        STATS = {"hp": 31, "atk": 31, "def":31, "spa": 31, "spd": 31, "spe": 31}

        for stat in STATS:
            if not self.set["evs"][stat]: self.set["evs"][stat] = 0
            if not self.set["ivs"][stat] and self.set["ivs"][stat] is not 0: self.set["ivs"][stat]= 31
        

        if self.battle.gen and self.battle.gen <= 2:
            for stat in self.set["ivs"]:
                self.set["ivs"][stat] &= 30
        
        # HP_DATA = self.battle.dex.getHiddenPower(self.set["ivs"])

        self.baseStoredStats = None
        self.storedStats = {"atk": 0, "def": 0, "spa": 0, "spd": 0, "spe": 0}
        self.boosts = {"atk": 0, "def": 0, "spa": 0, "spd": 0, "spe": 0, "accuracy": 0, "evasion":0}

        self.baseAbility = toID(self.set["ability"])
        self.ability = self.baseAbility
        self.abilityData = {"id": self.ability}

        self.item = toID(self.set["item"])
        self.itemData = {"id": self.item}
        self.lastItem = " "
        self.usedItemThisTurn = False
        self.ateBerry = False
        self.trapped  = False
        self.maybeTrapped = False
        self.maybeDisabled = False

        self.illusion = None
        self.transformed = False

        self.fainted = False
        self.faintQueued = False
        self.subFainted = None

        self.types = self.baseSpecies.types
        self.addType=""
        self.knownType = True
        self.apparentType = '/'.join(self.baseSpecies.types)

        self.switchFlag = False
        self.forceSwitchFlag = False
        self.switchCopyFlag = False
        self.draggedIn = None
        self.newlySwitched = False
        self.beingCalledBack = False

        self.lastMove = None
        self.moveThisTurn = ''
        self.statsRaisedThisTurn = False
        self.statsLoweredThisTurn = False
        self.hurtThisTurn = False
        self.lastDamage = 0
        self.attackedBy = []    

        self.isActive = False
        self.activeTurns = 0
        self.activeMoveActions = 0
        self.previouslySwitchedIn = 0
        self.truantTurn = False
        self.isStarted = False
        self.duringMove = False 

        self.weighthg = 1
        self.speed = 0
        self.abilityOrder = 0   
        # this.canMegaEvo = this.battle.canMegaEvo(this)
        # this.canUltraBurst = this.battle.canUltraBurst(this)
        # // Normally would want to use battle.canDynamax to set this, but it references this property.
        self.canDynamax = (self.battle.gen >= 8)
        self.canGigantamax = self.baseSpecies.canGigantamax or None

		# // This is used in gen 1 only, here to avoid code repetition.
		# // Only declared if gen 1 to avoid declaring an object we aren't going to need.
        if (self.battle.gen == 1): self.modifiedStats = {"atk": 0, "def": 0, "spa": 0, "spd": 0, "spe": 0}

        self.maxhp = 0
        self.baseMaxhp = 0
        self.hp = 0
        # self.clearVolatile()
        self.hp = self.maxhp    

        print("> Pokemon Class __init__ end")

    # def toJSON
    # def moves()
    # def baseMoves()
    # def getSlot
    # toString
    # def __init

    def updateSpeed(self):
        self.speed = self.getActionSpeed()
    
    # def calculateStat
    def getStat(self, statName, unboosted, unmodified):
        """
        statNameのステータスを取得する
        """
        statName = toID(statName)
        if statName is "hp": raise Exception("Please read `maxhp` directly")

        stat = self.storedStats[statName]
        # // Download ignores Wonder Room's effect, but this results in
		# // stat stages being calculated on the opposite defensive stat
        if unmodified and "wonderroom" in self.battle.field.pseudoWeather:
            if statName is "def":
                statName = "spd"
            elif statName is "spd":
                statName = "def"
        
        if not unboosted:
            boosts = self.battle.runEvent("ModifyBoost", self, None, None, )



    def getActionSpeed(self):
        speed = self.getStat("spe", False, False)



    def baseMoves(self):
        return [x.id for x in self.baseMoveSlots]

    # def setSpecies(self,)


    def clearVolatile(self,includeSwitchFlags = True):
        self.boosts = {
			"atk": 0,
			"def": 0,
			"spa": 0,
			"spd": 0,
			"spe": 0,
			"accuracy": 0,
			"evasion": 0
		}

        if (self.battle.gen == 1 and 'mimic' in self.baseMoves() and not self.transformed):
            moveslot = self.baseMoves().index('mimic' )
            mimicPP = self.moveSlots[moveslot].pp if self.moveSlots[moveslot] else 16
            self.moveSlots = copy.deepcopy(self.baseMoveSlots)
            self.moveSlots[moveslot].pp = mimicPP
        else:
            self.moveSlots = copy.deepcopy(self.baseMoveSlots)
		

        self.transformed = False
        self.ability = self.baseAbility
        # self.hpType = self.baseHpType
        # self.hpPower = self.baseHpPower
        for i in self.volatiles:
            if ("linkedStatus" in self.volatiles[i]):
                # self.removeLinkedVolatiles(self.volatiles[i]["linkedStatus"], self.volatiles[i]["linkedPokemon"])
                raise Exception("removeLinkedVolatiles is unimplemented")
	
        if (self.species.name == 'Eternatus-Eternamax' and self.volatiles["dynamax"]):
            self.volatiles = {"dynamax": self.volatiles["dynamax"]}
        else:
            self.volatiles = {}
		
        if (includeSwitchFlags):
            self.switchFlag = False
            self.forceSwitchFlag = False

        self.lastMove = None
        self.moveThisTurn = ''

        self.lastDamage = 0
        self.attackedBy = []
        self.hurtThisTurn = False
        self.newlySwitched = True
        self.beingCalledBack = False

        self.setSpecies(self.baseSpecies)

    # def removeLinkedVolatiles(self, linkedStatus, linkedPokemon):
    #     linkedStatus = str(linkedStatus)
	# 	for linkedPoke in linkedPokemon:
	# 	    volatileData = linkedPoke.volatiles[linkedStatus]
	# 		if not volatileData: continue
	# 		volatileData.linkedPokemon.splice(volatileData.linkedPokemon.index(self), 1)
	# 		if len(volatileData["linkedPokemon"]) == 0
	# 			linkedPoke.removeVolatile(linkedStatus)

    def getStatus(self):
        return self.battle.dex.getEffectByID(self.status)

    def getItem(self):
        return self.battle.dex.getItem(self.item)
    

    def getAbility():
        return self.battle.dex.getAbility(self.ability)

    def hasAbility(self, ability):
        """
        return False or 
        """
        if self.ignoringAbility(): return False
        ownAbility = self.ability
        if type(ability) is list : return ownAbility == toID(ability)
        return any((toID(x) in ownAbility) for x in ability)

    def getVolatile(self, status):
        status = self.battle.dex.getEffect(status)
        if self.volatiles[status.id]:
            return None
        return status

