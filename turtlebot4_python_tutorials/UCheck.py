import numpy as np
import cv2
import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32

import sys
sys.path.append('/home/lee/ros2_ws/src/turtlebot4_python_tutorials/turtlebot4_python_tutorials/')
sys.path.append('/home/ros2_ws/src/turtlebot4_python_tutorials/turtlebot4_python_tutorials/')
import torch 
from UNet import UNet
from Deeplab_resnet import DeepLabv3_plus
import torchvision.transforms as transforms
from PIL import Image as PILImage

class UCheck(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.bridge = CvBridge()
        # self.subscription = self.create_subscription(
        #     Image,
        #     '/oakd/rgb/preview/image_raw',
        #     self.image_UNET,
        #     10)
        self.subscription = self.create_subscription(
            CompressedImage,
            '/oakd/rgb/image_raw/compressed',
            self.image_UNET,
            10)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.model_path = "/home/ros2_ws/src/turtlebot4_python_tutorials/turtlebot4_python_tutorials/pth_/BEST_Water_real_floor_4_epoch0_server.pth"
        print("pth: ",self.model_path)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        #self.model = UNet(3,3).to(self.device)
        self.model = DeepLabv3_plus(nInputChannels=3, n_classes=2, os=16, pretrained=True, _print=True).to(self.device)
        self.model.load_state_dict(torch.load(self.model_path, map_location=torch.device('cpu')))
        self.model.eval()
        
    def preprocess_image(self, image):
        transform = transforms.Compose([
            transforms.Resize((512,512)),
            transforms.ToTensor(),
        ])
        image_tensor = transform(image).unsqueeze(0)
        return image_tensor
    
    
    def image_UNET(self, msg=CompressedImage()):
        # Convert the ROS Image message to a numpy array with CvBridge
        cv_image = CvBridge().compressed_imgmsg_to_cv2(msg, desired_encoding="bgr8")
        # Now you have a cv2 (OpenCV) image and you can process it as you like
        # For instance, you can display it
        #cv2.imshow("Image window", cv_image)
        print("checkpoint2")
        image = PILImage.fromarray(cv2.cvtColor(cv_image,cv2.COLOR_BGR2RGB))
        image_tensor = self.preprocess_image(image).to(self.device)
        with torch.no_grad():
            output = self.model(image_tensor)
        output_label = output.argmax(dim=1, keepdim=True)
        output_label = output_label.cpu().numpy().squeeze().astype(np.uint8)
        print("\routput_values:",np.unique(output_label),end="")

        #통합
        #output_label_3d = np.stack((output_label,)*3, axis=-1)
        print("output",output_label.shape)
        print("cv_image",cv_image.shape)
        #integrated = cv2.addWeighted(cv_image, 1, output_label*255, 0.5, 0)

        cv2.imshow("output",output_label*255)
        cv2.imshow("original",cv_image.astype(np.uint8))
        #cv2.imshow("integrated",integrated.astype(np.uint8))
        
        #print(np.count_nonzero(output_label==1)) ##
        #print(output_label.shape) #256 x 256
        #print(np.max(output_label))
        cv2.waitKey(1)
        #self.publish_twist() # You need this to actually display the image

    def publish_twist(self):
        #print("run_0.05")
        msg = Twist()
        msg.linear.x = -1.0#self.speed*0.1
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0
        self.publisher.publish(msg) #움직이려면 이거 필ㄷ요

def main(args=None):
    print("as")
    rclpy.init(args=args)

    image_subscriber = UCheck()
    
    rclpy.spin(image_subscriber)
    
    image_subscriber.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    main()