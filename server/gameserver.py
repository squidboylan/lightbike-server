from game.game import Game
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import binascii
import os

# SERVER PROTOCOL
# CREATE <GAME_SIZE>
# AUTHACK <USERNAME> <TOKEN>
# START <GAME_WIDTH> <GAME_HEIGHT> <POS_X> <POS_Y> <DIRECTION>
# UPDATE <GAME_BOARD>
# WINNER <WINNER_NAMES>

# CLIENT PROTOCOL
# AUTH <USERNAME>
# <TOKEN> DIRECTION <DIRECTION>

class GameServer(DatagramProtocol):
    def __init__(self):
        self.token_length = 512/8
        self.curr_game = None

    def datagramReceived(self, data, (host, port)):
        print "received %r from %s:%d" % (data, host, port)
        #self.transport.write(data, (host, port))
        self.parse_received_packet(data, (host, port))

    def parse_received_packet(self, data, (host, port)):
        split_data = data.rstrip().split()
        if split_data[0] == "CREATE":
            self.create_game(split_data, (host, port))
        if split_data[0] == "AUTH":
            self.auth(split_data, (host, port))

    def create_game(self, split_data, (host, port)):
        print "Creating game of size " + split_data[1]
        if not self.curr_game:
            self.curr_game = Game(int(split_data[1]))
            send_str = "CREATE SUCCESS\n"
            self.transport.write(send_str, (host, port))
        else:
            # Error 1 is game already exists
            send_str = "CREATE ERROR 1\n"
            self.transport.write(send_str, (host, port))

    def auth(self, split_data, (host, port)):
        print "User authenticating " + split_data[1]
        token = binascii.hexlify(os.urandom(self.token_length))
        self.curr_game.players[split_data[1]] = {}
        self.curr_game.players[split_data[1]]['token'] = token
        self.curr_game.players[split_data[1]]['host'] = host
        self.curr_game.players[split_data[1]]['port'] = port
        send_str = "AUTHACK " + split_data[1] + " " + token + "\n"
        self.transport.write(send_str, (host, port))
