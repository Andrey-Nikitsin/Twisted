from twisted.internet import reactor,endpoints, defer
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver


class ServerCL(LineReceiver):
    def __init__(self, users, addr):
        self.user_info = addr
        self.users = users
    schet = 0
    def connectionMade(self):
        self.transport.write(b'Server connect\n')
        self.transport.write(b'inter you name\n')
        self.users.update({self : ''})
        print(self.users)

    def dataReceived(self, data):
        def SaveNameUser(NameUser):
            for key in self.users.keys():
                if key == self:
                    self.users.pop(self)
                    self.users.update({self:(NameUser[:-2],self.user_info)})
                    print(self.users)
                    break

        def GeneralChat(messange):
            print(messange)
            for key in self.users.keys():
                if key != self:
                    name = self.users.get(self)[0]
                    key.transport.write(name)
                    key.transport.write(b':\t')
                    key.transport.write(messange)

        for key in self.users.keys():
            if len(self.users.get(key)) == 0:
                SaveNameUser(data)
                break
            elif len(self.users.get(self)) > 0:
                self.schet+=1
                print(self.schet)
                if self.schet==len(self.users):
                    GeneralChat(data)
                    self.schet=0




class FactoryServerCl(ServerFactory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return ServerCL(self.users, addr)


if __name__ == '__main__':
    endpoints.serverFromString(reactor, 'tcp:8052').listen(FactoryServerCl())
    reactor.run()