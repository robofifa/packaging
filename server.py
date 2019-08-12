import socket
import sys
from RobotConnection import *


def print_robot_list(robots):
    print("connected to " + str(len(robots)) + " robots")
    for robot in robots:
        print(str(robot) + ", ")


def create_connection():
    try:
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error:
        import sys
        msg = sys.exc_info()[1]
        print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    try:
        socket1.bind(('', 0xF1FA))
    except socket.error:
        import sys
        msg = sys.exc_info()[1]
        print('Bind failed. Error: ' + str(msg[0]) + ': ' + msg[1])
        sys.exit()
    return socket1


def wait_for_request(sock):
    print('Server listening')
    data, address = sock.recvfrom(1024)

    if not data:
        return

    return RobotConnection(address, data)


def main():
    robots = []
    socket1 = create_connection()
    while True:
        new_robot = wait_for_request(socket1)
        if new_robot in robots:
            robots = [new_robot if new_robot is robot else robot for robot in robots]
        else:
            robots.append(new_robot)
        print_robot_list(robots)


    socket1.close()


if __name__ == '__main__':
    main()
