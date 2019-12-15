import socket
import constant_values

TCP_IP = '192.168.8.102'
TCP_PORT = constant_values.port
BUFFER_SIZE = 8  # Normally 1024, but I want fast response


def start_reciving(q):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, addr = s.accept()
    print('Connection address:', addr)
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        # print(struct.unpack('bbbH', data))
        # q.put(data)
        q.put(data)
    conn.close()
