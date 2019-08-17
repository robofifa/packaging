import server
import robot_wheel_speeds_pb2
import json
import paho.mqtt.client as mqtt  # import the client1
import sys
from time import sleep

robot_messages = robot_wheel_speeds_pb2.Robots()


def on_message(client, userdata, message):
    print("message received ", str(message.payload))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)
    if message.topic == "RoboFIFA/packaging":
        print("parsing packaging message...")
        robot_messages.ParseFromString(message.payload)


def main():
    broker_address = "127.0.0.1"
    print("creating new instance")
    client = mqtt.Client("packaging")  # create new instance
    client.on_message = on_message  # attach function to callback
    print("connecting to broker")
    client.connect(broker_address, port=1883)  # connect to broker
    client.loop_start()  # start the loop
    print("Subscribing to topic", "RoboFIFA/packaging")
    client.subscribe("RoboFIFA/packaging")
    client.subscribe("RoboFIFA/feedback/+")
    #
    # try:
    #     with open('robot_wheel_speeds', "rb") as f:
    #         robot_messages.ParseFromString(f.read())
    # except IOError:
    #     print('robot_wheel_speeds' + ": File not found.")

    robot_server = server.Server()
    try:
        while True:
            # print("Publishing message to topic", "RoboFIFA/packaging")
            # client.publish("RoboFIFA/packaging", "OFF")
            robot_server.check_for_request()
            print("connected to " + str(len(robot_server.robot_connections)) + " robots")
            sleep(1)
            while robot_messages.robots:
                robot_message = robot_messages.robots.pop()
                msg = {"left": robot_message.left, "right": robot_message.right}
                msg = json.dumps(msg)
                print(msg)
                robot_server.send_to_robot(robot_message.id, msg)
                client.publish("RoboFIFA/robot0", str(robot_message.left))
    except KeyboardInterrupt:
        pass
    print("closing robot server")
    robot_server.local_socket.close()
    print("stop listening for mqtt messages")
    client.loop_stop()  # stop the loop


if __name__ == '__main__':
    main()
