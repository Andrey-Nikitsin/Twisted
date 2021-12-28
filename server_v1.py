from twisted.internet import protocol, reactor, endpoints

class Calculator(protocol.Protocol):

    def connectionMade(self):
        self.transport.write(b'Server connect\n')

    def answer(self, data):
        try:
            eval(data)
            return eval(data)
        except NameError:
            return 'SyntaxError'
        except SyntaxError:
            return 'SyntaxError'

    def dataReceived(self, data):
        data = data.decode('UTF-8')
        quest = self.answer(data[:-2])
        self.transport.write(str.encode(f'{quest}\n','UTF-8'))

class CalculatorFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Calculator()

endpoints.serverFromString(reactor, "tcp:1234").listen(CalculatorFactory())
reactor.run()