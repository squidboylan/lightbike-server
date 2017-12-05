from game.game import Game
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import threading

# SERVER PROTOCOL
# CREATE <GAME_SIZE>
# AUTHACK <USERNAME> <TOKEN>
# UPDATE <GAME_BOARD>
# WINNER <WINNER_NAMES>

# CLIENT PROTOCOL
# AUTH <USERNAME>
# DIRECTION <TOKEN> <DIRECTION>

class GameServer(DatagramProtocol):
    def __init__(self):
        self.curr_game = None

    def datagramReceived(self, data, (host, port)):
        print "received %r from %s:%d" % (data, host, port)
        self.parse_received_packet(data, (host, port))

    def parse_received_packet(self, data, (host, port)):
        split_data = data.rstrip().split()
        if split_data[0] == "CREATE":
            self.create_game(split_data, (host, port))

        elif split_data[0] == "AUTH":
            self.auth(split_data, (host, port))

        elif split_data[0] == "UPDATE":
            self.update(split_data, (host, port))

        elif split_data[0] == "DIRECTION":
            self.update_direction(split_data, (host, port))

    def create_game(self, split_data, (host, port)):
        print "Creating game of size " + split_data[1]
        if int(split_data[1]) <= 1 or int(split_data[1]) > 4:
            # ERROR 2 means invalid game size
            send_str = "CREATE ERROR 2\n"
            self.transport.write(send_str, (host, port))
            return

        if not self.curr_game:
            self.curr_game = Game(int(split_data[1]), self)
            send_str = "CREATE SUCCESS\n"
            self.transport.write(send_str, (host, port))

        else:
            # Error 1 is game already exists
            send_str = "CREATE ERROR 1\n"
            self.transport.write(send_str, (host, port))

    def auth(self, split_data, (host, port)):
        print "User authenticating " + split_data[1]
        send_str = self.curr_game.add_player(split_data, (host, port))
        self.transport.write(send_str, (host, port))
        if len(self.curr_game.players.keys()) == self.curr_game.player_count and send_str.startswith("AUTHACK"):
            self.start_game()

    def update_direction(self, split_data, (host, port)):
        send_str = self.curr_game.update_direction(split_data, (host, port))
        if send_str:
            self.transport.write(send_str, (host, port))

    def start_game(self):
        t1 = threading.Thread(target=self.curr_game.run)
        t1.start()
