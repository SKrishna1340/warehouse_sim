# pylint: disable=ungrouped-imports

# Author: Sai Krishna M
# Date: December 22, 2024
# Description: Launch a robot URDF file using Gazebo.
"""
Docstring for robot_urdf.launch.cart_gazebo.launch
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    """Generate launch description for robot URDF in Gazebo."""

    use_sim_time = LaunchConfiguration('use_sim_time',
                                       default=True)

    # Set the path to this package.
    pkg_share = FindPackageShare(package='robot_urdf').find('robot_urdf')

    # Set the path to the URDF file
    default_urdf_model_path = os.path.join(pkg_share, 'urdf',
                                           'object.urdf')
                                        #    'test_cart_position.xacro.urdf')

    #need to set this variable for GAZEBO to find the mesh files.
    #https://gazebosim.org/api/sim/8/migrationsdf.html
    if 'GZ_SIM_RESOURCE_PATH' in os.environ:
        os.environ['GZ_SIM_RESOURCE_PATH'] += pkg_share+"/.."
    else:
        os.environ['GZ_SIM_RESOURCE_PATH'] =  pkg_share+"/.."

    # Process the URDF file an set the robot_description
    robot_desc = ParameterValue(Command(['xacro ', default_urdf_model_path]),
                                value_type=str)
    # Configure the node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': True,
                     'robot_description': robot_desc
                     }]
                     )

    # Example addition: Joint State Publisher
    node_joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        output='screen',
    )

    spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=['-topic', '/robot_description',
                   '-name', 'cart'],
        output = "screen"
    )

    robot_controllers = os.path.join(pkg_share, 'config', 'cart_controller.yaml')
    joint_trajectory_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'robot_controller',
            '--param-file',
            robot_controllers,
            ],
    )

    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster',
                   '--controller-manager',
                   '/controller_manager'],
    )

    # Bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        #ros_arguments=['yes'],
        parameters = [{"config_file":os.path.join(pkg_share,
                                                  'config',
                                                  'ros_gz_bridge_config.yaml')}],
        output='screen'
    )

    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'),
                         'launch',
                         'gz_sim.launch.py')
        ),
    )

    # Run the nodes
    return LaunchDescription([
        node_robot_state_publisher,
        node_joint_state_publisher,
        spawn_entity,
        joint_trajectory_controller_spawner,
        gazebo_client,
        joint_state_broadcaster_spawner,
        bridge,

        DeclareLaunchArgument(
            'use_sim_time',
            default_value=use_sim_time,
            description='If true, use simulated clock')
    ])


#ros2 topic pub --once /robot_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "{joint_names: ['slider_to_cart'], points: [{positions: [-1.345], time_from_start: {sec: 50, nanosec: 0}}]}"


#ros2 topic pub /robot_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "{joint_names: ['robot1_jnt_Base_to_Ax1', 'robot1_jnt_Ax1_to_Ax2', 'robot1_jnt_Ax2_to_Ax3', 'robot1_jnt_Ax3_to_Ax4', 'robot1_jnt_Ax4_to_Ax5', 'robot1_jnt_Ax5_to_Ax6'], points: [{positions: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], time_from_start: {sec: 50, nanosec: 0}}]}"