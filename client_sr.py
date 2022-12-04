from packet import Packet


def client_program(client_socket, router_addr, router_port, server_addr, server_port):
    n = 4
    win_start = 0
    win_end = win_start + n - 1
    # host = socket.gethostname()  # as both code is running on same pc
    # port = 12344  # socket server port number
    sender = []
    flag = 0 #send whole sender list else 1 means send only win_start frame
    # client_socket = socket.socket()  # instantiate
    # client_socket.connect((host, port))  # connect to the server
    print('Window Size is ', n)
    print('******** Enter "bye" to close connection ***************')
    message = input("Hit any key to start sending frames -> ")  # take input
    while message.lower().strip() != 'bye':
        print("Sending frames...")
        if flag == 0:
            for i in range(n):
                msg = str(win_start)
                p = Packet(packet_type=0,
                           seq_num=i,
                           peer_ip_addr=server_addr,
                           peer_port=server_port,
                           payload=msg.encode("utf-8"))
                sender.append(p)
                print(f"server_addr ====> {server_addr} :: server_port ====> {server_port}")
                client_socket.sendto(p.to_bytes(), (router_addr, router_port))  # send message
            for i in sender:
                print("Frame -> ", i)
        else:
            print("Frame -> ", win_start)

        received_data = client_socket.recv(1024)  # receive NAK
        data = Packet.from_bytes(received_data)

        print(f"data ====> {data} :: type(data) ====> {type(data)}")

        msg = str(data.seq_num)
        ack = int(msg)
        if ack > len(sender):
            win_start = ack
            win_end = win_start + n - 1
            flag = 0         		#send new frame
            for i in range(n):
                sender.pop()
        else:
            win_start = int(msg)
            flag = 1			#send old frame

        print("************************************")
        print(f'Received ACK server: {data}')  # show in terminal

        message = input("Hit any key to start sending frames -> ")  # again take input

        # client_socket.close()  # close the connection