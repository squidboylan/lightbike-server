from game.game import Game
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import binascii
import os

class GameServer(DatagramProtocol):

    def datagramReceived(self, data, (host, port)):
        print "received %r from %s:%d" % (data, host, port)
        #self.transport.write(data, (host, port))
        self.parse_received_packet(data, (host, port))
        self.token_length = 512/8

    def parse_received_packet(self, data, (host, port)):
        split_data = data.rstrip().split()
        if split_data[0] == "CREATE":
            self.create_game(split_data)
        if split_data[0] == "AUTH":
            self.auth(split_data, host, port)

    def create_game(self, split_data):
        print "Creating game of size " + split_data[1]
        self.curr_game = Game(int(split_data[1]))

    def auth(self, split_data, host, port):
        print "User authenticating " + split_data[1]
        token = binascii.hexlify(os.urandom(self.token_length))
        self.curr_game.players[split_data[1]] = {}
        self.curr_game.players[split_data[1]]['token'] = token
        self.curr_game.players[split_data[1]]['host'] = host
        self.curr_game.players[split_data[1]]['port'] = port
        send_str = "AUTHACK " + split_data[1] + " " + token + "\n"
        self.transport.write(send_str, (host, port))
