# Prog memory gets 0, 4, 8, C.... n+4 in hex as offset

class Memory:

    def __init__(self):
        self.memory = [{hex(n): '' for n in range(0,4096)}, #Data Segment
                       {hex(n): '' for n in range(4096,8192)}] #Prog Memory
