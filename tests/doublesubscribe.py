from std_msgs import String
from uros import NodeHandle
import time

def cb(msg):
    print(msg.data)

node=NodeHandle(2,57600)
node.subscribe('chatter', String, cb)
node.subscribe('greet', String, cb)