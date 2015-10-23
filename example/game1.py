from world import World, Scene, Direction
import gameserver
import prompt

class Game1Server(gameserver.GameServer):
	def makeGame(self):
		street = Scene("You are on the street in front of your home.")
		home = Scene("You are at home.")
		home.connect(Direction.North, street)
		return World(home)

if __name__ == "__main__":
	prompt.run(Game1Server)

