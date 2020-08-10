# uPy-rosserial
`rosserial` is a method used by ROS in order to establish communication via serial, basically a middleware, mostly used with microcontrollers, which in this case are the ones responsible in some ROS applications for actuators and sensors usage.

This library targets the communication between ROS and uPy with rosserial as middleware.

**Note: All of this library was coded using an ESP32, can't guarantee to work with other boards.**

## Features
- [x] Advertising Topics
- [x] Publishing
- [x] Subscribing
- [ ] Services

**To Do: Implement services usage.**

## Installation
Before using this library you must have ROS installed, as well as rosserial which would be with the following command:

`sudo apt install ros-<version>-rosserial`

In theory every board with the kind of generic `UART` class for ESP32 is capable of using this library, but it must be known exactly which `UART ID` is being used, this means for example, for ESP32 defined pins correspond to TX0 and RX0 for UART0, and so on. In the examples below, UART2 is used.


### Copying source files
In order to use ros node communication, have in mind a python class for each message must be available. this means a dependency of this library is [uPy Genpy](https://github.com/FunPythonEC/uPy-genpy) and [uPy rosserial_msgs](https://github.com/FunPythonEC/uPy-rosserial_msgs), `ugenpy` used to create Python classes for messages from `*.msg` files while `rosserial_msgs` has the `TopicInfo` class for topic negotiation. The folders from `src`  from this current repo and the other two must be copied

I strongly recommend using [rshell](https://github.com/dhylands/rshell).

### Using upip
Now available with upip, could be installed with:
``` python
import upip
upip.install('micropython-rosserial')
```
If `micropython-rosserial` is installed, because of requirementes, `ugenpy` and `TopicInfo` will too.
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

## Classes
### `uros.NodeHandle`
#### Constructor
##### `uros.NodeHandle(serial_id, baudrate)`
Initiates the class which handles the node, advertised topics, publishes and subscribe.
* `serial_id`: corresponds to the UART ID, in case of ESP32, it has 3 UARTS, in the examples UART2 is used.
* `baudrate`: is the baudrate in which the board will communicate.

#### Methods
##### `uros.NodeHandle.publish(topic_name, msg, buffer_size=1024)`
Publishes data to a defined topic, with a defined message class.
* `topic_name`: the topic where the message will be put or published.
* `msg`: the msg class initiated with its slots values defined.
* `buffer_size`: the amount of bytes that will be published as a maximum from this particular topic, 1024 is by default.

##### `uros.NodeHandle.subscribe(topic_name, msgobj, cb, buffer_size=1024)`
Subscribe to a defined topic.
* `topic_name`: same as publish.
* `msgobj`: is the object class, but not instantiated, just the class passed.
* `cb`: must be defined, it is a callback function, with a single argument that corresponds to the inconming message class.
* `buffer_size`: same as publish.
