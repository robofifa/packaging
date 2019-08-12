import socket


class RobotConnection:
    def __init__(self, address=("", 0x0), robot_id=-1):
        self.address = address
        self.id = robot_id

    def __str__(self):
        return "ID:" + str(self.id) + " IP:" + str(self.address)

    def __eq__(self, other):
        return self.id == other.id

    def send(self, local_socket, msg):
        bytes_to_send = str.encode(msg)
        print("sending '" + str(bytes_to_send) + "' to " + str(self.address))
        local_socket.sendto(bytes_to_send, self.address)
        # self.UDPClientSocket.sendto(bytes_to_send, self.address)
