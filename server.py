from RobotConnection import *
from time import sleep
import json
import warnings

class Server:
    """
    maintains connections with active robots
    """
    def __init__(self):
        warnings.simplefilter('always', UserWarning)
        try:
            self.local_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.local_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.local_socket.settimeout(1.0)
            self.local_socket.bind(('', 0xF1FA))
        except socket.error as e:
            print('Failed to create socket. Error Code : ' + str(e))
            raise e
        self.robot_connections = []
        self.connected_robot_ids = set()

    def check_for_request(self):
        """
        check whether a new robot is requesting messages
        :return:
        """
        try:
            data, address = self.local_socket.recvfrom(1024)
        except socket.timeout:
            print("nothing received")
            return
        robot_id = decode_message(data)
        new_robot = RobotConnection(address, robot_id)
        self.add_new_robot(new_robot)

    def add_new_robot(self, new_robot):
        """
        safely adds a new robot connection
        :param new_robot:
        :return: None
        """
        if new_robot in self.robot_connections:
            self.robot_connections = [new_robot if new_robot is robot else robot for robot in self.robot_connections]
            warnings.warn("reconnected to: %s" % str(new_robot))
        else:
            self.robot_connections.append(new_robot)
            self.connected_robot_ids.add(new_robot.id)
            print("new connection: %s" % str(new_robot))

    def send_to_robot(self, robot_id, msg):
        """
        Try to send the message to the robot with the given robot_id
        :param robot_id: id of the robot to send to
        :param msg: message to send
        :return: True if message was successfully sent
        """
        success = False
        for robot in self.robot_connections:
            if robot_id is robot.id:
                if robot.send(self.local_socket, msg):
                    success = True
        return success


def decode_message(data):
    """
    decodes messages coming from a robot
    :param data: received raw string
    :return: tuple containing data from the message
    """
    try:
        data_dict = json.loads(data)
        robot_id = data_dict['id']
    except json.decoder.JSONDecodeError:
        print("unreadable data received: " + str(data))
        return
    return robot_id


def main():
    server = Server()
    while True:
        server.check_for_request()
        print("connected to " + str(len(server.robot_connections)) + " robots")
        sleep(1)
        for robot_id in range(10):
            server.send_to_robot(robot_id, "go fast " + str(robot_id))
    server.local_socket.close()


if __name__ == '__main__':
    main()
