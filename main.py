import server
import robot_wheel_speeds_pb2
import sys
from time import sleep


def main():
    robot_messages = robot_wheel_speeds_pb2.Robots()
    try:
        with open('robot_wheel_speeds', "rb") as f:
            robot_messages.ParseFromString(f.read())
    except IOError:
        print('robot_wheel_speeds' + ": File not found.")

    robot_server = server.Server()
    while True:
        robot_server.check_for_request()
        print("connected to " + str(len(robot_server.robot_connections)) + " robots")
        sleep(1)
        for robot_message in robot_messages.robots:
            msg = str(robot_message.left) + str(robot_message.right)
            print(msg)
            robot_server.send_to_robot(robot_message.id, msg)
    robot_server.local_socket.close()


if __name__ == '__main__':
    main()
