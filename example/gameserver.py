from SimpleWebSocketServer import SimpleWebSocketServer
from prompt import PromptServer

class GameServer(PromptServer):
	def makeCommandProcessor(self):
		return self.makeGame()

	def makeGame(self):
		raise NotImplementedError

