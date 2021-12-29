from twisted.internet import reactor,endpoints, defer
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver

class ServerCL(LineReceiver):
    def __init__(self, users, addr):
        self.user_info = addr
        self.users = users


    def connectionMade(self):
        self.transport.write(b'Server connect\n')
        self.transport.write(b'inter you name\n')
        self.users.update({self : self.user_info})
        print(self.users)

    def dataReceived(self, data):
        data = data.decode("UTF-8")
        def SaveNameUser(NameUser):
            for key in self.users.keys():
                if key == NameUser[:-2]:
                    print(NameUser[:-2])
                    self.transport.write(b'this name taken, write you name\n')
                    return 'repeat'
                else:
                    self.users.pop(self)
                    self.users.update({NameUser[:-2]:self.user_info})
                    break
                    return 'OK'

        if self in self.users.keys():
            while SaveNameUser(data) == 'repeat':
                SaveNameUser(data)
        print(self.users)

class FactoryServerCl(ServerFactory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return ServerCL(self.users, addr)

endpoints.serverFromString(reactor, 'tcp:8051').listen(FactoryServerCl())
reactor.run()