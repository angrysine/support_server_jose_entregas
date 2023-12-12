import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped
from tf_transformations import quaternion_from_euler
from std_msgs.msg import String
import re


class Robot():
    def __init__(self):
        super().__init__('robot_node')
        self._publisher = self.create_publisher(String, 'api_topic', 10)
        self._subscriber = self.create_subscription(
            String,
            'chatbot_topic',
            self.listener_callback,
            10)
        self._logger = self.get_logger()
        self._msg = String()
        self.nav = BasicNavigator()
        q_x, q_y, q_z, q_w = quaternion_from_euler(0.0, 0.0, 0.0)
        initial_pose = PoseStamped()
        initial_pose.header.frame_id = 'map'
        initial_pose.header.stamp = self.nav.get_clock().now().to_msg()
        initial_pose.pose.position.x = 0.0
        initial_pose.pose.position.y = 0.0
        initial_pose.pose.position.z = 0.0
        initial_pose.pose.orientation.x = q_x
        initial_pose.pose.orientation.y = q_y
        initial_pose.pose.orientation.z = q_z
        initial_pose.pose.orientation.w = q_w

        self.nav.setInitialPose(initial_pose)
        self.nav.waitUntilNav2Active()


    def go_to(self):
        goal_pose3 = self._create_pose_stamped(self.nav, 0.0, 0.0, 0.00)
        goal_pose1 = self._create_pose_stamped(self.nav, 2.5, 1.0, 1.57)
        goal_pose2 = self._create_pose_stamped(self.nav, 0.0, 1.0, 1.57)
        waypoints = [goal_pose1, goal_pose2, goal_pose3]
        self.nav.followWaypoints(waypoints)
        while not self.nav.isTaskComplete():
            print(self.nav.getFeedback())



    def _create_pose_stamped(navigator, pos_x, pos_y, rot_z):
        q_x, q_y, q_z, q_w = quaternion_from_euler(0.0, 0.0, rot_z)
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = navigator.get_clock().now().to_msg()
        pose.pose.position.x = pos_x
        pose.pose.position.y = pos_y
        pose.pose.position.z = pos_x
        pose.pose.orientation.x = q_x
        pose.pose.orientation.y = q_y
        pose.pose.orientation.z = q_z
        pose.pose.orientation.w = q_w
        return pose

    def listener_callback(msg,self):
        self._logger.info(f'Robot received: {msg.data}')
        self.go_to()



def main():
    rclpy.init()
    node = Robot()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()





if __name__ == '__main__':
    main()
