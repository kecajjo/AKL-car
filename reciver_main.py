from queue import Queue
from threading import Thread
import Udp_reciver
import Message_decoder
import send_orders

# import constant_values

q = Queue(maxsize=20)
orders = Queue(maxsize=20)

reciver = Thread(target=Udp_reciver.start_reciving, args=(q, ))
reciver.start()
decoder = Thread(target=Message_decoder.start_decoding, args=(
    q,
    orders,
))
decoder.start()
send_orders = Thread(target=send_orders.start_sending_orders, args=(orders, ))
send_orders.start()