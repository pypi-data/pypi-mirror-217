import socket
import random
import sys
import time
from pieraknet.protocol_info import ProtocolInfo
from pieraknet.packets.offline_ping import OfflinePing
from pieraknet.handlers.offline_ping import OfflinePingHandler
from pieraknet.packets.open_connection_request_1 import OpenConnectionRequest1
from pieraknet.handlers.open_connection_request_1 import OpenConnectionRequest1Handler
from pieraknet.packets.open_connection_request_2 import OpenConnectionRequest2
from pieraknet.handlers.open_connection_request_2 import OpenConnectionRequest2Handler


class Server:
    def __init__(self, hostname='0.0.0.0', port='19132'):
        self.hostname = hostname
        self.port = port
        self.ipv = 4
        self.name = ''
        self.protocol_version = 11
        self.guid = random.randint(0, sys.maxsize - 1)
        self.connections = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.SOL_UDP)
        self.start_time = int(time.time() * 1000)
        self.maxsize = 4096
        self.magic = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'
        self.running = True
    
    def get_time_ms(self):
        return int(time.time() * 1000) - self.start_time
    
    def send(self, data, address: tuple):
        if not (data is bytes):
            data = str(data)
            data = data.encode()
        self.socket.sendto(data, address)

    def start(self):
        self.socket.bind((self.hostname, self.port))
        while self.running:
            data, client = self.socket.recvfrom(self.maxsize)
            if data[0] in [ProtocolInfo.OFFLINE_PING, ProtocolInfo.OFFLINE_PING_OPEN_CONNECTIONS]:
                packet: OfflinePing = OfflinePing(data)
                OfflinePingHandler.handle(packet, self, client)
            elif data[0] == ProtocolInfo.OPEN_CONNECTION_REQUEST_1:
                packet: OpenConnectionRequest1 = OpenConnectionRequest1(data)
                OpenConnectionRequest1Handler.handle(packet, self, client)
            elif data[0] == ProtocolInfo.OPEN_CONNECTION_REQUEST_2:
                packet: OpenConnectionRequest2 = OpenConnectionRequest2(data)
                OpenConnectionRequest2Handler.handle(packet, self, client)

    def stop(self):
        self.running = False
        self.socket.close()
