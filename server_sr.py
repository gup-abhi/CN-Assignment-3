from packet import Packet
from time import sleep

from get import get_data
from post import post_data

def server_program(client_socket, server_addr, server_port, router_addr, router_port, n=4, win_start=0, sender=[], flag=0):
    n = n
    win_start = win_start
    win_end = win_start + n - 1

    sender = sender
    # send whole sender list else 1 means send only win_start frame
    flag = flag

    sleep(5)
    received_data = client_socket.recv(1024)  # receive NAK
    data = Packet.from_bytes(received_data)
    print(f"data ====> {data} :: type(data) ====> {type(data)}")

    msg = str(data.seq_num)
    ack = int(msg)

    p = Packet(packet_type=0,
               seq_num=ack,
               peer_ip_addr=server_addr,
               peer_port=server_port,
               payload=msg.encode("utf-8"))
    sender.append(p)
    print(f"server_addr ====> {server_addr} :: server_port ====> {server_port}")
    client_socket.sendto(p.to_bytes(), (router_addr, router_port))  # send message

    request = str(data.payload.decode())
    if request.split(" ")[0] == 'get':
        response = get_data(request)
    else:
        response = post_data(request)

    print(f"response - {response}")

    msg = str(response)
    p = Packet(packet_type=0,
               seq_num=1,
               peer_ip_addr=server_addr,
               peer_port=server_port,
               payload=msg.encode("utf-8"))
    sender.append(p)
    print(f"server_addr ====> {server_addr} :: server_port ====> {server_port}")
    client_socket.sendto(p.to_bytes(), (router_addr, router_port))  # send message

    sleep(5)
    received_data = client_socket.recv(1024)  # receive NAK
    data = Packet.from_bytes(received_data)
    print(f"data ====> {data} :: type(data) ====> {type(data)}")

    msg = str(data.seq_num)
    ack = int(msg)

    print(f"ack - {ack}")

    # sleep(30)
    return


    # print('Window Size is ', n)
    # print('******** Enter "bye" to close connection ***************')

    # while message.lower().strip() != 'bye':
    # print("Sending frames...")
    # if flag == 0:
    #     for i in range(n):
    #         msg = str(win_start)
    #         p = Packet(packet_type=0,
    #                    seq_num=i,
    #                    peer_ip_addr=server_addr,
    #                    peer_port=server_port,
    #                    payload=msg.encode("utf-8"))
    #         sender.append(p)
    #         print(f"server_addr ====> {server_addr} :: server_port ====> {server_port}")
    #         client_socket.sendto(p.to_bytes(), (router_addr, router_port))  # send message
    #     for i in sender:
    #         print("Frame -> ", i)
    # else:
    #     print("Frame -> ", win_start)
    #
    # ack = 0
    # counter = 0
    #
    # while True:
    #     received_data = client_socket.recv(1024)  # receive NAK
    #
    #     data = Packet.from_bytes(received_data)
    #
    #     print(f"data ====> {data} :: type(data) ====> {type(data)}")
    #
    #     msg = str(data.seq_num)
    #     ack = int(msg)
    #
    #     if ack == 4:
    #         print("Breaking Loop")
    #         break
    #     else:
    #         print("Waiting for other frames =====>")
    #         sleep(3)
    #
    #     counter += 1
    #
    #     if counter == 4:
    #         print("Timeout")
    #         break
    #
    # print(f"ack - {ack}")
    #
    # if ack > len(sender):
    #     win_start = ack
    #     win_end = win_start + n - 1
    #     flag = 0  # send new frame
    #     for i in range(n):
    #         sender.pop()
    # else:
    #     win_start = int(msg)
    #     flag = 1  # send old frame
    #     server_program(client_socket, router_addr, router_port, server_addr, server_port, 4, win_start, sender, flag)
    #
    # print("************************************")
    # print(f'Received ACK server: {data}')  # show in terminal