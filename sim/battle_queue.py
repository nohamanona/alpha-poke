

class BattleQueue:
    def __init__(self,battle):
        self.battle = battle
        self.list = []
        # queueScripts = battle.format.queue or battle.dex.data()["Scripts"].queue
        # Scriptsにqueueがないので未実装

    def shift(self):
        return self.list.pop(0)

    def peek(self):
        return self.list[0]

    def push (self,action):
        return self.list.append(action)

    def unshift(self,action):
        return self.list.insert(0,action)

    # Symbol.iterator?

    # def entries(self):
    #     return self.list

    def resolveAction(self,action, midTurn = False):
        if not action : raise Exception("Action not passed to resolveAction")
        if action["choice"] == "pass": return []
        actions = [action]

        if not (action["side"] if "side" in action else False) and (action["pokemon"] if "pokemon" in action else False):
            ction["side"] = action["pokemon"]["side"]
        if not (action["move"] if "move" in action else False) and (action["moveid"] if "moveid" in action else False):
            action["move"] = self.battle.dex.getActiveMove(action["moveid"])
        if not (action["order"] if "order" in action else False):
            orders = {
                "team": 1,
                "start": 2,
                "instaswitch": 3,
                "beforeTurn": 4,
                "beforeTurnMove": 5,

                "runUnnerve": 100,
                "runSwitch": 101,
                "runPrimal": 102,
                "switch": 103,
                "megaEvo": 104,
                "runDynamax": 105,

                "shift": 200,
				# // default is 200 (for moves)

                "residual": 300,
            }
            if action["choice"] in orders:
                action["order"] = orders[action["choice"]]
            else:
                action["order"] = 200
                if any((x in action["choices"]) for x in ["move", "event"]):
                    raise Exception("Unexpected orderless action" + action["choice"])
        
        if not midTurn:
            if action["choice"] is "move":
                if not action["maxMove"] and not action["zmove"] and action["move"]["beforeTurnCallback"]:
                    actions.unshift(*self.resolveAction({
                        "choice": "beforeTurnMove",
                        "pokemon": action["pokemon"],
                        "move": action["move"],
                        "targetLoc": action["targetLoc"],
                    }))
                if action["mega"]:
                    actions.unshift(*self.resolveAction({
                        "choice": "megaEvo",
                        "pokemon": action["pokemon"],
                    }))
                if action["maxMove"] and not action["pokemon"].volatiles["dynamax"]:
                    actions.unshift(*self.resolveAction({
                        "choice": "runDynamax",
                        "pokemon": action["pokemon"]
                    }))
                # action["fractionalPriority"] = 
            elif any(((x in action["choices"]) if "choices" in action else False) for x in ["switch", "instaswitch"]):
                if type(action["pokemon"].switchFlag) is str:
                    action["sourceEffect"] = self.battle.dex.getMove(action["pokemon"].switchFlag)
                action["pokemon"].switchFlag = False
        
        deferPriority = self.battle.gen is 7 and action["mega"] and action["mega"] is not "done"
        if action["move"] if "move" in action else False:
            target = None
            action["move"] = self.battle.dex.getActiveMove(action["move"])

            if not action["targetLoc"]:
                target = self.battle.getRandomTarget(action["pokemon"], action["move"])
                if target:
                    action["targetLoc"] = self.battle.getTargetLoc(target, action["pokemon"])
            action["originalTarget"] = self.battle.getAtLoc(action["pokemon"], action["targetLoc"])
        
        if not deferPriority: self.battle.getActionSpeed(action)
        return actions



    # def prioritizeAction

    # def changeAction

    def addChoice(self, choices):
        if type(choices) is not list: choices = [choices]
        for choice in choices:
            self.list.append(*self.resolveAction(choice))

    # def willAct
    # def willMove
    # def cancelAction
    # def cancelMove
    # def willSwitch

    def insertChoice(self, choices, midTurn = False):
        if type(choices) == list:
            for choice in choices:
                self.insertChoice(choice)

            return
        
        choice = choices

        if (choice["pokemon"] if "pokemon" in choice else False):
            choice["pokemon"].updateSpeed()

