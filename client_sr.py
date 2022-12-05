import random
from time import sleep

from packet import Packet


def client_program(conn, client_addr, client_port, router_addr, router_port, request, n=4, new=1, win_start=0, receiver=['' for _ in range(4)]):
    n = n
    new = new
    win_start = win_start
    win_end = win_start + n - 1
    receiver = receiver

    # sending request
    data = str(request)
    p = Packet(packet_type=0,
               seq_num=0,
               peer_ip_addr=client_addr,
               peer_port=client_port,
               payload=data.encode("utf-8"))
    conn.sendto(p.to_bytes(), (router_addr, router_port))

    # waiting for ack
    sleep(5)
    # while True:
    # receive data stream. it won't accept data packet greater than 1024 bytes
    data = conn.recv(1024)

    data = Packet.from_bytes(data)
    print(f"data received ====> {data} :: seq_num ====> {data.seq_num} :: payload ====> {data.payload}")
    ack = int(data.seq_num)

        # # randy = random.randint(1, 4)
        # if new == 1:  # you received a new frame of a new window
        #     print("Received Frame -> ", rec)
        #     receiver[data.seq_num] = data
        #     ack = data.seq_num + 1
        # else:
        #     print("Received Frame -> ", rec)  # you received a new frame of an old window
        #     receiver[data.seq_num] = data
        #     ack = data.seq_num + 1
        #
        # if ack == 4:
        #     break

    sleep(5)

    data = conn.recv(1024)

    data = Packet.from_bytes(data)
    print(f"data received ====> {data} :: seq_num ====> {data.seq_num} :: payload ====> {data.payload}")
    ack = int(data.seq_num)
    print(f"Response ====>\n{data.payload.decode()}")

    print("Sending ACK    -> ", ack)  # next expected frame
    print('***************************************************')

    data = str(ack)
    p = Packet(packet_type=0,
               seq_num=ack,
               peer_ip_addr=client_addr,
               peer_port=client_port,
               payload=data.encode("utf-8"))
    conn.sendto(p.to_bytes(), (router_addr, router_port))  # send data to the client

    # if ack > win_end:
    #     win_start = ack
    #     win_end = win_start + n - 1
    #     new = 1  # now receive a new frame of a new window
    # else:
    #     new = 0  # now received a new frame of an old window

