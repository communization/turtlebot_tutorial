import numpy as np
import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32

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
        self.button_subscriber = self.create_subscription(Int32,"number_topic", self.number_callback, 10)
        self.speed=0
        #self.timer = self.create_timer(0.1, self.publish_twist)
        #self.activate() ##
        #########
        
    def number_callback(self, msg): #button노드에서 넘겨받게된다.
        number = msg.data
        # 받은 숫자를 처리하는 로직 작성
        print("Received number:", number)
        self.speed=number
        
    def image_callback(self, msg):
        # Convert the ROS Image message to a numpy array with CvBridge
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        # Now you have a cv2 (OpenCV) image and you can process it as you like
        # For instance, you can display it
        cv2.imshow("Image window", cv_image)
        self.publish_twist()
        cv2.waitKey(3)  # You need this to actually display the image

    def publish_twist(self):
        #print("run_0.05")
        msg = Twist()
        msg.linear.x = self.speed*0.1
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