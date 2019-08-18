import robot_wheel_speeds_pb2
import paho.mqtt.client as mqtt  # import the client1

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
    try:
        while True:
            while robot_messages.robots:
                robot_message = robot_messages.robots.pop()
                client.publish("RoboFIFA/robot0", str(robot_message.left))
    except KeyboardInterrupt:
        pass
    print("closing robot server")
    print("stop listening for mqtt messages")
    client.loop_stop()  # stop the loop


if __name__ == '__main__':
    main()
