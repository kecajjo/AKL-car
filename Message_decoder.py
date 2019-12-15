# from queue import Queue
# import constant_values
import struct
import binascii


def decode_single_message(data):
    try:
        a, b, c, d = struct.unpack('bbbH', data)

        if (d == binascii.crc_hqx(struct.pack('bbb', a, b, c), 0)):
            return a, b, c

        else:
            return 0, 0, 0
    except:
        print("smthin fucked up")


def start_decoding(q, orders):
    while 1:
        if not q.empty():
            orders.put(decode_single_message(q.get()))
            # print(orders.get())
