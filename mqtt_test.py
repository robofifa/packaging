import paho.mqtt.client as mqtt  # import the client1
import time
import robot_wheel_speeds_pb2


def on_message(client, userdata, message):
    # print("message received ", str(message.payload.decode("utf-8")))
    print("message received ", str(message.payload))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


# broker_address = "192.168.1.184"
# broker_address = "test.mosquitto.org"
broker_address = "127.0.0.1"
print("creating new instance")
client = mqtt.Client("P1")  # create new instance
client.on_message = on_message  # attach function to callback
print("connecting to broker")
client.connect(broker_address, port=1883)  # connect to broker
client.loop_start()  # start the loop
print("Subscribing to topic", "RoboFIFA/packaging")
client.subscribe("RoboFIFA/packaging")
print("Publishing message to topic", "RoboFIFA/packaging")

robot_messages = robot_wheel_speeds_pb2.Robots()
robot_message = robot_messages.robots.add()
robot_message.id = 0
robot_message.left = -.5
robot_message.right = .5

client.publish("RoboFIFA/packaging", robot_messages.SerializeToString())
client.publish("RoboFIFA/robot0", "some test message for robot0")
time.sleep(4)  # wait
client.loop_stop()  # stop the loop
