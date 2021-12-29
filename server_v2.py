from twisted.internet import reactor,endpoints, defer
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver

class ServerCL(LineReceiver):
    def __init__(self,users):
        self.users = users

    def connectionMade(self):
        self.transport.write(b'Server connect\n')
        self.transport.write(b'write you name\n')


    def dataReceived(self, data):
        self.users.update({(data.decode("UTF-8"))[:-2]:self})
        self.transport.write(b'data received\n')
        print(self.users)

class FactoryServerCl(ServerFactory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return ServerCL(self.users)

endpoints.serverFromString(reactor, 'tcp:8051').listen(FactoryServerCl())
reactor.run()