from tf_transformations import quaternion_from_euler
from geometry_msgs.msg import PoseStamped
import re
def create_pose_stamped( pos_x, pos_y, rot_z,nav) -> PoseStamped:
    """Creates a position in the map frame with the given coordinates and rotation"""
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

def generate_initial_pose(nav)-> None:
    """sets the initial pose of the robot to the origin so that nav2 can start"""
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

def move_to(self,nav)-> None:
    """moves the robot next the  position in the queue"""
    if len(self.queue) == 0:
        return
    while len(self.queue) > 0:
        positions = self.queue.pop()
        position = create_pose_stamped(positions[0],positions[1],0.0,nav)
        nav.goToPose(position)
        while not nav.isTaskComplete():
            # print(nav.getFeedback())
            # print(nav.get_clock().now().to_msg().sec)
            pass
        nav.get_logger().info('reached  point ' + str(positions))
   


