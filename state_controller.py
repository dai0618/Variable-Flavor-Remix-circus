"""
Open Sound Control Server/Client and callback function design example.

2022-11-11
Atsuya Kobayashi
"""
import os
import threading
from typing import Any, Callable, Dict, List, Optional, Union

from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

import time

from pathlib import Path

from sound_source_separation import separate_loops
from loop_move_osc import move_loop

track_list = []
wait_track_list = []
track_counter = 0
wait_track_counter = 0

class OSCServer:
    def __init__(self, ip: str, port: int) -> None:
        # addresses
        self.address_first = "/get_song"
        self.address_second = "/selected_loops"
        self.address_third = "/track_move"
        # callback functions
        self.on_received_first: Optional[Callable] = None
        self.on_received_second: Optional[Callable] = None
        self.on_received_third: Optional[Callable] = None
        self.server: Optional[BlockingOSCUDPServer] = None
        self.ip = ip
        self.port = port

    def parse_message(self, input_args: str) -> List[str]:
        if type(input_args) == float:
            args = [input_args]
        else:
            args: List[str] = input_args.split(" ")
        return args

    def run(self, single_thread=False) -> None:
        """Start OSC server on main or sub thread.

        Args:
            single_thread (bool, optional): Defaults to False.
        """
        self.dispatcher = Dispatcher()

        if self.on_received_first:
            self.dispatcher.map(self.address_first,
                                self.on_received_first)  # type: ignore
        # NOTE: 受け付けるアドレスを増やしたい場合は以下のようにしてアドレスを増やす
        if self.on_received_second:
            self.dispatcher.map(self.address_second,
                                self.on_received_second)  # type: ignore
        if self.on_received_third:
            self.dispatcher.map(self.address_third,
                                self.on_received_third)  # type: ignore

        self.server = BlockingOSCUDPServer(
            (self.ip, self.port), self.dispatcher)
        print(f"Serving on {self.server.server_address}")
        if single_thread:
            self.server.serve_forever()
        else:
            # running the server on new thread
            server_thread = threading.Thread(target=self.server.serve_forever)
            server_thread.start()

    def stop(self):
        if self.server is not None:
            self.server.shutdown()

    def __del__(self):
        if self.server is not None:
            self.server.shutdown()


class OSCSender:
    def __init__(self, ip: str, port: int) -> None:
        self.client = udp_client.SimpleUDPClient(ip, port)
        # NOTE: 一つのSenderに付き送れるホストは一つ。
        self.ip = ip
        self.port = port

    def send(self, path: str, msg: Any) -> None:
        assert path[0] == "/", "given osc address path is incorrect"
        print(f"sending OSC message",
              f"(type={type(msg)})",
              f"to {self.ip}:{self.port}:{path}")
        self.client.send_message(path, msg)

    def __del__(self):
        if self.client is not None:
            del self.client


def get_sample_callback(
    sender: OSCSender,
    keyword: str = "",
    # given_path: str = ""
) -> Callable:
    """Callback関数を返す関数

    Args:
        sender (OSCSender): 受信時にオウム返しをするのでClientのインスタンスが必要
        keyword (str, optional): hoge/fuga/piyo 等のアドレスのときどうするかみたいな.

    Returns:
        Callable: 関数を返す
    """

    # NOTE: もし機械学習モデル等を読む場合は、`get_sample_callback`の引数でパスを受け取り
    # ここでインスタンスの読み込みを行うことで、毎回の呼び出しでの読み込みなどが発生せずに済む
    # 例) model = Model.load_model(given_path)

    def callback_func(addr: str, *args: Any):
        global track_list, track_counter, wait_track_counter
        """Actual callback function: 実際にOSCを受け取って呼ばれる関数

        Args:
            addr (str): OSCのパス (e.g. /path/to)
            args (Any): 可変長引数なのでTupleとして扱うこと
        """
        print("received:", addr, args)

        if addr == "/get_song":
            print(f"曲名を取得 : {args[0]}")
            track_title = str(args[0])
            track_counter += 1

            if track_counter <= 8:
                track_list.append(track_title)
                loops_max_addr = f"/select_loops/{track_counter}"
                current_dir = Path.cwd()
                loop_path = str(current_dir.joinpath(f"tmp/loops/{track_list[track_counter-1]}/{track_list[track_counter-1]}.wav"))
                print(loop_path)
                sender.send(loops_max_addr, loop_path)

                artworks_max_addr = f"/select_artworks/{track_counter}"
                artwork_path = str(current_dir.joinpath(f"tmp/artworks/{track_list[track_counter-1]}.jpeg"))
                sender.send(artworks_max_addr, artwork_path)
                
                titles_max_addr = f"/select_titles/{track_counter}"
                sender.send(titles_max_addr, track_list[track_counter-1])

                separate_loops(track_title)

            else:
                wait_track_list.append(track_title)

        elif addr == "/selected_loops":
            print(f"取得した数字 : {args[0]}")
            try:
                selected_num = int(args[0])
                separate_track = track_list[selected_num-1]

                print(wait_track_counter)
                print(wait_track_list)

                track_list[selected_num-1] = wait_track_list[wait_track_counter]
                to_max_addr = f"/select_loops/{selected_num}"
                current_dir = Path.cwd()
                loop_path = str(current_dir.joinpath(f"tmp/loops/{track_list[selected_num-1]}/{track_list[selected_num-1]}.wav"))
                sender.send(to_max_addr, loop_path)

                artworks_max_addr = f"/select_artworks/{selected_num}"
                artwork_path = str(current_dir.joinpath(f"tmp/artworks/{track_list[selected_num-1]}.jpeg"))
                sender.send(artworks_max_addr, artwork_path)

                titles_max_addr = f"/select_titles/{selected_num}"
                sender.send(titles_max_addr, track_list[selected_num-1])

                separate_loops(separate_track)

                wait_track_counter += 1

            except:
                print("out of range or failed sound source separation")
                
        elif addr == "/track_move":
            print(f"曲の移動 : {args[0]}")
            move_track = str(args[0])
            move_loop(move_track)

    return callback_func


if __name__ == "__main__":
    server = OSCServer("127.0.0.1", 9999)
    sender = OSCSender("127.0.0.1", 8888)
    server.on_received_first = get_sample_callback(sender)
    server.on_received_second = get_sample_callback(sender)
    server.on_received_third = get_sample_callback(sender)
    server.run(single_thread=True)