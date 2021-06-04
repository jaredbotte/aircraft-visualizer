#!/usr/bin/env python3

import socket
import time

from aircraft import Aircraft
from multiprocessing import Process, Manager
#from guiapp import AircraftVisualizer  # May change this to * later if needed

HOST = '192.168.0.47'  # Local IP address of the PiAware
PORT = 30003  # Basestation data port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def socket_listening_thread(visible_aircraft):
    while True:
        try:
            messages = sock.recvfrom(4096)[0].decode("utf-8").split('\n')
            for message in messages:
                parse_message(message, visible_aircraft)
        except socket.error as e:
            if str(e) == "[Errno 35] Resource temporarily unavaliable":
                continue
            else:
                print(str(e))
                sock.close()


def setup_piaware_data_stream(visible_aircraft):
    sock.connect((HOST, PORT))
    # TODO: Wait for connection (ignore Errno 36?). Look at non blocking socket issues.
    return Process(target=socket_listening_thread, args=(visible_aircraft,))


def parse_msg(msg_arr, visible_aircraft):
    if msg_arr[4] in visible_aircraft:
        visible_aircraft[msg_arr[4]].update(msg_arr)
    else:
        visible_aircraft[msg_arr[4]] = Aircraft(msg_arr)


def parse_message(message, visible_aircraft):
    message_arr = message.split(',')
    if message_arr[0] == "MSG":
        parse_msg(message_arr, visible_aircraft)
    else:
        pass


def main():
    man = Manager()
    visible_aircraft = man.dict({})
    data_stream_thread = setup_piaware_data_stream(visible_aircraft)
    data_stream_thread.start()

    # AircraftVisualizer().run()
    # TODO: Create Cleanup Thread to remove old aircraft
    # TODO: Create GUI Thread
    # TODO: Determine how to kill the program and create cleanup function
    while True:
        print(f"Current Visible Aircraft: {len(visible_aircraft)}", end='\r')
        time.sleep(0.5)  # This is needed to prevent pycharm from being able to end the program


if __name__ == '__main__':
    main()