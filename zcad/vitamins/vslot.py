from zencad import box


class VSlot20x20:
    def __init__(self, length):
        self.length = length

    def inst(self):
        return box([20, 20, self.length], center=True)


class VSlot20x40:
    def __init__(self, length):
        self.length = length

    def inst(self):
        return box([20, 40, self.length], center=True)
