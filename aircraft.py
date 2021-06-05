import sys
import time


class Aircraft:
    def __init__(self, initMessage):
        try:
            self.ident, self.callsign, self.alt, self.groundSpeed, self.track, self.latitude, \
                self.longitude, self.verticalRate, self.squawk, self.isInEmergency, self.isIdent, self.isOnGround = \
                [initMessage[i] for i in (4, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21)]
            self.lastMessageRecieved = time.time()
        except IndexError:
            print("indexerror message type:", initMessage[1])
            print("message length:", len(initMessage))

    def assign_field(self, ind, field):
        if ind < 10 or ind == 18 or ind > 21:
            pass  # We don't care about this info. Also should never be more than 21.
        elif ind == 10:
            self.callsign = field
        elif ind == 11:
            self.alt = field
        elif ind == 12:
            self.groundSpeed = field
        elif ind == 13:
            self.track = field
        elif ind == 14:
            self.latitude = field
        elif ind == 15:
            self.longitude = field
        elif ind == 16:
            self.verticalRate = field
        elif ind == 17:
            self.squawk = field
        elif ind == 19:
            self.isInEmergency = field
        elif ind == 20:
            self.isIdent = field
        elif ind == 21:
            self.isOnGround = field
        else:
            pass  # Should not be possible

    def update(self, msg):
        # TODO: don't bother looping through the first portion of the list
        self.lastMessageRecieved = time.time()
        if msg[4] != self.ident:
            print("ERROR: Aircraft identities mixed up! Information no longer accurate!", file=sys.stderr)
            pass
        for ind, field in enumerate(msg):
            if field != '':
                self.assign_field(ind, field)
