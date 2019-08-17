import robot_wheel_speeds_pb2

robot_messages = robot_wheel_speeds_pb2.Robots()
robot_message = robot_messages.robots.add()
robot_message.id = 0
robot_message.left = -.5
robot_message.right = .5
# Write the new address book back to disk.
with open('robot_wheel_speeds', "wb") as f:
    f.write(robot_messages.SerializeToString())
