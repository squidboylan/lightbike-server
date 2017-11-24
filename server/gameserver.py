from game.game import Game
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class GameServer(DatagramProtocol):

    def datagramReceived(self, data, (host, port)):
        print "received %r from %s:%d" % (data, host, port)
        #self.transport.write(data, (host, port))
        self.parse_received_packet(data, (host, port))

    def parse_received_packet(self, data, (host, port)):
        split_data = data.rstrip().split()
        if split_data[0] == "CREATE":
            self.create_game(split_data)

    def create_game(self, split_data):
        print "Creating game of size " + split_data[1]
        self.curr_game = Game(int(split_data[1]))
