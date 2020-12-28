import os
import json
from collections import OrderedDict
import pprint
import copy
from importlib import import_module
# import traceback

from sim import dex_data

toID = dex_data.Tools.getId

Log = True

BASE_MOD = 'gen8'
DEFAULT_MOD = BASE_MOD
DATA_DIR = "./data-dist"
MODS_DIR = "./data-dist/mods"
FORMATS = "./config-dist/"

DEXES = {}

DATA_TYPES = [
	'Abilities', 'Formats', 'FormatsData', 'Items', 'Learnsets', 'Moves',
	'Natures', 'Pokedex', 'Scripts', 'Conditions', 'TypeChart',
]

DATA_FILES = {
	"Abilities": 'abilities',
	"Aliases": 'aliases',
	"Formats": 'rulesets',
	"FormatsData": 'formats-data',
	"Items": 'items',
	"Learnsets": 'learnsets',
	"Moves": 'moves',
	"Natures": 'natures',
	"Pokedex": 'pokedex',
	"Scripts": 'scripts',
	"Conditions": 'conditions',
	"TypeChart": 'typechart',
}

nullEffect = dex_data.Condition({"name": "", "exists": False})

NATURES = {
    "adamant": {"name": "Adamant", "plus": 'atk', "minus": 'spa'},
	"bashful": {"name": "Bashful"},
	"bold": {"name": "Bold", "plus": 'def', "minus": 'atk'},
	"brave": {"name": "Brave", "plus": 'atk', "minus": 'spe'},
	"calm": {"name": "Calm", "plus": 'spd', "minus": 'atk'},
	"careful": {"name": "Careful", "plus": 'spd', "minus": 'spa'},
	"docile": {"name": "Docile"},
	"gentle": {"name": "Gentle", "plus": 'spd', "minus": 'def'},
	"hardy": {"name": "Hardy"},
	"hasty": {"name": "Hasty", "plus": 'spe', "minus": 'def'},
	"impish": {"name": "Impish", "plus": 'def', "minus": 'spa'},
	"jolly": {"name": "Jolly", "plus": 'spe', "minus": 'spa'},
	"lax": {"name": "Lax", "plus": 'def', "minus": 'spd'},
	"lonely": {"name": "Lonely", "plus": 'atk', "minus": 'def'},
	"mild": {"name": "Mild", "plus": 'spa', "minus": 'def'},
	"modest": {"name": "Modest", "plus": 'spa', "minus": 'atk'},
	"naive": {"name": "Naive", "plus": 'spe', "minus": 'spd'},
	"naughty": {"name": "Naughty", "plus": 'atk', "minus": 'spd'},
	"quiet": {"name": "Quiet", "plus": 'spa', "minus": 'spe'},
	"quirky": {"name": "Quirky"},
	"rash": {"name": "Rash", "plus": 'spa', "minus": 'spd'},
	"relaxed": {"name": "Relaxed", "plus": 'def', "minus": 'spe'},
	"sassy": {"name": "Sassy", "plus": 'spd', "minus": 'spe'},
	"serious": {"name": "Serious"},
	"timid": {"name": "Timid", "plus": 'spe', "minus": 'atk'},
}

class ModdedDex:
    def __init__(self, mod='base', isOriginal = False):
        # self.ModdedDex = None

        self.name = "[ModdedDex]"
        self.isBase = (mod == "base")
        self.currentMod = mod
        
        self.abillityCache = {}
        self.effectCache = {}
        self.itemCache = {}
        self.moveCache = {}
        self.learnsetCache = {}
        self.speciesCache = {}
        self.typeCache = []

        self.gen = 0

        self.modsLoaded = False

        self.dataCache = None
        self.formatsCache = None

    def data(self):
        return self.loadData()

    def formats(self):
        self.includeFormats()
        return self.formatsCache

    def forFormat(self, battle, format):
        self.battle = battle
        if not self.modsLoaded:
            self.includeMods()
        MOD = self.getFormat(self.battle, format).mod
        return DEXES[MOD].includeData(self.battle)

    def dataDir(self):
        return (DATA_DIR if self.isBase else MODS_DIR + '/' + self.currentMod )

    @staticmethod
    def fastUnpackTeam(buf):
        print("fastUnpackTeam")
        if (not buf): 
            print("not buf")
            return None
        if (type(buf) != str): 
            print("buf is not str")
            return buf
        TEAM = []
        i=0
        j=0
        for i in range(1): # original 24
            SET = {}
            TEAM.append(SET)

            # name
            j = buf.find('|',i)
            if(j<0): return None
            SET["name"] = buf[i:j]
            i = j+1
            # print(i,j,SET["name"])

            # species
            j = buf.find('|',i)
            if(j<0): return None
            SET["species"] = buf[i:j]
            i = j+1
            # print(i,j,SET["species"])

            # item
            j = buf.find('|',i)
            if(j<0): return None
            SET["item"] = buf[i:j]
            i = j+1

            # ability　とくせい
            j = buf.find('|',i)
            if(j<0): return None
            SET["ability"] = buf[i:j]
            # SPECIES = Dex.getSpecies(SET["species"])
            i = j+1

            # moves
            j = buf.find('|',i)
            if(j<0): return None
            SET["moves"] = [x for x in buf[i:j].split(',') if x != '']
            i = j+1
            # print("moves",SET["moves"])

            # nature せいかく
            j = buf.find('|',i)
            if(j<0): return None
            SET["nature"] = buf[i:j]
            i = j+1

            # evs　努力値
            j = buf.find('|',i)
            if(j<0): return None
            if(j != i):
                EVS = buf[i:j].split(',')
                SET['evs'] = {
                    'hp':int(EVS[0] or 0),
                    'atk':int(EVS[1] or 0),
                    'def':int(EVS[2] or 0),
                    'spa':int(EVS[3] or 0),
                    'spd':int(EVS[4] or 0),
                    'spe':int(EVS[5] or 0)
                }
            i = j+1
            # print(SET['evs'])

            # gender
            j = buf.find('|',i)
            if(j<0): return None
            if(i!=j):SET["gender"] = buf[i:j]
            i = j+1

            # ivs 個体値
            j = buf.find('|',i)
            if(j<0): return None
            if(j != i):
                IVS = buf[i:j].split(',')
                SET['ivs'] = {
                    'hp':31 if IVS[0]=="" else int(IVS[0] or 0),
                    'atk':31 if IVS[0]=="" else int(IVS[1] or 0),
                    'def':31 if IVS[0]=="" else int(IVS[2] or 0),
                    'spa':31 if IVS[0]=="" else int(IVS[3] or 0),
                    'spd':31 if IVS[0]=="" else int(IVS[4] or 0),
                    'spe':31 if IVS[0]=="" else int(IVS[5] or 0)
                }
            i = j+1
            # print("ivs",SET['ivs'])

            # shiny
            j = buf.find('|',i)
            if(j<0): return None
            if(i!=j):SET["shiny"] = True
            i = j+1

            # level
            j = buf.find('|',i)
            if(j<0): return None
            if(i!=j):SET["level"] = int(buf[i:j])
            i = j+1

            # happiness
            j = buf.find(']',i)
            if (j < 0): break
            i = j+1

        return TEAM

    # @staticmethod
    def getSpecies(self, name):  #　未完成
        print("> dex getSpecies Start")
        if Log:print("getSpecies", name)
        if(name and type(name) != str): return name

        name = (name or "").strip(' ')
        id = toID(name)
        if (id == 'nidoran' and name[-1] == '♀'):
            id = 'nidoranf'
        elif (id == 'nidoran' and name[-1] == '♂'):
            id = 'nidoranm'

        if id in self.speciesCache:
            species = self.speciesCache[id]
            return species
        print("----------------------get species--------------------")
        # print(self.data()["Aliases"]["maero"])
        if id in self.data()["Aliases"]:
            if Log:print("id in Aliases")
            if id in self.data()["FormatsData"]:
                if Log:print("id in FormatsData")
                baseId = toID(self.data()["Aliases"][id])
                species = dex_data.Species({name}, self.data()["Pokedex"][baseId], self.data()["FormatsData"][id])
                species.name = id
                species.id = id
                species.abilities = {"0": species.abilities["S"]}
            else:
                if Log:print("id not in FormatsData")
                species = self.getSpecies(self.data()["Aliases"][id])
                if species.cosmeticFormes:
                    for forme in species.cosmeticFormes:
                        if toID(forme) == id:
                            species = dex_data.Species(species,{
                                "name": forme,
                                "id": id,
                                "forme": forme[len(species.name) + 1 : ],
                                "baseForme": "",
                                "baseSpecies": species.name,
                                "otherFormes": None,
                                "cosmeticFormes": None,
                            })
                            break
            if species:
                self.speciesCache[id] = species
            return species
        
        if id not in self.data()["Pokedex"]:
            if Log:print("id not in Pokedex")
            aliasTo = " "
            FORMENAMES = {
                "alola": ["a", "alola", "alolan"],
                "galar": ["g", "galar", "galarian"],
                "mega": ["m", "mega"],
                "primal": ["p", "primal"],
            }
            for forme in FORMENAMES:
                pokeName = " "
                for i in FORMENAMES[forme]:
                    if id.startswith(i):
                        pokeName = id[len(i): ]
                    elif id.endswith(i):
                        pokeName = id[ : -len(i)]
                if pokeName in self.data()["Aliases"]: pokeName = toID(self.data()["Aliases"]["pokeName"])
                if self.data()["Pokedex"][pokeName + forme]:
                    aliasTo = pokeName + forme
                    break

            if aliasTo:
                species = self.getSpecies(aliasTo)
                if species.exists:
                    self.speciesCache[id] = species
                    return species


        if id and id in self.data()["Pokedex"]:
            if Log:print("id in Pokedex")
            species = dex_data.Species({"name":name}, **self.data()["Pokedex"][id], **self.data()["FormatsData"][id])
            baseSpeciesStatuses = self.data()["Conditions"][toID(species.baseSpecies)] if toID(species.baseSpecies) in self.data()["Conditions"] else None
            if baseSpeciesStatuses is not None:
                for key in baseSpeciesStatuses:
                    if key not in species: species[key] = baseSpeciesStatuses[key]

            if not species.tier and not species.doublesTier and species.baseSpecies is not species.name:
                if species.baseSpecies is "Mimikyu":
                    species.tier = self.data()["FormatsData"][toID(species.baseSpecies)].tier or "Illegal"
                    species.doublesTier = self.data()["FormatsData"][toID(species.baseSpecies)].doublesTier or "Illegal"
                elif species.id.endswith("totem"):
                    species.tier = self.data()["FormatsData"][species.id[0:-5]].tier or "Illegal"
                    species.doublesTier = self.data()["FormatsData"][species.id[0:-5]].doublesTier or "Illegal"
                elif species.battleOnly:
                    species.tier = self.data()["FormatsData"][toID(species.battleOnly)].tier or "Illegal"
                    species.doublesTier = self.data()["FormatsData"][toID(species.battleOnly)].doublesTier or "Illegal"
                else:
                    baseFormatsData = self.data()["FormatsData"][toID(species.baseSpecies)]
                    if not baseFormatsData:
                        raise Exception(species.baseSpecies + " has no formats-data entry")
                    species.tier = baseFormatsData.tier or "Illegal"
                    species.doublesTier = baseFormatsData.doublesTier or "Illegal"
            
            if not species.tier: species.tier = "Illegal"
            if not species.doublesTier: species.doublesTier = species
            if species.gen > self.gen:
                species.tier = "Illegal"
                species.doublesTier = "Illegal"
                species.isNonstandard = "Future"
            if self.currentMod == "letsgo" and not species.isNonstandard:
                isLetsGo = (
                    (species.num <= 151 or ["Meltan", "Melmetal"] in species.name) and \
                        (not species.forme or ["Alola", "Mega", "Mega-X", "Mega-Y", "Starter"] in species.forme)
                )
                if not isLetsGo: species.isNonstandard = "Past"
            # print("species evos[0]", species.evos)
            species.nfe = len(species.evos) and self.getSpecies(species.evos[0]).gen <= self.gen
        else:
            species = dex_data.Species({
                "id": id, "name": name, "exists": False, "tier": "Illegal", "isNonstandard": "Custom"
            })
        if species.exists: self.speciesCache[id] = species
        return species
        
        # input()

        
        print("a",id,"a")
        # print(self.includeMods())

        print("> dex getSpecies end")

        return id

    def getMove(self, name):
        if (name and type(name) != str): return name

        name = (name or "").strip(' ')
        move_id = toID(name)
        move = self.moveCache[move_id] if move_id in self.moveCache else ""
        if move: return move
        if move_id in self.data()["Aliases"]:
            move = self.getMove(self.data()["Aliases"][move_id])
            if "exists" in move and move["exists"]:
                self.moveCache["id"] = move
            return move
        if move_id[0:11] == "hiddenpower":
            #未実装
            pass
        if move_id in self.data()["Moves"]:
            move = dex_data.Move({"name":name}, **self.data()["Moves"][move_id])
            if move.gen > self.gen:
                move.isNonstandard = "Future"
        else:
            move = dex_data.Move({"id":move_id, "name":name, "exists":False})

        if move.exists:
            self.moveCache[move_id] = move
        return move

    def getActiveMove(self, move):
        if move and type(move.hit) == int: return move
        move = self.getMove(move)
        moveCopy = self.deepClone(move)
        moveCopy.hit = 0
        return moveCopy

    def getEffect(self, name):
        if not name:
            return nullEffect
        if type(name) is not str:
            return name
        
        id = toID(name)
        effect = self.effectCache[id]
        if effect:
            return effect
        
        if name.startswith("move:"):
            effect = self.getMove(name[5:])
        elif name.startswith("item:"):
            effect = self.getItem(name[5:])
        elif name.startswith("ability:"):
            ability = self.getAbility(name[8:])
            ability["id"] = "ability:" + ability.import ipdb; ipdb.set_trace()
            effect = ability
        
        if effect:
            self.effectCache[id] = effect
            return effect
        
        return self.getEffectByID(id, effect)


    def getEffectByID(self, id, effect):
        if not id:
            return nullEffect
        if not effect:
            effect = self.effectCache[id]
        if effect:
            return effect

        if id in dir(self.data()["Formats"]):
            effect = dex_data.Format({"name": id}, getattr(self.data.["Formats"], id))
        elif id in dir(self.data()["Conditions"]):
            effect = dex_data.Condition({"name":id}, getattr(self.data()["Conditions"], id))
        elif id in dir(self.data()["Moves"]) and getattr(self.data()["Moves"],id).condition if "condition" in getattr(self.data()["Moves"], id):
            found = getattr(self.data()["Moves"],id).condition
            effect = dex_data.Condition({"name": found.name or id}, found.condition)
        elif id in dir(self.data()["Abilities"]) and getattr(self.data()["Abilities"], id).condition if "conditon" in getattr(self.data()["Abilities"],id):
            found = getattr(self.data()["Abilities"],id).condition
            effect = dex_data.Condition({"name": found.name or id}, found.condition)
        elif id in dir(self.data()["Items"]) and getattr(self.data()["Items"], id).condition if "conditon" in getattr(self.data()["Items"],id):
            found = getattr(self.data()["Items"],id).condition
            effect = dex_data.Condition({"name": found.name or id}, found.condition)
        elif id is "recoil":
            effect = dex_data.Condition({"id":id,"name": "Recoil", "effectType":"Recoil"})
        elif id is "drain":
            effect = dex_data.Condition({"id":id, "name":"Drain", "effectType": "Recoil"})
        else:
            effect = dex_data.Condition({"id":id, "name":id, "exists":False})
        self.effectCache[id] = effect
        return effect
        

    def getFormat(self, battle, name, isTrusted = False):
        self.battle = battle
        if (name and type(name) != str):
            print("getFormat name type is not str, is ", type(name))
            return name
        
        name = (name or "").strip(' ')
        id = toID(name)
        print("getformat id =", id)
        if (DEFAULT_MOD + id) in self.data()["Formats"]:
            id = DEFAULT_MOD + id

        supplementaryAttributes = None
        # if namelincludes("@@@") @@@が付くことを想定していないので未実装　＠＠＠って何に使う？
        print(id)
        # tmp = self.data()["Formats"]
        # print(self.data()["Formats"])
        # pprint.pprint(self.data()["Formats"], width=100)
        # print(tmp)
        # pprint.pprint(tmp, width=100)

        if id in self.data()["Formats"]:
            print("in")
            print(self.data()["Formats"][id])
            effect = dex_data.Format({"name":name}, **self.data()["Formats"][id])
        else:
            print("not")
            effect = dex_data.Format({"id":id, "name":name, "exists":False})
        # input()
        return effect

    def getItem(self, name):
        if name and type(name) is not str:
            return name
        
        name = (name or "").strip(' ')
        id = toID(name)
        item = self.itemCache[id]
        if item:
            return item
        if id in self.data()["Aliases"]:
            if item["exists"]:
                self.itemCache[id] = item
            return item
        if id and not self.data()["Items"][id] and self.data()["Items"][id + "berry"]:
            item = self.getItem(id + "berry")
            self.itemCache[id] = item
            return item

        if id and id (self.data()["Items"]):
            item = dex_data.Item({"name":name}, self.data()["Items"][id])
            if item.gen > self.gen:
                item.isNonstandard = "Future"
            
            if self.currentMod is "letsgo" and not item.isNonstandard and not item.megaStone:
                item.isNonstandard = "Past"
        else:
            item = dex_data.Item({"id":id, "name":name, "exist":False})
        
        if item.exists:
            self.itemCache[id] = item

        return item

    def getAbility(self, namo = ""):
        if namge and type(name) is not str:
            return name
        
        id = toID(name)
        ability = self.abillityCache[id]
        if ability:
            return ability
        if id in self.data()["Aliases"]:
            ability = self.getAbility(getattr(self.data()["Aliases"],id))
            if ability.exists:
                self.abillityCache[id] = ability
            return ability
        
        if id and id in self.data()["Abilities"]:
            ability = dex_data.Ability({"name":name}, getattr(self.data()["Abilities"], id))
            if ability.gen > self.gen:
                ability.isNonstandard = "Future"
            if self.currentMod is "letsgo" and ability.id is not "noability":
                ability.isNonstandard = "Past"
            if (self.currentMod is "letsgo" or self.gen <= 2) and ability.id is "noability":
                ability.isNonstandard　= None
        else:
            ability = dex_data.Ability({"id":id,"name":name,"exists":False})
        
        if ability.exists:
            self.abillityCache[id] = ability
        return ability

        




    def deepClone(self, obj):
        if obj == None or type(obj) is not object: return obj
        if type(obj) is list:[self.deepClone(x) for x in obj]
        clone = copy.deepcopy(obj)
        for key in dir(obj):
            temp = getattr(obj, key)
            setattr(clone, key, copy.deepcopy(temp))
        return clone

    def loadDataFile(self, basePath, dataType):
        #try:
        FILE_PATH = basePath + DATA_FILES[dataType]+".json"
        # print("FILE PATH", FILE_PATH)

        if not os.path.isfile(FILE_PATH):return None
        with open(FILE_PATH,'r',encoding="utf-8_sig") as f:
            df = json.load(f)
        return df
        

    def includeMods(self): # completed
        if (not self.isBase): raise Exception("This must be called on the base Dex")
        if (self.modsLoaded): return self

        for MOD in os.listdir(MODS_DIR):
            DEXES[MOD] = ModdedDex(MOD, True)
        self.modsLoaded = True

        return self

    def includeData(self, battle):
        self.battle = battle
        self.loadData()
        return self

    def loadData(self):
        if self.dataCache : return self.dataCache
        DEXES['base'].includeMods()
        DATA_CACHE = {}

        BASE_PATH = self.dataDir() + '/'

        # SCRIPTS = 
        self.parentMod = "" if self.isBase else "base"
        if (self.parentMod):
            parentDex = DEXES[self.parentMod]
        else:
            parentDex = ""
        DATA_TYPES.append("Aliases")
        for DATA_TYPE in DATA_TYPES:
            # print(DATA_TYPE)
            if (DATA_TYPE == "Natures" and self.isBase):
                DATA_CACHE[DATA_TYPE] = NATURES
                continue

            if (DATA_TYPE == "Scripts"):
                print(BASE_PATH, self.dataDir())
                import_module_name = self.dataDir()[2:]
                import_module_name =  import_module_name.replace("/", ".")
                script_module = import_module(import_module_name + ".scripts")
                DATA_CACHE[DATA_TYPE] = script_module.Scripts(self.battle)


            BATTLE_DATA = self.loadDataFile(BASE_PATH, DATA_TYPE)
            # print(BATTLE_DATA)
            if BATTLE_DATA == None:continue
            if DATA_TYPE == "Formats" and parentDex=="":
                # print(type(BATTLE_DATA[DATA_TYPE]))
                # print(type(self.formats()))
                BATTLE_DATA[DATA_TYPE].update(self.formats())
            if DATA_TYPE in DATA_CACHE:
                if BATTLE_DATA != DATA_CACHE[DATA_TYPE]:
                    DATA_CACHE[DATA_TYPE].update(BATTLE_DATA[DATA_TYPE])
            else:
                DATA_CACHE[DATA_TYPE] = BATTLE_DATA[DATA_TYPE]
            # ここでFormatsをBATTLE_DATAに追加しているが必要なさそう
        
        # print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
        # pprint.pprint(DATA_CACHE, width=100)

        self.dataCache = DATA_CACHE

        return self.dataCache

    def includeFormats(self):
        print("includeFormats")
        if not self.isBase :print("This should only be run on the base mod")
        self.includeMods()
        if self.formatsCache: return self

        if not self.formatsCache : self.formatsCache = {}
        FILE_PATH = FORMATS + "formats.json"
        if not os.path.isfile(FILE_PATH):
            print("file not found :" + FILE_PATH)
            return None
        with open(FILE_PATH,'r',encoding="utf-8_sig") as f:
            Formats = json.load(f)
        
        column = 1
        # print(Formats)
        for i, formatl in enumerate(Formats["Formats"]):
            # print(formatl, type(formatl))
            # for k in formatl:
            #     print(k)
            if 'name' in formatl:
                fid = toID(formatl['name'])
                # print(fid)
            if "section" in formatl : section = formatl["section"]
            if "column" in formatl : column = formatl["column"]
            if "name" not in formatl and "section" in formatl : continue
            if not fid:
                print("Format"+ str(i + 1) + "must have a name with alphanumeric characters, not " + formatl["name"])
            if "section" not in formatl : formatl["section"] = section
            if "column" not in formatl : formatl["column"] = column
            if fid in self.formatsCache : 
                print("Format" + str(i+1) + "has a duplicate ID: " + fid)
            formatl["effectType"] = "Format"
            formatl["baseRuleset"] = formatl["ruleset"] if "ruleset" in formatl else []
            if "challengeShow" not in formatl:
                formatl["challengeShow"] = True
            if "challengeShow" in formatl:
                if formatl["challengeShow"] == None:
                    formatl["challengeShow"] = True
            if "serchShow" not in formatl:
                formatl["serchShow"] = True
            if "serchShow" in formatl:
                if formatl["serchShow"] == None:
                    formatl["serchShow"] = True
            if "tournamentShow" not in formatl:
                formatl["tournamentShow"] = True
            if "tournamentShow" in formatl:
                if formatl["tournamentShow"] == None:
                    formatl["tournamentShow"] = True
            if "mod" not in formatl:
                formatl["mod"] = "gen8"
            if "mod" in formatl:
                if formatl["mod"] == None:
                    formatl["mod"] = gen8
                if formatl["mod"] not in DEXES:
                    print("Format" + formatl["name"] + " requires noneexistent mod: " + formatl["mod"])
            self.formatsCache[fid] = formatl
            
            print("------")

        return self





DEXES['base'] = ModdedDex("base",True)

Dex = DEXES['base']

