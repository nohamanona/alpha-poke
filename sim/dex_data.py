import re

class Tools:
    
    @staticmethod
    def getString(instr):
        if type(instr)==str:
            instr = instr
        elif type(instr)==int:
            instr = str(instr)
        else:
            instr = ''
        return instr

    @staticmethod
    def getId(text):
        if type(text) == str:
            text = text
        elif type(text)== dict and text["id"]:
            text = text["id"]
        elif type(text)== dict and text["userid"]:
            text = text["userid"]
        elif type(text)== dict and text["roomid"]:
            text = text["roomid"]
        
        if type(text) != str and type(text) != int: return ""
        if type(text) == int:
            text = str(text)
        # print("getId",text, text.lower())
        return re.sub('[^a-z0-9]','',("" + text).lower())

class BasicEffect:
    def __init__(self, data , **kwargs):
        self.exists = True
        data.update(kwargs)

        self.id = data["id"] if "id" in data else ""
        self.name = Tools.getString(data["name"]).strip(' ')
        self.effectType = Tools.getString(data["effectType"]) if "effectType" in data else 'Type'
        self.exists = self.exists and self.id
        self.num = data["num"] if "num" in data else 0
        self.gen = data["gen"] if "gen" in data else 0
        self.shortDesc = data["shortDesc"] if "shortDesc" in data else ""
        self.desc = data["desc"] if "desc" in data else ""
        self.isNonstandard = data["isNonstandard"] if "isNonstandard" in data else None
        self.duration = data["duration"] if "duration" in data else None
        self.noCopy = data["noCopy"] if "noCopy" in data else None
        self.affectFainted = data["affectFainted"] if "affectFainted" in data else None
        self.status = data["status"] if "status" in data else None
        self.weather = data["weather"] if "weather" in data else None
        self.sourceEffect = data["sourceEffect"] if "sourceEffect" in data else ""


class Format(BasicEffect):
    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        # data = self

        self.mod = Tools.getString(data["mod"]) if "mod" in data else "gen8"
        self.effectType = Tools.getString(data["effectType"]) if "effectType" in data else "Format"
        self.debug = data["debug"] if "debug" in data else None
        self.rated = (data["rated"] is not False) if "rated" in data else False
        self.gameType = data["gameType"] if "gameType" in data else "singles"
        self.ruleset = data["ruleset"] if "ruleset" in data else []
        self.baseRuleset = data["baseRuleset"] if "baseRuleset" in data else []
        self.banlist = data["banlist"] if "banlist" in data else []
        self.restricted = data["restricted"] if "restricted" in data else []
        self.unbanlist = data["unbanlist"] if "unbanlist" in data else []
        self.customRules = data["customRules"] if "customRules" in data else None
        self.ruleTable = None
        self.teamLength = data["teamLength"] if "teamLength" in data else None
        self.onBegin = data["onBegin"] if "onBegin" in data else None
        self.minSourceGen = data["minSourceGen"] if "minSourceGen" in data else None
        self.maxLevel = data["maxLevel"] if "maxLevel" in data else 100
        self.defaltLevel = data["defaltLevel"] if "defaltLevel" in data else self.maxLevel
        self.forcedLevel = data["forcedLevel"] if "forcedLevel" in data else None
        self.maxForcedLevel = data["maxForcedLevel"] if "maxForcedLevel" in data else None
        self.noLog = data["noLog"] if "noLog" in data else None

class Condition(BasicEffect):
    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        self.effectType = self.effectType if any(x in self.effectType for x in ["Weather", "Status"]) else "Condition"
        


class Species(BasicEffect):
    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)

        self.fullname = 'pokemon: '+ data["name"]
        self.effectType = 'Pokemon'
        self.id = data["id"] if "id" in data else ""
        self.name = data["name"]
        self.baseSpecies = data["baseSpecies"] if "baseSpecies" in data else self.name
        self.forme = data["forme"] if "forme" in data else ""
        self.baseForme = data["baseForme"] if "baseForme" in data else ""
        self.cosmeticFormes = data["cosmeticFormes"] if "cosmeticFormes" in data else ""
        self.otherFormes = data["otherFormes"] if "otherFormes" in data else ""
        self.formeOrder = data["formeOrder"] if "formeOrder" in data else ""
        self.spriteid = data["spriteid"] if "spriteid" in data else \
            (Tools.getId(self.baseSpecies) + (("-"+ Tools.getId(self.forme)) if self.baseSpecies is not self.name else "" ))
        self.abilities = data["abilities"] if "abilities" in data else {"0": ""}
        self.types = data["types"] if "types" in data else ["???"]
        self.addedType = data["addedType"] if "addedType" in data else None
        self.prevo = data["prevo"] if "prevo" in data else ""
        self.tier = data["tier"] if "tier" in data else ""
        self.doublesTier = data["doublesTier"] if "doublesTier" in data else ""
        self.evos = data["evos"] if "evos" in data else []
        self.evoType = data["evoType"] if "evoType" in data else None
        self.evoMove = data["evoMove"] if "evoMove" in data else None
        self.evoLevel = data["evoLevel"] if "evoLevel" in data else None
        self.nfe = data["nfe"] if "nfe" in data else False
        self.eggGroups = data["eggGroups"] if "eggGroups" in data else []
        self.gender = data["gender"] if "gender" in data else ""
        if "genderRatio" in data:
            self.genderRatio = data["genderRatio"]
        else:
            if self.gender == "M":
                self.genderRatio = {"M": 1, "F": 0}
            elif self.gender == "F":
                self.genderRatio = {"M": 0, "F": 1}
            elif self.gender == "N":
                self.genderRatio = {"M": 0, "F": 0}
            else:
                self.genderRatio = {"M": 0.5, "F": 0.5}
        self.requiredItem = data["requiredItem"] if "requiredItem" in data else None
        self.requiredItems = data["requiredItems"] if "requiredItems" in data else ([self.requiredItem] if self.requiredItem else None)
        self.baseStats = data["baseStats"] if "baseStats"in data else {"hp": 0, "atk":0, "def":0, "spa":0, "spd":0, "spe":0}
        self.weightkg = data["weightkg"] if "weightkg" in data else 0
        self.seighthg = int(self.weightkg) * 10
        self.heightm = data["heightm"] if "heightm" in data else 0
        self.color = data["color"] if "color" in data else ""
        self.unreleasedHidden = data["unreleasedHidden"] if "unreleasedHidden" in data else False
        self. maleOnlyHidden = data["maleOnlyHidden"] if "maleOnlyHidden" in data else None
        self.maxHP = data["maxHP"] if "maxHP" in data else None
        self.isMega = False # temp
        self.canGigantamax = data["canGigantamax"] if "canGigantamax" in data else None
        self.gmaxUnreleased = data["gmaxUnreleased"] if "gmaxUnreleased" in data else None
        self.cannotDynamax = data["cannotDynamax"] if "cannotDynamax" in data else None
        self.battleOnly = data["battleOnly"] if "battleOnly" in data else (self.baseSpecies if self.isMega else None)
        self.changeFrom = data["changesFrom"] if "changesFrom" in data else\
            (self.battleOnly if self.battleOnly is not self.baseSpecies else self.baseSpecies)
        
        if hasattr(self, 'gen') and self.num >= 1:
            if self.num >= 810 or any((s in self.forme) for s in ["Gmax", "Galar", "Galar-Zen"]):
                self.gen = 8
            elif self.num >= 722 or self.forme.startswith("Alola") or self.forme == "Starter":
                self.gen = 7
            elif self.forme == "Primal":
                self.gen = 6
                self.isPrimal = True
                self.battleOnly = self.baseSpecies
            elif self.num >= 650 or self.isMega:
                self.gen = 6
            elif self.num >= 494:
                self.gen = 5
            elif self.num >= 387:
                self.gen = 4
            elif self.num >= 252:
                self.gen = 3
            elif self.num >= 152:
                self.gen = 2
            else:
                self.gen = 1




class Move(BasicEffect):
    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        # print(data)

        self.fullname ="move: " + self.name
        self.effectType = "Move"
        self.type = Tools.getString(data["type"])
        self.target = data["target"]
        self.basePower = int(data["basePower"])
        self.accuracy = data["accuracy"]
        self.critRatio = float(data["critRatio"]) if "critRatio" in data else float(1)
        self.secondary = data["secondaries"] if "secondaries" in data else None
        if "secondaries" in data and data["secondaries"] != "":
            self.secondaries = data["secondaries"]
        elif self.secondary:
            self.secondaries = self.secondary and [self.secondary]
        else:
            self.secondaries = None
        self.priority = int(data["priority"]) if "priority" in data else 0
        self.category = data["category"] if "category" in data else None
        self.defensiveCategory = data["defensiveCategory"] if "defensiveCategory" in data else None
        self.useTargetOffensive = data["useTargetOffensive"] if "useTargetOffensive" in data else None
        self.useSourceDefensiveAsOffensive = data["useSourceDefensiveAsOffensive"] if "useSourceDefensiveAsOffensive" in data else None
        self.ignoreNegativeOffensive = data["ignoreNegativeOffensive"] if "ignoreNegativeOffensive" in data else None
        self.ignorePositiveDeffensive = data["ignorePositiveDeffensive"] if "ignorePositiveDeffensive" in data else None
        self.ignoreOffensive = data["ignoreOffensive"] if "ignoreOffensive" in data else None
        self.igdnoreDefensive = data["igdnoreDefensive"] if "igdnoreDefensive" in data else None
        self.ignoreImmunity = data["ignoreImmunity"] if "ignoreImmunity" in data else self.category == "Status"
        self.pp = int(data["pp"])
        self.noPPBoosts = data["noPPBoosts"] if "noPPBoosts" in data else None
        self.isZ = data["isZ"] if "isZ" in data else False
        self.isMax = data["isMax"] if "isMax" in data else False
        self.flags = data["flags"] if "flags" in data else {}
        if "selfSwitch" in data:
            if type(data["selfSwitch"])==str:
                self.selfSwitch = data["selfSwitch"]
            else:
                self.selfSwitch = None
        else:
            self.selfSwitch = None
        self.pressureTarget = data["pressureTarget"] if "pressureTarget" in data else ""
        self.nonGhostTarget = data["nonGhostTarget"] if "nonGhostTarget" in data else ""
        self.ignoreAbility = data["ignoreAbility"] if "ignoreAbility" in data else False
        self.damage = data["damage"] if "damage" in data else None
        self.spreadHit = data["spreadHit"] if "spreadHit" in data else False
        self.forceSTAB = data["forceSTAB"] if "forceSTAB" in data else None
        self.noSketch = data["noSketch"] if "noSketch" in data else None
        self.stab = data["stab"] if "stab" in data else None
        if "volatileStatus" in data:
            if type(data["volatileStatus"])==str:
                self.volatileStatus = data["volatileStatus"]
            else:
                None
        else:None
        self.maxMove = {}
        if (self.category != "Status" and self.id != "struggle"):
            self.maxMove = {"basePower":1}
            if self.isMax or self.isZ:
                # already initialized to 1
                pass
            elif (self.basePower == None):
                self.maxMove["basePower"] = 100
            elif "Fighting" in self.type or "Poison" in self.type:
                if self.basePower >= 150:
                    self.maxMove["basePower"] = 100
                elif self.basePower >= 110:
                    self.maxMove["basePower"] = 95
                elif self.basePower >= 75:
                    self.maxMove["basePower"] = 90
                elif self.basePower >= 65:
                    self.maxMove["basePower"] = 85
                elif self.basePower >= 55:
                    self.maxMove["basePower"] = 80
                elif self.basePower >= 45:
                    self.maxMove["basePower"] = 75
                else:
                    self.maxMove["basePower"] = 70
            else:
                if self.basePower >= 150:
                    self.maxMove["basePower"] = 150
                elif self.basePower >= 110:
                    self.maxMove["basePower"] = 140
                elif self.basePower >= 75:
                    self.maxMove["basePower"] = 130
                elif self.basePower >= 65:
                    self.maxMove["basePower"] = 120
                elif self.basePower >= 55:
                    self.maxMove["basePower"] = 110
                elif self.basePower >= 45:
                    self.maxMove["basePower"] = 100
                else:
                    self.maxMove["basePower"] = 90

        if self.gen == None:
            if self.num >= 743:
                self.gen = 8
            elif self.num >= 622:
                self.gen = 7
            elif self.num >= 560:
                self.gen = 6
            elif self.num >= 468:
                self.gen = 5
            elif self.num >= 355:
                self.gen = 4
            elif self.num >= 252:
                self.gen = 3
            elif self.num >= 166:
                self.gen = 2
            elif self.num >= 1:
                self.gen = 1


                    
                




        

