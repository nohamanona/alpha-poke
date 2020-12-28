from sim import dex as _dex
from sim import side
from sim import prng
from sim import battle_queue
from sim import field
from sim import pokemon

def _optionalChain(ops):
    lastAccessLHS = None
    value = ops[0]
    i = 1
    while(i < len(ops)):
        op = ops[i]
        fn = ops[i+1]
        i += 2
        if (op is "optionalAccess" or op is "optionalCall") and value is None:
            return None
        if op is "access" or op is "optionalAccess":
            lastAccessLHS = value
            value = fn(value)
        elif op is "call" or op is "optionalCall":
            raise Exception("_optionalChain call is Unimplemented")
        return value

def _opt_11(_11):
    return _11.fainted


class Battle:
    def __init__(self, options):
        self.log = []

        format = options["format"] if "format" in options else _dex.Dex.getFormat(self, options["formatid"], True)
        print("Battle format")
        input()
        self.format = format
        self.dex = _dex.Dex.forFormat(self,format)
        print("Battle dex format")
        self.gen = self.dex.gen
        # self.ruleTable = self.dex.getRuleTable(format)

        self.deserialized = False
        self.gameType = format.gameType or "singles"
        self.field = field.Field(self)

        self.sides = [None, None]
        self.prng = optins["prng"] if "prng" in options else prng.PRNG(optins["seed"] if "seed" in options else None)

        self.queue = battle_queue.BattleQueue(self)


        self.log_flag = True

        self.requestState = ""
        self.turn = 0
        self.midTurn = False
        self.started = False
        self.ended = False

    # def toString()

    # def random

    # def randomChance

    def sample(self, items):
        return self.prng.sample(items)

    # def resetRNG
    # def suppressingAttackEvents
    # def setActiveMove
    # def clearActiveMove
    # def updateSpeed
    # def comparePriority
    # def compareRedirectOrder
    # def compareLeftToRightOrder
    # def speedSort
    # def eachEvent
    # def residualEvent
    # def singleEvent
    def runEvent(self, eventid, target, source, sourceEffect, relayVar, onEffect, fastExit):
        if self.eventDepth >= 8:
            raise Exception("rnEvent eventDepth >=8 Stack overflow")
        if not target:
            target = self
        effectSource = None
        if source in dir(pokemon.Pokemon):
            effectSource = source
        handlers = self.findEventHandlers(target, eventid, effectSource)

    # def priorityEvent
    def resolvePriority(self, handler, callbackName):
        handler["order"] = handler["effect"][callbackName + Order] or False
        handler["priority"] = handler["effect"][callbackName + "Priority"] or 0
        handler["subOrder"] = handler["effect"][callbackName + "SubOrder"] or 0
        if handler["effectHolder"] and handler["effectHolder"].getStat:
            handler["speed"] = handler["effctHolder"].speed
        return handler

    def findEventHandlers(self, target, eventName, source):
        handlers = {}
        if type(target) is list:
            for i, pokemon in enumerate(target):
                curHandlers = self.findEventHandlers(pokemon, eventName, source)
                for handler in curHandlers:
                    handler["target"] = pokemon
                    handler["index"] = i
                handlers = handlers.update(curHandlers)
            return handlers
        
        if target in dir(pokemon.Pokemon) and target.isActive:
            handlers = self.findPokemonEventHandlers(target, "on"+ eventName)

    def findPokemonEventHandlers(self, pokemon, callbackName, getKey):
        handlers = {}
        status = pokemon.getStatus()
        callback = getattr(status, callbackName)
        if callback is not None or (getKey and pokemon.statusData[getKey] if getKey in pokemon.statusData):
            handlers.update(self.resolvePriority({
                "effect": status, "callback":callback, "state": pokemon.statusData, "end": pokemon.clearStatus, "effectHolder": pokemon
            }, callbackName))
        
        for id in pokemon.volotiles:
            volotileState = pokemon.volatiles[id]
            volatile = pokemon.getVolatile[id]
            callback = volatile[callbackName]
            if not callback or (getKey and volotileState[getkey] if getkey in volotileState):
                handlers.update(
                    self.resolvePriority({
                        "effect": volatile, "callback": callback, "state":volotileState, "end": pokemon.removeVolatile, "effectHolder": pokemon
                    }, callbackName)
                )
        ability = pokemon.getAbility()
        callback = ability[callbackName]
        if not callback or (getKey and pokemon.abilityData[getkey] if getkey in pokemon.abilityData):
            handlers.update(
                self.resolvePriority({
                    "effect": ability, "callback": callback, "state": pokemon.abilityData, "end": pokemon.clearAbility, "effectHolder": pokemon
                }, callbackName)
            )
        
        item = pokemon.getItem()

        callback = item[callbackName]
        if not callback or (getKey and pokemon.itemData[getkey] if getkey in pokemon.itemData):
            handlers.update(
                self.resolvePriority({
                    "effect": item, "callback": callback, "state": pokemon.itemData, "end": pokemon.clearItem, "effectHolder": pokemon
                }, callbackName)
            )

        species = pokemon.baseSpecies
        callback = species[callbackName]
        if not callback:
            handlers.update(
                self.resolvePriority({
                    "effect": species, "callback": callback, "state": pokemon.speciesData, "end": {}, "effectHolder": pokemon
                }, callbackName)
            )
        
        side = pokemon.sides
        for conditionid in side.slotConditions[pokemon.position]:
            slotConditionData = side.slotConditions[pokemon.position][conditionid]
            slotCondition = side.getSlotCondition(pokemon, conditionid)

            callback = slotCondition[callbackName]
            if not callback or (getKey and slotConditionData if getkey in slotConditionData):
                handlers.update(
                    self.resolvePriority({
                        "effect": slotCondition, 
                        "callback": callback, 
                        "state": slotConditionData, 
                        "end": side.removeSlotCondition, 
                        "endCallArgs": [side, pokemon, slotCondition.id],
                        "effectHolder": side
                    }, callbackName)
            ) 
        return handlers

    def start(self):
        print("------------------start---------------")
        if self.deserialized: return
        # need all players to start
        if (not all(self.sides)):
            raise Exception("Missing sides: " + self.sides)

        if self.started : 
            raise Exception("Battle already started")

        self.started = True
        self.sides[1].foe = self.sides[0]
        self.sides[0].foe = self.sides[1]

        # print("side.foe",self.sides[0].foe.name)

        # format.onBegin ?

        # print(self.sides[0].pokemon)#, self.sides[1].pokemon[0])

        if (not any([self.sides[0].pokemon, self.sides[1].pokemon])):
            raise Exception("Battle not started: A player has an empty team.")

        # if self.debugMode

        # self.residualEvent

        self.queue.addChoice({"choice": "start"})
        self.midTurn = True
        if not self.requestState: self.go()


    def setPlayer(self, slot, options):
        print("battle > setPlayer")
        # side
        didSomething = True
        SLOTNUM = int(slot[1]) - 1
        if (not self.sides[SLOTNUM]):
            print("create player")
            TEAM = self.getTeam(options)
            side_ = side.Side((options["name"] or ("Player" + str(SLOTNUM +1))), self, SLOTNUM, TEAM)
            # print("side_", side_.team, TEAM)
            self.sides[SLOTNUM] = side_
        else:
            print("TODO edit Player")

        print("side",all(self.sides),self.sides)

        if (all(self.sides) and not self.started):
            print("-----start-----")
            self.start()

    def validTargetLoc(self, targetLoc, source, targetType):
        if targetLoc is 0: return True
        numSlots = len(source.side.active)
        if abs(targetLoc) > numSlots: return False

        sourceLoc = -(source.position +1)
        isFoe = (targetLoc > 0)
        acrossFromTargetLoc = -(numSlots + 1 - targetLoc)
        isAdjacent = abs(acrossFromTargetLoc - sourceLoc)<=1 if isFoe else (abs(targetLoc - sourceLoc) is 1)
        isSelf = (sourceLoc is targetLoc)

        if targetType is "randomNormal" or "scripted" or "normal":
            return isAdjacent
        elif targetType is "adjacentAlly":
            return isAdjacent and not isFoe
        elif targetType is "adjacentAllyOrSelf":
            return isAdjacent and not isFoe or isSelf
        elif targetType is "adjacentFoe":
            return isAdjacent and isFoe
        elif "any":
            return not isSelf
        else:
            pass

        return False



    def getTargetLoc(self, target, source):
        position = target.position + 1
        return -position if target.side is source.side else position

    # def validTarget

    def getAtLoc(self, pokemon, targetLoc):
        if targetLoc > 0:
            return pokemon.side.foe.active[targetLoc -1]
        else:
            return pokemon.side.active[-targetLoc -1]

    def getTarget(self, pokemon, move, targetLoc, originalTarget):
        """

        return self.getRandomTarget or originalTarget or
        """
        move = self.dex.getMove(move)
        tracksTarget = move.tracsTarget

        if pokemon.hasAbility(["stalwart", "proprllertail"]):
            tracksTarget = True
        if tracksTarget and originalTarget and originalTarget.isActive:
            return originalTarget

        if move.smartTarget:
            return self.getAtLoc(pokemon, targetLoc)
        
        if any((x in move.target) for x in ["adjacentAlly", "any", "normal"]) and targetLoc is -(pokemon.position + 1) and \
            not pokemon.volatiles["twoturnmove"] and not pokemon.volatiles["iceball"] and not pokemon.volatiles["rollout"]:
            return pokemon if move.isFutureMove else None
        
        if move.target is not "randomNormal" and self.validTargetLoc(targetLoc, pokemon, move.target):
            target = self.getAtLoc(pokemon, targetLoc)
            if _optionalChain([target, "optionalAccess", _opt_11]) and target.side is pokemon.side:
                # Target is a fainted ally: attack shouldn't retarget
                return target
            if target and not target.fainted:
                # Target is unfainted: use selected target location
                return target
            # Chosen target not valid,
            # retarget randomly with getRandomTarget
        return self.getRandomTarget(pokemon, move)



    def getRandomTarget(self, pokemon, move):
        move = self.dex.getMove(move)
        if move.target is "adjacentAlly":
            allyActives = pokemon.side.active
            adjacentAllies = list(filter(lambda x: x and not x.fainted , adjacentAllies))
            return self.sample(adjacentAllies) if len(adjacentAllies) else None

        if move.target is "self" or move.target is "all" or move.target is "allySide" or\
            move.target is "allyTeam" or move.target is "adjacentAllyOrSelf":
            return pokemon

        if len(pokemon.side.active) > 2:
            if move.target is "adjacentFoe" or move.target is "normal" or move.target is "randomNormal":
                foeActives = pokemon.side.foe.active
                frontPosition = len(foeActives) -1 - pokemon.position
                adjacentFoes = foeActives[(0 if frontPosition < 1 else frontPosition -1),frontPosition + 2]
                adjacentFoes = list(filter(lambda x: x and not x.fainted, adjacentFoes))
                if len(adjacentFoes): return self.sample(adjacentFoes)
                return foeActives[frontPosition]
        
        return pokemon.side.foe.randomActive() or pokemon.side.foe.active[0]

    # def checkFainted()
    # def faintMessages
    
    def getActionSpeed(self, action):
        if action["choice"] is "move":
            move = action["move"]
            if action["zmove"]:
                # zMoveName = self.getZMove(action["move"], action["pokemon"], True)
                raise Exception("zmove is not implemented")

            if action["maxMove"]:
                maxMoveName = self.getMaxMove(action["maxMove"], action["pokemon"])
                # pass
            
            priority = self.dex.getMove(move.id).priority
            # singleEvent

            action["priority"] = priority + action["fractionalPriority"]
            if self.gen > 5: action["move"].priority = priority

        if not (action["pokemon"] if "pokemon" in action else False):
            action["speed"] = 1
        else:
            action["speed"] = action["pokemon"].getActionSpeed()


    def go(self):
        if self.requestState: self.requestState = ""

        if not self.midTurn:
            self.queue.insertChoice({"choice": "beforeTurn"})



    def getTeam(self, options):
        if self.log_flag:print("battle > getTeam")
        team = options["team"]
        print(team)
        print(type(team))
        if type(team) == str:
            team = _dex.Dex.fastUnpackTeam(team)
        print("team", team)

        if self.log_flag:print("battle > getTeam end")
        return team


    def getMaxMove(self, move, pokemon):
        raise Exception("getMaxMove is not implemented")

            
