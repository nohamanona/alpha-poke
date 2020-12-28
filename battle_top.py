from sim import battle

options_bob = {"name":"Bob", "team":"Rattata |Rattata ||Run Away|Tackle,Tail Whip|Serious|,,,,,||31,31,31,31,31,31||50|"}
options_alice = {"name":"Alice", "team":"Rattata |Rattata ||Run Away|Tackle,Tail Whip|Serious|,,,,,||31,31,31,31,31,31||50|"}

print("cleate Battle class")
Battle = battle.Battle({'formatid':'gen7OU'})
print("Battle_top : setPlayer P1")
Battle.setPlayer("p1",options_bob)
print("Battle_top : setPlayer P2")
Battle.setPlayer("p2",options_alice)
