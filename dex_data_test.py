from sim import dex_data

data = {}
data["id"] = "gen7OU"
data["name"] = "gen7OU"

f = {'name': '[Gen 7] OU', 'threads': ['&bullet; <a href="https://www.smogon.com/dex/sm/tags/ou/">USM OU Banlist</a>', '&bullet; <a href="https://www.smogon.com/forums/posts/8162240/">USM OU Sample Teams</a>', '&bullet; <a href="https://www.smogon.com/forums/threads/3667522/">USM OU Viability Rankings</a>'], 'mod': 'gen7', 'ruleset': ['Standard'], 'banlist': ['Uber', 'Arena Trap', 'Power Construct', 'Shadow Tag', 'Baton Pass'], 'section': 'Past Gens OU', 'column': 3, 'effectType': 'Format', 'baseRuleset': ['Standard'], 'challengeShow': True, 'serchShow': True, 'tournamentShow': True}
g = {"name":"aaa"}
dex_data.BasicEffect(data, **{}, **{})
dex_data.Format(data, **f)