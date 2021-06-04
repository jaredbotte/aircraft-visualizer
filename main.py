#!/usr/bin/env python3

import socket
from aircraft import Aircraft
#from guiapp import AircraftVisualizer  # May change this to * later if needed

HOST = '192.168.0.47'  # Local IP address of the PiAware
PORT = 30003  # Basestation data port


def setup_piaware_data_stream():
    return socket.create_connection((HOST, PORT))


def parse_msg(msg_arr, visible_aircraft):
    print(msg_arr[4])
    if msg_arr[4] in visible_aircraft:
        visible_aircraft[msg_arr[4]].update(msg_arr)
    else:
        visible_aircraft[msg_arr[4]] = Aircraft(msg_arr)


def parse_message(message, visible_aircraft):
    message_arr = message.split(b',')
    if message_arr[0] == b'MSG':
        parse_msg(message_arr, visible_aircraft)
    else:
        pass


if __name__ == '__main__':
    datasocket = setup_piaware_data_stream()
    datasocket.setblocking(False)
    visible_aircraft = {}
    #AircraftVisualizer().run()
    while True:
        try:
            for data in datasocket.recv(4096).split(b'\n'):
                parse_message(data, visible_aircraft)
                print(len(visible_aircraft))
                # Clean old aircraft
        except socket.error as e:
            if str(e) == "[Errno 35] Resource temporarily unavailable":
                continue
            else:
                datasocket.close()
