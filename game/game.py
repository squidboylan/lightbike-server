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
            return send_str

        if len(self.players.keys()) == 0:
            start_x = 0
            start_y = 0
            # DIR RIGHT
            direction = 1

        else if len(self.players.keys()) == 1:
            start_x = game_size_x - 1
            start_y = game_size_y - 1
            # DIR LEFT
            direction = 3

        else:
            self.players[split_data[1]] = {}
            self.players[split_data[1]]['token'] = token
            self.players[split_data[1]]['host'] = host
            self.players[split_data[1]]['port'] = port
            self.players[split_data[1]]['x'] = start_x
            self.players[split_data[1]]['y'] = start_y
            self.players[split_data[1]]['y'] = start_y
            self.players[split_data[1]]['direction'] = direction
            self.players[split_data[1]]['state'] = 1
            send_str = "AUTHACK " + split_data[1] + " " + token + "\n"
            return send_str
            send_str = "AUTHACK " + split_data[1] + " " + token + "\n"
            return send_str

    def run(self):
        for i in range(self.player_count):
            self.advance_player(i)

    def advance_player(self, player_num):
        direction = self.direction
        self.game_board[self.players[player_num]['y']][self.players[player_num]['x']] = "1"
        if direction == 0:
            self.players[player_num]['y'] = self.players[player_num]['y'] - 1
        if direction == 1:
            self.players[player_num]['x'] = self.players[player_num]['x'] + 1
        if direction == 2:
            self.players[player_num]['y'] = self.players[player_num]['y'] + 1
        if direction == 3:
            self.players[player_num]['x'] = self.players[player_num]['x'] - 1
