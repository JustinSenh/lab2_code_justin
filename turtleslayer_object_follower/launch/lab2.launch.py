import launch
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtleslayer_object_follower',
            executable='cam_v2_feed',
           
        ),
        Node(
            package='turtleslayer_object_follower',
            executable='find_object_node',
         
        ),
        Node(
            package='turtleslayer_object_follower',
            executable='rotate_robot',
            
        )
    ]) 