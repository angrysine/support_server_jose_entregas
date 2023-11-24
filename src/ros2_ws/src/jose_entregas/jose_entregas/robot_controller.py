#! /usr/bin/env python3

import re
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from nav2_simple_commander.robot_navigator import TaskResult

from .navigation_controller import Navigation

class Robot(Node):
    def __init__(self):
        super().__init__('robot_node')
        self._publisher = self.create_publisher(String, 'robot_topic', 10)
        self._subscriber = self.create_subscription(
            String,
            'chatbot_topic',
            self.listener_callback,
            10)
        self._logger = self.get_logger()
        # Uncomment the following lines to see the robot node and debug
        # timer_period = 3.0
        # self.i = 0
        # self._timer = self.create_timer(timer_period, self.timer_callback)
        self._msg = String()
        self._nav = Navigation()

    def listener_callback(self, msg):
        """ 
        This function purpose is to receive the data from the chatbot topic
        """
        self._logger.info(f'Robot received: {msg.data}')
        self._logger.warning('Passing data to navigation controller')
        self._msg = msg.data
        return self._msg

    # def timer_callback(self):
    #     """ 
    #     This function purpose is to show that the robot is still
    #     waiting for inputs besides the fact that a timer is set to
    #     posterior debugging/analytics 
    #     """
    #     self._msg.data = f'Robot waiting for inputs: {self.i}' 
    #     self._publisher.publish(self._msg)
    #     self._logger.info(f'Robot sent: {self._msg.data}')
    #     self._logger.info('Robot is running')
    #     self.i += 1
    
    def get_input_position(self):
        """ 
        This function purpose is to get the position from the chatbot
        using a regex, then returning it as a list of integers
        """
        input_text = self.listener_callback()
        match = re.findall(r'\b\d+\b', input_text)
        position = [int(match) for i in match[-2:]]
        return position

    def move_towards_required_position(self):
        """ 
        This function purpose is to create a pose and move the robot
        """
        position = self.get_input_position()
        self._nav.create_pose(position[0], position[1], 0.0)
    
    def cheking_status(self):
        """ 
        Checks the status of a task after moving towards the required position.
        Returns:
        bool: True if the task is completed successfully, False otherwise.
        """
        self.move_towards_required_position()
        task_status = self._nav.robot_navigation_status()
        
        return task_status if task_status == TaskResult.SUCCEEDED else False

def main():
    rclpy.init()
    robot = Robot()
    while True:
        task_status = robot.cheking_status()
        if task_status:
            robot._msg.data = 'Goal arrived, waiting for new command'
            robot._publisher(robot._msg)
        else:
            robot._msg.data = 'Failed to reach goal'
            break
    robot.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
