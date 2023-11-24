import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class LogRobot(Node):

    def __init__(self):
        super().__init__('log_robot')
        self.get_logger().info('LogRobot node started')
        self._subscriptions = self.create_subscription(String, 'topic', self.listener_callback, 10)
    
    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
    
    def write_on_file(self, text):
        with open('output.txt', 'a') as f:
            f.write(text)