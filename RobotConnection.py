

class RobotConnection:
    def __init__(self, address=("", 0x0), robot_id=-1):
        self.address = address
        self.id = robot_id

    def __str__(self):
        return "ID:" + str(self.id) + " IP:" + str(self.address)

    def __eq__(self, other):
        return self.id == other.id
