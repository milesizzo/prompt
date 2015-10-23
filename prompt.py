import json
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer

clients = set()
authenticated = set()
class PromptServer(WebSocket):
	def handleMessage(self):
		print "%s: %s" % (self.formatAddress(), self.data)
		data = self.processor.processCommand(self.data)
		if data is None:
			data = "Invalid command: \"%s\"" % self.data
		print "%s replying" % self.formatAddress()
		self.sendMessage(unicode(data))
	
	def handleConnected(self):
		clients.add(self)
		self.processor = self.makeCommandProcessor()
		print "%s connected (%d total)" % (self.formatAddress(), len(clients))

	def handleClose(self):
		clients.discard(self)
		authenticated.discard(self)
		self.processor = None
		print "%s disconnected (%d still connected)" % (self.formatAddress(), len(clients))

	def formatAddress(self):
		return "[%s:%d]" % self.address

	def makeCommandProcessor(self):
		raise NotImplementedError

	def printState(self):
		print 'clients connected:'
		for client in clients:
			print client.formatAddress()

def run(serverType):
	port = 5167
	print "Starting server (port %d)" % port
	server = SimpleWebSocketServer('', port, serverType)
	server.serveforever()

