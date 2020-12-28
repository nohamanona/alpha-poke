
class Scripts:
    def __init__(self, battle):
        self.gen = 8
        self.battle = battle

    def runMove(self, moveOrMoveName, pokemon, targetLoc, sourceEffect, zMove, externalMove, maxMove, originalTarget):
        print("scripts > runMove")
        pokemon.activeMoveActions += 1
        target = self.battle.getTarget(pokemon, maxMove or zMove or moveOrMoveName, targetLoc, originalTarget)
        baseMove = self.battle.dex.getActiveMove(moveOrMoveName)
        pranksterBoosted = baseMove.pranksterBoosted
        if baseMove.id is not "struggle" and not zMove and not maxMove and not externalMove:
            changedMove = self.runEvent('OverrideAction', pokemon, target, baseMove)