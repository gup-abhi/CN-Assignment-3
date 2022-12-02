import argparse
import ipaddress
import socket
import pickle
from time import sleep

from packet import Packet
from threeWayHandshaking import ThreeWayHandshake


def run_client(router_addr, router_port, server_addr, server_port):
    peer_ip = ipaddress.ip_address(socket.gethostbyname(server_addr))
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # conn.bind
    timeout = 5

    # Three Way Hand Shaking
    conn1 = ThreeWayHandshake()
    # print("before", conn1)
    # conn.connect((server_addr, server_port))
    p = conn1.connection(peer_ip, server_port)

    while conn1.connected is not True:
        conn1 = ThreeWayHandshake(conn1.status, conn1.connected)
        print(f'conn1.connected ====> {conn1.connected}')
        print("Client side packet:", p)

        print(f"Status ====> {conn1.status} :: Connected ====> {conn1.connected}")

        if conn1.connected is True:
            break

        conn.sendto(p.to_bytes(), (router_addr, router_port))

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

        p = conn1.connection(peer_ip, server_port)
        sleep(3)

    print("3-way done.") if conn1.connected is True else print("3-way not done")

    if conn1.connected:
        try:
            msg = "Hello World"
            p = Packet(packet_type=0,
                       seq_num=1,
                       peer_ip_addr=peer_ip,
                       peer_port=server_port,
                       payload=msg.encode("utf-8"))
            conn.sendto(p.to_bytes(), (router_addr, router_port))
            print('Send "{}" to router'.format(msg))

            # Try to receive a response within timeout
            conn.settimeout(timeout)
            print('Waiting for a response')
            response, sender = conn.recvfrom(1024)
            p = Packet.from_bytes(response)
            print('Router: ', sender)
            print('Packet: ', p)
            print('Payload: ' + p.payload.decode("utf-8"))

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
