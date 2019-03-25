import soccersimulator as soc
import math

def getAllActions():
	actions = dict()

	moves_classes = Move.__subclasses__()
	tuples = list(map(lambda x : (x.__name__, x), moves_classes))
	moves = {'names' : []}

	for name, move_class in tuples :
		moves["names"].append(name)
		moves[name] = move_class


	shoots_classes = Shoot.__subclasses__()
	tuples = list(map(lambda x : (x.__name__, x), shoots_classes))
	shoots = {'names' : []}

	for name, shoot_class in tuples :
		shoots["names"].append(name)
		shoots[name] = shoot_class


	actions["moves"] = moves
	actions["shoots"] = shoots
	return actions

class Action:
	def __init__(self, name):
		self.name = name
	def computeAction(self, superstate):
		return soc.SoccerAction()

class Move(Action):
	def __init__(self, name):
		Action.__init__(self, name)

class Shoot(Action):
	def __init__(self, name):
		Action.__init__(self, name)

class DontMove(Move):
	def __init__(self):
		Move.__init__(self, "DontMove")

	def computeAction(self, superstate):
		return soc.SoccerAction()

class RunToBall(Move):
	def __init__(self):
		Move.__init__(self, "RunToBall")

	def computeAction(self, superstate):
		return soc.SoccerAction( acceleration = superstate.vect_play_ball)

class RunToPredictBall(Move):
	def __init__(self):
		Move.__init__(self, "RunToPredictBall")
	def computeAction(self, superstate):
		return soc.SoccerAction( acceleration = (superstate.vect_play_ball + superstate.ball_vit * 20 * superstate.coeff_distance) )

class RunToDefensivePos(Move):
	def __init__(self):
		Move.__init__(self, "RunToDefensivePos")
	def computeAction(self, superstate):
		return soc.SoccerAction(acceleration = (superstate.defensive_pos + superstate.ball_pos - superstate.player_pos))

class RunToCloseDefensivePos(Move):
	def __init__(self):
		Move.__init__(self, "RunToDefensivePos")
	def computeAction(self, superstate):
		return soc.SoccerAction(acceleration = (superstate.close_defensive_pos + superstate.ball_pos - superstate.player_pos))
class DontShoot(Shoot):
	def __init__(self):
		Shoot.__init__(self, "DontShoot")

	def computeAction(self, superstate):
		return soc.SoccerAction()

class ShootToGoal(Shoot):
	def __init__(self):
		Shoot.__init__(self, "ShootToGoal")
	def computeAction(self, superstate):
		return soc.SoccerAction( shoot = ((superstate.opp_goal - superstate.player_pos).normalize() * 6) )

class ShootToNearestAlly(Shoot):
	def __init__(self):
		Shoot.__init__(self, "ShootToNearestAlly")
	def computeAction(self, superstate):
		return soc.SoccerAction( shoot = (superstate.nearest_ally.position - superstate.player_pos).normalize() * 6)

class ShootToNearestAllyFarFromOpponent(Shoot):
	def __init__(self):
		Shoot.__init__(self, "ShootAllyFarOpp")
	def computeAction(self, superstate):
		shoot = (superstate.nearest_ally.position - superstate.player_pos).normalize() * 6
		shoot.angle += (math.pi / 12 * math.copysign(1, shoot.angle - (superstate.nearest_opp.position - superstate.player_pos).angle))
		return soc.SoccerAction( shoot = shoot )
			

class ShootToMoveToGoal(Shoot):
	def __init__(self):
		Shoot.__init__(self, "ShootToMove")
	def computeAction(self,superstate):
		return soc.SoccerAction(shoot = (superstate.opp_goal - superstate.player_pos).normalize() * 1.5)
	
class StrongShootToGoal(Shoot):
	def __init__(self):
		Shoot.__init__(self, "StrongShootToGoal")
	def computeAction(self,superstate):
		if (superstate.player_pos.distance(superstate.ball_pos) < 20):
			coeff = (40 - (superstate.player_pos - superstate.ball_pos).norm)/20 * 3
		else : coeff = 3
		return soc.SoccerAction(shoot = ((superstate.opp_goal - superstate.player_pos).normalize() * coeff))

class ShootToCornerFarFromOpp(Shoot):
	def __init__(self):
		Shoot.__init__(self, "ShootToCorner")
	def computeAction(self,superstate):
		shoot = (superstate.ally_corner_far_opp_near_player - superstate.player_pos).normalize() * 4
		return soc.SoccerAction( shoot = shoot)

if __name__ == "__main__":
	print(getAllActions())