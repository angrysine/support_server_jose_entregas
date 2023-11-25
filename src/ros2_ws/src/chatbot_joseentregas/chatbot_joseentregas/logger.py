import rclpy
import sys
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovarianceStamped
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy
from rclpy.qos import QoSProfile, QoSReliabilityPolicy

from datetime import datetime
class LogRobot(Node):

    def __init__(self):
        super().__init__('log_robot')
        self.get_logger().info('LogRobot node started')

        amcl_pose_qos = QoSProfile(
          durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
          reliability=QoSReliabilityPolicy.RELIABLE,
          history=QoSHistoryPolicy.KEEP_LAST,
          depth=1)

        self.subscription = self.create_subscription(PoseWithCovarianceStamped,
                                                              'amcl_pose',
                                                              self.listener_callback,
                                                              amcl_pose_qos)
    
    def listener_callback(self, msg):
        current_position = msg.pose.pose.position

        with open('output.txt', 'a') as f:

            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            f.write(f'{now} - My current position is: ({current_position.x}, {current_position.y}, {current_position.z})\n')

            self.get_logger().info(f'My current position is: ({current_position.x}, {current_position.y}, {current_position.z})')
            


    
    def write_on_file(self, text):
        with open('output.txt', 'a') as f:
            f.write(text)

def main(args=None):
    rclpy.init(args=args)
    log_robot = LogRobot()
    rclpy.spin(log_robot)
    log_robot.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()