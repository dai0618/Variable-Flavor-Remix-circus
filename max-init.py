from pythonosc import udp_client
from pythonosc.osc_message_builder import OscMessageBuilder

IP = '127.0.0.1'
MAX_PORT = 7400
max_client = udp_client.UDPClient(IP, MAX_PORT)

msg = OscMessageBuilder(address="/startup")
msg.add_arg('start')
max_client.send(msg.build())