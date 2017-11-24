#!/usr/bin/env python

import sys
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from server.gameserver import GameServer


try:
    port = int(sys.argv[1])
except:
    port = 9999

reactor.listenUDP(port, GameServer())
reactor.run()
