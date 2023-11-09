#! /usr/bin/env python3 
import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped
from tf_transformations import quaternion_from_euler
from math import pi

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

rclpy.init()
nav = BasicNavigator()
goal_pose1 = create_pose_stamped(nav, 2.5, 1.0, 1.57)
goal_pose2 = create_pose_stamped(nav, 0.0, 1.0, 1.57)
goal_pose3 = create_pose_stamped(nav, 0.0, 0.0, 0.00)

waypoints = [goal_pose1, goal_pose2, goal_pose3]

nav.followWaypoints(waypoints)
while not nav.isTaskComplete():
    print(nav.getFeedback())

rclpy.shutdown()