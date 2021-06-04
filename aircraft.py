import sys


class Aircraft:
    def __init__(self, initMessage):
        self.ident, self.lastMessageRecieved, self.callsign, self.alt, self.groundSpeed, self.track, self.latitude, \
        self.longitude, self.verticalRate, self.squawk, self.isInEmergency, self.isIdent, self.isOnGround = \
            [initMessage[i] for i in (4, 7, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21)]


    def assign_field(self, ind, field):
        if ind < 7 or ind in (8, 9, 18) or ind > 21:
            pass  # We don't care about this info. Also should never be more than 21.
        elif ind == 7:
            self.lastMessageRecieved = field
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
        if(msg[4] != self.ident):
            print("ERROR: Aircraft identities mixed up! Information no longer accurate!", file=sys.stderr)
            pass
        for ind, field in enumerate(msg):
            if field != b'':
                self.assign_field(ind, field)