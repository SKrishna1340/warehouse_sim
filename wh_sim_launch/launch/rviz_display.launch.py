#!/usr/bin/env python

import os

import launch
import xacro

from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

def generate_launch_description():
    pkgPath = FindPackageShare(package='wh_robot_urdf').find('wh_robot_urdf')
    urdfModelPath= os.path.join(pkgPath, 'urdf', 'robot_desc.xacro')
    
    robot_desc = xacro.process_file(urdfModelPath)
    robot_desc = robot_desc.toprettyxml(indent="  ")
    # with open(urdfModelPath,'r') as infp:
    # 	robot_desc = infp.read()
    
    params = {'robot_description': robot_desc}
    
    robot_state_publisher_node = Node(
    package='robot_state_publisher',
	executable='robot_state_publisher',
    output='screen',
    parameters=[params]
    )
    
    
    # joint_state_publisher_node = Node(
    #     package='joint_state_publisher',
    #     executable='joint_state_publisher',
    #     name='joint_state_publisher',
    #     parameters=[params],
    #     condition=launch.conditions.UnlessCondition(LaunchConfiguration('gui'))
    # )
    # joint_state_publisher_gui_node = Node(
    #     package='joint_state_publisher_gui',
    #     executable='joint_state_publisher_gui',
    #     name='joint_state_publisher_gui',
    #     condition=launch.conditions.IfCondition(LaunchConfiguration('gui'))
    # )

    rviz_config_file_path = os.path.join(pkgPath,
                                         "config",
                                         "RVIZ_config.rviz")
    
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=["-d", rviz_config_file_path]
    )
    #add config file to the rviz node

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='gui', default_value='True',
                                            description='This is a flag for joint_state_publisher_gui'),
        launch.actions.DeclareLaunchArgument(name='model', default_value=urdfModelPath,
                                            description='Path to the urdf model file'),
        robot_state_publisher_node,
        #joint_state_publisher_node,
        #joint_state_publisher_gui_node,
        rviz_node
    ]) 