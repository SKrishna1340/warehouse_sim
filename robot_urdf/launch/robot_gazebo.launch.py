# Author: Sai Krishna M
# Date: December 22, 2024
# Description: Launch a robot URDF file using Gazebo.

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default=True)

    # Set the path to this package.
    robot_urdf_pkg_share = FindPackageShare(package='robot_urdf').find('robot_urdf')
 
    # Set the path to the URDF file
    default_urdf_model_path = os.path.join(robot_urdf_pkg_share, 'urdf', 'KUKA_robots.xacro')

    #need to set this variable for GAZEBO IONIC to find the mesh files.
    #https://gazebosim.org/api/sim/8/migrationsdf.html
    if 'GZ_SIM_RESOURCE_PATH' in os.environ:
        os.environ['GZ_SIM_RESOURCE_PATH'] += robot_urdf_pkg_share+"/.."
    else:
        os.environ['GZ_SIM_RESOURCE_PATH'] =  robot_urdf_pkg_share+"/.."

    # with open(default_urdf_model_path, 'r') as infp:
    #     robot_desc = infp.read()
    
    # Configure the node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': True,
                     'robot_description': ParameterValue(Command(["xacro ", default_urdf_model_path]),
                                                     value_type=str)}])

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(get_package_share_directory('ros_gz_sim'), 'launch'),
             '/gz_sim.launch.py'
             ]),
        launch_arguments={
            'gz_args': [PathJoinSubstitution([robot_urdf_pkg_share, 'config', 'world.sdf']), ' -r'],
            }.items()
        )
    
    spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=['-topic', 'robot_description',
                  '-name', 'KUKA_robot1'],
        # arguments=['-file', '/home/mskrishna/ros2_ws/src/robot_urdf/urdf/robot_urdf_manual.urdf', '-name', 'KUKA_robot'],
        output = "screen"
    )

    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster',],
    )

    robot_controllers = os.path.join(robot_urdf_pkg_share, 'config', 'KUKA_controller.yaml')
    
    joint_trajectory_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'robot_controller',
            '--param-file',
            robot_controllers,
            ],
    )

    # Bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        #ros_arguments=['yes'],
        parameters = [{"config_file":os.path.join(robot_urdf_pkg_share, 'config', 'ros_gz_bridge_config.yaml')}],
        output='screen'
    )

    # Run the nodes
    return LaunchDescription([
        node_robot_state_publisher,
        gazebo,        
        spawn_entity,
        joint_state_broadcaster_spawner,
        joint_trajectory_controller_spawner,
        bridge,

        DeclareLaunchArgument(
            'use_sim_time',
            default_value=use_sim_time,
            description='If true, use simulated clock')
    ])


#ros2 topic pub --once /robot_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "{joint_names: ['robot1_jnt_Base_to_Ax1', 'robot1_jnt_Ax1_to_Ax2', 'robot1_jnt_Ax2_to_Ax3', 'robot1_jnt_Ax3_to_Ax4', 'robot1_jnt_Ax4_to_Ax5', 'robot1_jnt_Ax5_to_Ax6'], points: [{positions: [-1.345, -1.23, 0.264, -0.296, 0.389, -1.5], time_from_start: {sec: 50, nanosec: 0}}]}"

#ros2 topic pub --once /robot_controller/commands std_msgs/msg/Float64MultiArray "{data: [10.45, 22.5, 75.0, 30.0, 85.0, 50.0]}"

#ros2 topic pub /robot_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "{joint_names: ['robot1_jnt_Base_to_Ax1', 'robot1_jnt_Ax1_to_Ax2', 'robot1_jnt_Ax2_to_Ax3', 'robot1_jnt_Ax3_to_Ax4', 'robot1_jnt_Ax4_to_Ax5', 'robot1_jnt_Ax5_to_Ax6'], points: [{positions: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], time_from_start: {sec: 50, nanosec: 0}}]}"