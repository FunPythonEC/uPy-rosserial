# uros contains NodeHandle which is reponsable to publish and subscribe
import uros
from std_msgs import String  # object string imported
from time import sleep

node = uros.NodeHandle(2, 115200)  # node initialized, for tx2/rx2 and 115200 baudrate
msg = String()  # msg object init
msg.data = "Hola FunPython - Pilas esa cuarentena :v"
while True:
    node.publish("Greet", msg)  # publish data to node
    sleep(1)
