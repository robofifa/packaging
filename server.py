from RobotConnection import *
from time import sleep


def create_connection():
    try:
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket1.settimeout(1.0)
    except socket.error as e:
        print('Failed to create socket. Error Code : ' + str(e))
        raise e

    try:
        socket1.bind(('', 0xF1FA))
    except socket.error as e:
        print('Bind failed.. Error Code : ' + str(e))
        raise e

    return socket1


def wait_for_request(sock):
    print('Server listening')
    try:
        data, address = sock.recvfrom(1024)
    except socket.timeout:
        print("nothing received")
        return None

    return RobotConnection(address, data)


def main():
    robots = []
    socket1 = create_connection()
    while True:
        new_robot = wait_for_request(socket1)
        if new_robot is not None:
            if new_robot in robots:
                robots = [new_robot if new_robot is robot else robot for robot in robots]
            else:
                robots.append(new_robot)
        print("connected to " + str(len(robots)) + " robots")
        sleep(0.1)
        for robot in robots:
            print(str(robot) + ", ")
            robot.send(socket1, "go fast")

    socket1.close()


if __name__ == '__main__':
    main()
