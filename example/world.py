from commands import CommandProcessor

def enum(**enums):
	return type('Enum', (), enums)

Direction = enum(North=1, East=2, South=3, West=4)

class World(CommandProcessor):
	def __init__(self, scene):
		self.scene = scene
		self.time = 0

	def processCommand(self, command):
		result = self.scene.processCommand(command)
		if isinstance(result, tuple):
			scene, result = result
			self.scene = scene
		return result

class Scene:
	def __init__(self, description):
		self.description = description
		self.directions = {Direction.North: None, Direction.East: None, Direction.South: None, Direction.West: None}

	def connect(self, direction, scene):
		opposite = {
			Direction.North: Direction.South,
			Direction.East: Direction.West,
			Direction.South: Direction.North,
			Direction.West: Direction.East
		}[direction]
		if scene.directions[opposite] is not None:
			raise Exception("Invalid scene placement")
		scene.directions[opposite] = self
		self.directions[direction] = scene

	def walk(self, direction):
		if direction in self.directions:
			return self.directions[direction]
		return None

	def _directionStr(self, direction):
		return {
			Direction.North: "North",
			Direction.East: "East",
			Direction.South: "South",
			Direction.West: "West"
		}[direction]

	def _strDirection(self, directionStr):
		return {
			"north": Direction.North,
			"east": Direction.East,
			"south": Direction.South,
			"west": Direction.West
		}[directionStr]

	def processCommand(self, command):
		if command == "look":
			return self.on_look()
		if command in {"north", "south", "east", "west"}:
			return self.on_move(self._strDirection(command))

	def on_look(self):
		directions = [self._directionStr(key) for key, value in self.directions.iteritems() if value is not None]
		if directions:
			return "%s Directions you can move are: %s" % (self.description, ", ".join(directions))
		return "%s You are stuck!" % self.description

	def on_move(self, direction):
		if self.directions[direction] is None:
			return "You cannot move in that direction."
		scene = self.walk(direction)
		return scene, scene.on_look()

if __name__ == "__main__":
	street = Scene("You are on the street in front of your home.")
	home = Scene("You are at home.")
	home.connect(Direction.North, street)
	world = World(home)
	print world.scene.on_look()
	print street.on_look()

