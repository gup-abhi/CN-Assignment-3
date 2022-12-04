import random

from packet import Packet


def server_program(conn, client_addr, client_port, router_addr, router_port):
    # get the hostname
    # host = socket.gethostname()
    # port = 12344  # initiate port no above 1024
    exp = 0
    ack_counter = 0
    n = 4
    new = 1
    win_start = 0
    win_end = win_start + n - 1
    receiver = ['', '', '', '']
    # server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    # server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    # server_socket.listen(2)
    # conn, address = server_socket.accept()  # accept new connection
    # print("Connection from: ", str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024)
        if not data:
            # if data is not received break
            break

        data = Packet.from_bytes(data)
        print(f"data received ====> {data} :: seq_num ====> {data.seq_num}")
        rec = int(data.seq_num)
        # lim = rec + n - 1
        # count = 0
        flag = 0
        ack = rec

        # randy = random.randint(1, 4)
        if new == 1:  # you received a new frame of a new window
            print("Received Frame -> ", rec)
            receiver[data.seq_num] = data
            # while count != randy:
            #     temp = random.randint(rec, lim)
            #
            #     if temp not in receiver:
            #         print("Received Frame -> ", temp)
            #
            #         count += 1
            #         flag = 1  # Atleast one new frame added in receiver buffer
            #         receiver.append(temp)
            ack = data.seq_num + 1
            # ack_counter += 1
        else:
            print("Received Frame -> ", rec)  # you received a new frame of an old window
            receiver[data.seq_num] = data
            # flag = 1
            # if flag == 1:
            #     for i in range(rec, lim + 1):
            #         if i not in receiver:
            #             ack = i
            #             break
            #         ack = i + 1
            ack = data.seq_num + 1
            # ack_counter += 1

        print("Sending ACK    -> ", ack)  # next expected frame
        print('***************************************************')

        data = str(ack)
        p = Packet(packet_type=0,
                   seq_num=ack,
                   peer_ip_addr=client_addr,
                   peer_port=client_port,
                   payload=data.encode("utf-8"))
        conn.sendto(p.to_bytes(), (router_addr, router_port))  # send data to the client

        if ack > win_end:
            win_start = ack
            win_end = win_start + n - 1
            new = 1  # now receive a new frame of a new window
        else:
            new = 0  # now received a new frame of an old window

        # conn.close()  # close the connection
