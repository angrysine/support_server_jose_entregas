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

def move_to(self,text,nav)-> None:
    """moves the robot to the given position"""
    positions= get_input_position(self,text)
    if positions is None:
        return None
    goal_pose = create_pose_stamped(positions[0], positions[1], 0.0,nav)
    nav.goToPose(goal_pose)
    
    while not nav.isTaskComplete():
        # print(nav.getFeedback())
        # print(nav.get_clock().now().to_msg().sec)
        pass
    nav.get_logger().info('reached  point ' + str(positions))





def get_input_position(self,text)->list[float]|None:
        """ 
        This function purpose is to get the position from the chatbot
        using a regex, then returning it as a list of float
        """
        input_text = text
        match = re.findall(r'\b\d+\b', input_text)
        if len(match) <2:
            return None
        self._logger.info(f'Robot received: {text}')
        self._logger.info(f'Robot received: {match}')
        position = [float(match[0]),float(match[1])]
        return position



