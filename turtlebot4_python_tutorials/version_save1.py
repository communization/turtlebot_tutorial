import numpy as np
import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            Image,
            '/oakd/rgb/preview/image_raw',
            self.image_callback,
            10)
        ###############
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.publish_twist)
        self.activate() ##
        #########
        
    def image_callback(self, msg):
        # Convert the ROS Image message to a numpy array with CvBridge
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        # Now you have a cv2 (OpenCV) image and you can process it as you like
        # For instance, you can display it
        cv2.imshow("Image window", cv_image)
        cv2.waitKey(3)  # You need this to actually display the image

    def publish_twist(self):
        print("run_0.2")
        msg = Twist()
        msg.linear.x = 0.2
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0
        self.publisher.publish(msg)

def main(args=None):
    print("as")
    rclpy.init(args=args)

    ##########go#############
    # node = rclpy.create_node('turtlebot_controller')
    # publisher = node.create_publisher(Twist, '/cmd_vel', 0.1)
    # msg = Twist()
    # msg.linear.x = 0.2
    # msg.angular.z = 0.0
    # publisher.publish(msg)
    #####################
    
    image_subscriber = ImageSubscriber()
    
    rclpy.spin(image_subscriber)
    
    image_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()