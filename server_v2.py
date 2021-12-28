from twisted.internet import reactor,endpoints
from twisted.internet.protocol import Protocol, Factory

class ServerCL(Protocol):
    def connectionMade(self):
        self.transport.write(b'Server connect\n')

    def dataReceived(self, data):
        data = data.decode('UTF-8')
        print(data[:-2])
        self.transport.write(b'data received\n')

class FactoryServerCl(Factory):
    def buildProtocol(self, addr):
        return ServerCL()

endpoints.serverFromString(reactor, 'tcp:8051').listen(FactoryServerCl())
reactor.run()