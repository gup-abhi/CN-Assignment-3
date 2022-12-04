# status 1. sync from user
# sync recv 2.ack-sync from server
# sync rec 3.ack from user then data

from packet import Packet
import pickle


def create_packet(socket_type, seq_num, peer_ip_addr, peer_port, data):
    p = Packet(packet_type=socket_type,
               seq_num=seq_num,
               peer_ip_addr=peer_ip_addr,
               peer_port=peer_port,
               payload=str(data).encode('utf-8'))

    return p


class ThreeWayHandshake:

    def __init__(self, status=None, connected=False):

        self.status = status
        self.connected = connected

    def connection(self, peer_ip_addr, peer_port):
        if self.status is None:
            print("starting 3-way handshake", "status: sync", sep="\n")
            self.status = "sync"
            return create_packet(0, 1, peer_ip_addr, peer_port, self)
        elif self.status == "sync":
            print("sync received", "sending status: ack-sync", sep="\n")
            self.status = "ack-sync"
            return create_packet(0, 1, peer_ip_addr, peer_port, self)
        elif self.status == "ack-sync":
            print("ack-sync received", "sending status: ack", sep="\n")
            self.status = "ack"
            return create_packet(0, 1, peer_ip_addr, peer_port, self)
        elif self.status == "ack":
            self.connected = True
            print("Connected.")

    # def connected(self):
    #     return self.connected

    def reset(self):
        self.status = None
        self.connected = False

    def __str__(self):
        return f"status: {self.status}, connection established: {self.connected}."