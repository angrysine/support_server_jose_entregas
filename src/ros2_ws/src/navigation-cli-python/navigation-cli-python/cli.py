import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped
from tf_transformations import quaternion_from_euler
from math import pi

from initial_pose import * 
import re


def create_pose_stamped(navigator, pos_x, pos_y, rot_z):
    q_x, q_y, q_z, q_w = quaternion_from_euler(0.0, 0.0, rot_z)
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = nav.get_clock().now().to_msg()
     
    pose.pose.position.x = pos_x
    pose.pose.position.y = pos_y
    pose.pose.position.z = pos_x
    pose.pose.orientation.x = q_x
    pose.pose.orientation.y = q_y
    pose.pose.orientation.z = q_z
    pose.pose.orientation.w = q_w
    return pose

def getCoordinates(text):
    matches = re.findall(r'[+-]?\d+(?:\.\d+)?', text)
    if len(matches) >= 2:
        first_two_numbers = matches[:2]
        first_two_numbers[0] = float(first_two_numbers[0])
        first_two_numbers[1] = float(first_two_numbers[1])
        return first_two_numbers
    else:
        return None


while True:
    
    input_text = input("Enter a command: ")
    positions = getCoordinates(input_text)
    if input_text == "exit":
        break
    if positions is None:
        print("Invalid command")
        continue

    goal_pose = create_pose_stamped(nav, positions[0], positions[1], 0.0)

    
    

    nav.goToPose(goal_pose)
    while not nav.isTaskComplete():
        # print(nav.getFeedback())
        # print(nav.get_clock().now().to_msg().sec)
        pass
    nav.get_logger().info('reached  point ' + str(positions))

rclpy.shutdown()
