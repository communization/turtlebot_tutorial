import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class ButtonNode(Node):
    def __init__(self):
        super().__init__("button")
        self.publisher = self.create_publisher(Int32, "number_topic", 10)
        self.get_logger().info("Button node initialized.")

    def publish_number(self, number):
        msg = Int32()
        msg.data = number
        self.get_logger().info(f"Publishing number: {number}")
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ButtonNode()

    while rclpy.ok():
        user_input = input("Enter a number (or 'q' to quit): ")
        if user_input == "q":
            break
        try:
            number = int(user_input)
            node.publish_number(number)
        except ValueError:
            node.get_logger().error("Invalid input! Please enter a valid number.")

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()