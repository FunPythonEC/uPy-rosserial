from std_msgs import String
from uros import NodeHandle
import time

def cb(msg):
    print(msg.data)

msgp=String()
msgp.data='ItsMeLuigi'

node=NodeHandle(2,57600)
node.subscribe('chatter', String, cb)

while True:
    node.publish('groop',msgp)
    time.sleep(1)