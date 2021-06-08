#!/usr/bin/env python3

import time
import socket
import datetime
from aircraft import Aircraft
from multiprocessing import Process, Manager
#from guiapp import AircraftVisualizer  # May change this to * later if needed

HOST = 'wallyburger.ddns.net'
PORT = 30003  # Basestation data port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def socket_listening_thread(visible_aircraft):
    """BaseStation Message Listener.

    This function (run as a thread) constantly polls the BaseStation socket and looks for ADS-B messages. It then
    parses them and applies it to the proper aircraft.

    :param visible_aircraft: The master list of all currently visible aircraft
    :type visible_aircraft: managed dictionary
    """
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


def aircraft_cleanup_thread(visible_aircraft, timeout):
    """Aircraft Cleanup Thread

    This function (run as a thread) checks for visible aircraft that have not seen a message in timeout time. This
    function polls the visible aircraft list approx. every 30 seconds

    :param visible_aircraft: The master list of currently visible aircraft
    :type visible_aircraft: managed dictionary
    :param timeout: The time (in seconds) after which an aircraft should be considered "dead" and be removed from
        the list
    :type timeout: int
    """
    while True:
        for ident, aircraft in visible_aircraft.items():
            if time.time() - aircraft.lastMessageRecieved > timeout:
                # print("No longer able to see: ", ident)
                # TODO: Add logging that will log when aircraft can no longer be seen
                visible_aircraft.pop(ident)
        time.sleep(30)  # We will cleanup once every 30 seconds


def setup_piaware_data_stream(visible_aircraft):
    """Setup data stream from PiAware

    This function sets up the socket that connects to the PiAware to receive the BaseStation messages

    :param visible_aircraft: The master list of currently visible aircraft
    :type visible_aircraft: managed dictionary
    :return: The BaseStation listening thread
    """
    sock.connect((HOST, PORT))
    return Process(target=socket_listening_thread, args=(visible_aircraft,))


def parse_message(message, visible_aircraft):
    """Parse basic BaseStation Message

    This function checks for the Aircraft ID and either updates the ADS-B data for the existing aircraft or creates a
    new aircraft with the ADS-B data. It also checks the type of message and splits the data into a message array.

    :param message: The BaseStation Message
    :type message: string
    :param visible_aircraft: The master list of currently visible aircraft
    :type visible_aircraft: managed dictionary
    """

    msg_arr = message.split(',')
    if msg_arr[0] != "MSG":
        pass

    try:
        if msg_arr[4] in visible_aircraft:
            visible_aircraft[msg_arr[4]].update(msg_arr)
        else:
            visible_aircraft[msg_arr[4]] = Aircraft(msg_arr)
    except IndexError:
        print("IndexError: ", msg_arr)


def main():
    man = Manager()
    visible_aircraft = man.dict({})
    data_stream_thread = setup_piaware_data_stream(visible_aircraft)
    data_stream_thread.start()
    cleanup_thread = Process(target=aircraft_cleanup_thread, args=(visible_aircraft, 45))
    cleanup_thread.start()

    # AircraftVisualizer().run()
    # TODO: Create GUI Thread
    # TODO: Determine how to kill the program and create cleanup function
    while True:
        print(f"Current Visible Aircraft: {len(visible_aircraft)}", end='\r')
        time.sleep(0.5)  # This is needed to prevent pycharm from being able to end the program


if __name__ == '__main__':
    main()