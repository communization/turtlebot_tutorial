from irobot_create_msgs.msg import InterfaceButtons, LightringLeds

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
import sys



class TurtleBot4FirstNode(Node):
    def __init__(self):
        super().__init__('turtlebot4_first_python_node')

class TurtleBot4FirstNode(Node):
    lights_on_ = False

    def __init__(self):
        super().__init__('turtlebot4_first_python_node')
        print("a")
        # Subscribe to the /interface_buttons topic
        self.interface_buttons_subscriber = self.create_subscription(
            InterfaceButtons,
            '/interface_buttons',
            self.interface_buttons_callback,
            qos_profile_sensor_data)
        # Create a publisher for the /cmd_lightring topic
        self.lightring_publisher = self.create_publisher(
            LightringLeds,
            '/cmd_lightring',
            qos_profile_sensor_data)
    def button_1_function(self):
        # Create a ROS 2 message
        lightring_msg = LightringLeds()
        # Stamp the message with the current time
        lightring_msg.header.stamp = self.get_clock().now().to_msg()

        # Override system lights
        lightring_msg.override_system = True

        # LED 0
        lightring_msg.leds[0].red = 255
        lightring_msg.leds[0].blue = 0
        lightring_msg.leds[0].green = 0

        # LED 1
        lightring_msg.leds[1].red = 0
        lightring_msg.leds[1].blue = 255
        lightring_msg.leds[1].green = 0

        # LED 2
        lightring_msg.leds[2].red = 0
        lightring_msg.leds[2].blue = 0
        lightring_msg.leds[2].green = 255

        # LED 3
        lightring_msg.leds[3].red = 255
        lightring_msg.leds[3].blue = 255
        lightring_msg.leds[3].green = 0

        # LED 4
        lightring_msg.leds[4].red = 255
        lightring_msg.leds[4].blue = 0
        lightring_msg.leds[4].green = 255

        # LED 5
        lightring_msg.leds[5].red = 0
        lightring_msg.leds[5].blue = 255
        lightring_msg.leds[5].green = 255

        # Publish the message
        self.lightring_publisher.publish(lightring_msg)
    # Interface buttons subscription callback
    def interface_buttons_callback(self, create3_buttons_msg: InterfaceButtons):
        #self.get_logger().info('Received an InterfaceButtons message')
        if create3_buttons_msg.button_2.is_pressed:
            self.get_logger().info('Button 2 Pressed!')
            self.button_1_function()
def main(args=None):
    print('Hi from turtlebot4_python_tutorials.')
    #args = sys.argv
    rclpy.init(args=args)
    node = TurtleBot4FirstNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
