import binascii
import os
import math


class Game:
    def __init__(self, player_count):
        self.player_count = player_count
        self.players = {}
        self.token_length = 512/8
        game_size_base = 20
        self.game_size_x = game_size_base * int(math.floor(player_count/2.0))
        self.game_size_y = game_size_base * int(math.floor(player_count/2.0))
        self.game_board = []

        # Generate board
        for i in range(self.game_size_y):
            self.game_board.append([])
            for j in range(self.game_size_x):
                self.game_board[i].append("0")

        # Debugging
        print self.game_board

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
