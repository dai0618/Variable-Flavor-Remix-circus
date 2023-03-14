from pythonosc import udp_client
from pythonosc.osc_message_builder import OscMessageBuilder


def send_osc(content, ip, port, address):
    # UDPのクライアントを作る
    client = udp_client.UDPClient(ip, port)

    # 送信するメッセージを作って送信する eg. address = '/loops'
    msg = OscMessageBuilder(address=address)
    msg.add_arg(content)
    m = msg.build()

    client.send(m)


def send_stems(ip, port):
    client = udp_client.UDPClient(ip, port)

    for stem in ['bass', 'drums', 'other', 'vocals']:
        msg = OscMessageBuilder(address=f"/1/{stem}")
        msg.add_arg(f"/Users/dai/Desktop/project/vfr-performance-reciever-main-icc/reciever/tmp/separated_loops_stem/{stem}/{stem}_天体観測.wav")
        m = msg.build()

        client.send(m)


if __name__ == '__main__':
    # send_osc('hello',
    #          '127.0.0.1',
    #          7400,
    #          '/1/b')

    send_stems('127.0.0.1', 7400)
