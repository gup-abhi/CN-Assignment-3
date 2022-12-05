import argparse
import ipaddress
import socket
import pickle
from time import sleep

from packet import Packet
from threeWayHandshaking import ThreeWayHandshake
from client_sr import client_program
from get import get_data


def run_client(router_addr, router_port, server_addr, server_port):
    peer_ip = ipaddress.ip_address(socket.gethostbyname(server_addr))
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # conn.bind
    timeout = 5

    # Three Way Hand Shaking
    conn1 = ThreeWayHandshake()
    # print("before", conn1)
    # conn.connect((server_addr, server_port))
    # p = conn1.connection(peer_ip, server_port)

    while conn1.connected is not True:
        # conn1 = ThreeWayHandshake(conn1.status, conn1.connected)
        p = conn1.connection(peer_ip, server_port)

        print(f'conn1.connected ====> {conn1.connected}')
        print("Client side packet:", p)

        print(f"Status ====> {conn1.status} :: Connected ====> {conn1.connected}")

        # if conn1.status == 'ack':
        #     conn1.connected = True
        #     break

        conn.sendto(p.to_bytes(), (router_addr, router_port))

        if conn1.status == 'ack':
            conn1.connected = True
            break

        del conn1

        data = conn.recv(4096)
        # print(f"Data received ====> {data}")

        sleep(1)
        recvp = Packet.from_bytes(data)

        del data
        # print("Response from server ====> ", recvp)

        print(f"Response payload ====> {recvp.payload.decode()}")

        str_obj = recvp.payload.decode()

        status = str_obj[str_obj.find(': ') + 2: str_obj.find(',')]
        connected = str_obj[str_obj.find('established: ') + 13: str_obj.find('.')]

        conn1 = ThreeWayHandshake(status, connected)

        sleep(3)

    print(f"conn1.connected ====> {conn1.connected}")
    print("3-way done.") if conn1.connected is True else print("3-way not done")

    if conn1.connected:
        try:
            print("Send request")
            request = input("Enter the request to be sent to the server: ")

            print(f"request ====> {request}")
            # client_program(conn, router_addr, router_port, peer_ip, server_port)
            client_program(conn, peer_ip, server_port, router_addr, router_port, request)

        except socket.timeout:
            print('No response after {}s'.format(timeout))
        finally:
            conn.close()


# Usage:
# python echoclient.py --routerhost localhost --routerport 3000 --serverhost localhost --serverport 8007

parser = argparse.ArgumentParser()
parser.add_argument("--routerhost", help="router host", default="localhost")
parser.add_argument("--routerport", help="router port", type=int, default=3000)

parser.add_argument("--serverhost", help="server host", default="localhost")
parser.add_argument("--serverport", help="server port", type=int, default=8007)

args = parser.parse_args()

run_client(args.routerhost, args.routerport, args.serverhost, args.serverport)
