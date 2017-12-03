import binascii
import os
import math
import time

class Game:
    def __init__(self, player_count, server_obj):
        self.server_obj = server_obj
        self.player_count = player_count
        self.players = {}
        self.token_length = 512/8
        game_size_base = 20
        #self.game_size_x = game_size_base * int(math.floor(player_count/2.0))
        #self.game_size_y = game_size_base * int(math.floor(player_count/2.0))
        self.game_size_x = game_size_base * player_count/2
        self.game_size_y = game_size_base * player_count/2
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
        if len(self.players.keys()) == 0:
            start_x = 0
            start_y = 0
            # DIR RIGHT
            direction = "RIGHT"

        elif len(self.players.keys()) == 1:
            start_x = self.game_size_x - 1
            start_y = self.game_size_y - 1
            # DIR LEFT
            direction = "LEFT"

        if len(self.players.keys()) >= self.player_count:
            # AUTHFAIL 1 means game full
            send_str = "AUTHFAIL 1\n"
            return send_str

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

    def run(self):
        while 1:
            alive = []
            for i in self.players.keys():
                if self.players[i]['state'] == 1:
                    alive.append(i)

            for i in self.players.keys():
                self.advance_player(i)

            self.check_collision()

            for i in self.players.keys():
                tmp_board = map(list, self.game_board)
                for j in self.players.keys():
                    if self.players[j]['state'] == 1:
                        if j == i:
                            tmp_board[self.players[j]['y']][self.players[j]['x']] = 'P'
                        else:
                            tmp_board[self.players[j]['y']][self.players[j]['x']] = 'E'

                send_str = "UPDATE "
                for j in range(self.game_size_y):
                    send_str = send_str + ''.join(tmp_board[j])
                    send_str = send_str + "\n"

                host = self.players[i]['host']
                port = self.players[i]['port']
                self.server_obj.transport.write(send_str, (host, port))

            post_run_alive = []
            for i in self.players.keys():
                if self.players[i]['state'] == 1:
                    post_run_alive.append(i)

            if len(post_run_alive) == 1:
                send_str = "WINNER " + post_run_alive[0] + "\n"
                for i in self.players.keys():
                    host = self.players[i]['host']
                    port = self.players[i]['port']
                    self.server_obj.transport.write(send_str, (host, port))

                self.server_obj.curr_game = None
                return

            if len(post_run_alive) == 0:
                send_str = "WINNER"
                for j in alive:
                    send_str = send_str + " " + j

                send_str = send_str + "\n"
                for i in self.players.keys():
                    host = self.players[i]['host']
                    port = self.players[i]['port']
                    self.server_obj.transport.write(send_str, (host, port))

                self.server_obj.curr_game = None
                return

            time.sleep(.500)


    def advance_player(self, player_name):
        direction = self.players[player_name]['direction']
        if self.players[player_name]['state'] == 1:
            self.game_board[self.players[player_name]['y']][self.players[player_name]['x']] = "1"
            if direction == "UP":
                self.players[player_name]['y'] = self.players[player_name]['y'] - 1
            elif direction == "RIGHT":
                self.players[player_name]['x'] = self.players[player_name]['x'] + 1
            elif direction == "DOWN":
                self.players[player_name]['y'] = self.players[player_name]['y'] + 1
            elif direction == "LEFT":
                self.players[player_name]['x'] = self.players[player_name]['x'] - 1

    def update_direction(self, split_data, (host, port)):
        player = None
        token = split_data[1]
        direction = split_data[2]

        for i in self.players.keys():
            if self.players[i]['host'] == host and self.players[i]['port'] == port and self.players[i]['token'] == token:
                player = self.players[i]
                break

        if not player:
            send_str = "BAD TOKEN"
            return send_str

        if direction == "RIGHT" and not player['direction'] == "LEFT":
            player['direction'] = direction
        elif direction == "UP" and not player['direction'] == "DOWN":
            player['direction'] = direction
        elif direction == "LEFT" and not player['direction'] == "RIGHT":
            player['direction'] = direction
        elif direction == "DOWN" and not player['direction'] == "UP":
            player['direction'] = direction

    def check_collision(self):
        for i in self.players.keys():
            if self.players[i]['state'] == 1:
                x = self.players[i]['x']
                y = self.players[i]['y']
                print i + " x: " + str(x) + ", y: " + str(y)
                if x >= self.game_size_x or x < 0:
                    self.players[i]['state'] = 0
                    continue

                if y >= self.game_size_y or y < 0:
                    self.players[i]['state'] = 0
                    continue

                if self.game_board[y][x] == "1":
                    self.players[i]['state'] = 0

