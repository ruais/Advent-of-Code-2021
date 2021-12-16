# advent of code day 16 by Ruma (Lynn)

from collections import deque

class BITSPacket:
    def __init__(self, packet):
        self.length = 0

        if isinstance(packet, deque):
            self.data = packet
        else:
            self.data = deque()
            for char in packet:
                n = int(char, 16)
                cursor = 8
                while cursor:
                    self.data.append(1 if cursor & n else 0)
                    cursor >>= 1

        self.ver = self.clip(3)
        self.typeID = self.clip(3)

        if self.typeID == 4:
            self.value = self.literal()
            self.sub = ()

        else:
            self.value = 0

            if not self.clip(1):
                sublength = (0, self.clip(15))
            else:
                sublength = (1, self.clip(11))

            sub = []
            lengthcheck = lambda: ((0, sum(map(len, sub))), (1, len(sub)))
            while all(sublength != l for l in lengthcheck()):
                sub.append(BITSPacket(self.data))
                self.length += sub[-1].length

            self.sub = tuple(sub)

        del self.data

    def __repr__(self):
        return f'BITSPacket v{self.ver}: {self.typeID} -- {self.value}'

    def __len__(self):
        return self.length

    def __int__(self):
        func = (int.__add__, int.__mul__, min, max, None,
                int.__gt__, int.__lt__, int.__eq__)
        if self.typeID == 4:
            return self.value
        else:
            n = int(self.sub[0])
            for sub in self.sub[1:]:
                n = func[self.typeID](n, int(sub))
            return int(n)

    def clip(self, cliplength):
        clip = 0
        while cliplength > 0:
            clip = (clip << 1) + self.data.popleft()
            self.length += 1
            cliplength -= 1

        return clip

    def literal(self):
        literal = 0

        incomplete = True
        while incomplete:
            incomplete, val = divmod(self.clip(5), 16)
            literal = (literal << 4) + val

        return literal

def init():
    with open(r'.\input\day16.txt') as file:
        data = file.read()

    return data.strip('\n')

def solveA():
    packet = init()

    def vernum(packet):
        vernums = (packet.ver,)
        for sub in packet.sub:
            vernums += vernum(sub)

        return vernums

    return sum(vernum(BITSPacket(packet)))

def solveB():
    packet = init()

    return int(BITSPacket(packet))
