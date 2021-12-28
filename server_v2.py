from twisted.internet import reactor,endpoints
from twisted.internet.protocol import Protocol, Factory

class ServerCL(Protocol):
    def __init__(self, addr):
        self.addr = addr

    def connectionMade(self):
        a = str(self.addr)
        self.transport.write(b'Server connect\n')
        self.transport.write(a.encode("utf-8")+b'- you addr\n')

    def dataReceived(self, data):
        data = data.decode('UTF-8')
        print(data[:-2])
        self.transport.write(b'data received\n')

class FactoryServerCl(Factory):
    def buildProtocol(self, addr):
        return ServerCL(addr)

endpoints.serverFromString(reactor, 'tcp:8051').listen(FactoryServerCl())
reactor.run()