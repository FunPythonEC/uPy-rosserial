# uPy-rosserial
`rosserial` a method used by ROS in order to establish communication via serial , mostly this is used with microcontrollers, which in this case are the ones responsible in some ROS applications for actuators and sensors usage.

Since there is no rosserial package for uPy as there is for Arduino, this repo has been created where every needed script to establish rosserial with uPy will be found.

## Features
- [x] Advertising Topics
- [x] Publishing
- [x] Subscribing
- [ ] Actions
- [ ] Services

**To Do: Subscribing testing and implementation.**

## Installation
Before using this library you must have ROS installed, as well as rosserial which would be with the following command:
`sudo apt install ros-<version>-rosserial`


In theory every board with the kind of generic `UART` class for ESP32 is capable of using this library, but it must be known exactly which `UART ID` is being used, this means for example, for ESP32 defined pins correspond to TX0 and RX0 for UART0, and so on. In the examples below, UART2 is used.

In order to use ros node communication, have in mind a python class for each message must be available. this means a dependency of this library is [uPy Genpy](https://github.com/FunPythonEC/uPy-genpy) and [uPy rosserial_msgs](https://github.com/FunPythonEC/uPy-rosserial_msgs), `ugenpy` used to create Python classes for messages from `*.msg` files while `rosserial_msgs` has the `TopicInfo` class for topic negotiation. Follow the installation from `ugenpy` before proceeding.

Once `ugenpy` and `rosserial_msgs` are inside, the package `uros` from this repository must be copied to the flash memory. I strongly recommend using [rshell](https://github.com/dhylands/rshell).

Now available with upip, could be installed with:
``` python
import upip
upip.install('micropython-rosserial')
```
>Note: must be connected to WiFi to use upip like this.

**Have in mind before publishing or subscribing to a topic, the message class must be generated with `ugenpy`**

## Usage

Everytime before establishing rosserial communication, this command must be run, even before running the script in uPy, will be improved afterwards:

>rosrun rosserial_arduino serial_node.py _port:=/dev/ttyUSB0 _baud:=115200

**Note port and baudrate can be changed, in ESP32 I prefer using 115200 for baudrate.**

### Publish example

Suppose `ColorRGBA.py` has been created using `ugenpy` and `ColorRGBA.msg` file:
```
float32 r
float32 g
float32 b
float32 a
```

And then running the following e.g.:

``` python
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
```

### Subscribe example

```python
import uros
from std_msgs import String

def cb(msg):
	print(msg.data)
	
node = uros.NodeHandle(2, 115200)
node.subscribe('chatter', String, cb)
```

### Mixed example

```python
import uros
from std_msgs import String

def cb(msg):
	print(msg.data)
	
packet=String()
packet.data='hola fpy'
node = uros.NodeHandle(2, 115200)
node.subscribe('chatter', String, cb)
while True:
	node.publish('greet', packet)
```