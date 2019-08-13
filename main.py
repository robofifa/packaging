import server
import robot_wheel_speeds_pb2
import sys
from time import sleep


def main():
    robot_messages = robot_wheel_speeds_pb2.Robots()
    try:
        with open('robot_wheel_speeds', "rb") as f:
            robot_messages.ParseFromString(f.read())

        robots = []
        socket1 = server.create_connection()
        while True:
            new_robot = server.wait_for_request(socket1)
            if new_robot is not None:
                if new_robot in robots:
                    robots = [new_robot if new_robot is robot else robot for robot in robots]
                else:
                    robots.append(new_robot)
            print("connected to " + str(len(robots)) + " robots")
            sleep(0.1)
            for robot_message in robot_messages.robots:
                for robot in robots:
                    if robot_message.id is robot.id:
                        print(str(robot) + ", ")
                        robot.send(socket1, str(robot_message.left) + str(robot_message.right))
    except IOError:
        print('robot_wheel_speeds' + ": File not found.")


if __name__ == '__main__':
    main()
