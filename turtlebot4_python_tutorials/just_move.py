import sys
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class AutoTwistPublisher(Node):
    def __init__(self):
        super().__init__('auto_twist_publisher')
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.publish_twist)  # Call publish_twist every 0.1 seconds
        self.speed = 0.5
        self.turn = 1.0

    def publish_twist(self):
        twist = Twist()
        twist.linear.x = self.speed
        twist.angular.z = self.turn
        self.publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    auto_twist_publisher = AutoTwistPublisher()
    rclpy.spin(auto_twist_publisher)
    auto_twist_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()