import uros
from std_msgs import ColorRGBA #message object ColorRGBA
from time import sleep
node=uros.NodeHandle(2,115200) #node initialized, for tx2/rx2 and 115200 baudrate
msg=ColorRGBA() #msg object init
msg.r=1 #values to variables assigned
msg.g=3
msg.b=4
msg.a=1
while True:
    node.publish('Colorsh',msg) #publish data to node Colorsh
    sleep(1)