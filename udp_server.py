import argparse
import socket
import pickle
from time import sleep
import ipaddress

from packet import Packet
from threeWayHandshaking import ThreeWayHandshake
from server_sr import server_program


def run_server(port):
    client_addr = ''
    client_port = 0
    peer_ip = None
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))
    print('Echo server is listening at', port)
    print("waiting for connection")

    # Three Way HandShaking
    # con = (sock.accept()[0])
    # print(f"con - {con}")
    connection = False
    while not connection:
        sleep(3)
        data = sock.recv(4096)
        # print(f"Sender - {sender}")
        print(f"Data - {data}")

        packetData = Packet.from_bytes(data)
        str_obj = packetData.payload.decode()

        print(f"packetData - {packetData} :: packetData.peer_ip_addr - {packetData.peer_ip_addr} "
              f":: packetData.peer_port - {packetData.peer_port}")

        client_addr = packetData.peer_ip_addr
        client_port = packetData.peer_port
        peer_ip = ipaddress.ip_address(socket.gethostbyname(str(client_addr)))

        del data

        print(f"str_obj ====> {str_obj}")
        print(f"Status ===> {str_obj[str_obj.find(': ') + 2: str_obj.find(',')]}")
        print(f"Connected status ===> {str_obj[str_obj.find('established: ') + 13: str_obj.find('.')]}")

        conn1 = ThreeWayHandshake(str_obj[str_obj.find(': ') + 2: str_obj.find(',')], str_obj[str_obj.find('established: ') + 13: str_obj.find('.')])
        p = conn1.connection(packetData.peer_ip_addr, packetData.peer_port)
        address = ('127.0.0.1', 3000)

        print(f"conn1.connected ====> {conn1.connected}")

        if conn1.connected is True:
            print(f"conn1.connected ====> {conn1.connected}")
            connection = True
            break

        sock.sendto(p.to_bytes(), address)

        # print(f"packetData.payload - {packetData.payload.decode()}")
        # connection = pickle.load(packetData.payload).connected
    print("3-way done!!!")

    if connection:
        try:
            # while True:
            #     data, sender = sock.recvfrom(1024)
            #     handle_client(sock, data, sender)
            server_program(sock, peer_ip, client_port, '127.0.0.1', 3000)

        finally:
            sock.close()
            run_server(8007)


def handle_client(conn, data, sender):
    try:
        p = Packet.from_bytes(data)
        print("Router: ", sender)
        print("Packet: ", p)
        print("Payload: ", p.payload.decode("utf-8"))

        # How to send a reply.
        # The peer address of the packet p is the address of the client already.
        # We will send the same payload of p. Thus we can re-use either `data` or `p`.
        conn.sendto(p.to_bytes(), sender)

    except Exception as e:
        print("Error: ", e)


# Usage python udp_server.py [--port port-number]
parser = argparse.ArgumentParser()
parser.add_argument("--port", help="echo server port", type=int, default=8007)
args = parser.parse_args()
run_server(args.port)
