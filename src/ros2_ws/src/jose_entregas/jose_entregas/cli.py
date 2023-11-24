#! /usr/bin/env python3

import re
import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped
from tf_transformations import quaternion_from_euler

def create_pose_stamped( pos_x, pos_y, rot_z,nav):
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

def main():
    rclpy.init()
    nav = BasicNavigator()
    q_x, q_y, q_z, q_w = quaternion_from_euler(0.0, 0.0, 0.0)
    initial_pose = PoseStamped()
    initial_pose.header.frame_id = 'map'
    initial_pose.header.stamp = nav.get_clock().now().to_msg()
    initial_pose.pose.position.x = 0.0
    initial_pose.pose.position.y = 0.0
    initial_pose.pose.position.z = 0.0
    initial_pose.pose.orientation.x = q_x
    initial_pose.pose.orientation.y = q_y
    initial_pose.pose.orientation.z = q_z
    initial_pose.pose.orientation.w = q_w

    nav.setInitialPose(initial_pose)
    nav.waitUntilNav2Active()

    while True:
        
        input_text = input("Enter a command: ")
        positions = getCoordinates(input_text)
        if input_text == "exit":
            break
        if positions is None:
            print("Invalid command")
            continue
        
        goal_pose = create_pose_stamped(positions[0], positions[1], 0.0,nav)
        nav.goToPose(goal_pose)
        
        while not nav.isTaskComplete():
            # print(nav.getFeedback())
            # print(nav.get_clock().now().to_msg().sec)
            pass
        nav.get_logger().info('reached  point ' + str(positions))

    rclpy.shutdown()

if __name__ == '__main__':
    main()
