import binascii
import os


class Game:
    def __init__(self, player_count):
        self.player_count = player_count
        self.players = {}
        self.token_length = 512/8

    def add_player(self, split_data, (host, port)):
        token = binascii.hexlify(os.urandom(self.token_length))
        if len(self.players.keys()) >= self.player_count:
            # AUTHFAIL 1 means game full
            send_str = "AUTHFAIL 1\n"

        else:
            self.players[split_data[1]] = {}
            self.players[split_data[1]]['token'] = token
            self.players[split_data[1]]['host'] = host
            self.players[split_data[1]]['port'] = port
            send_str = "AUTHACK " + split_data[1] + " " + token + "\n"

        return send_str
