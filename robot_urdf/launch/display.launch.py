# Author: Sai Krishna M
# Date: December 22, 2024
# Description: Launch a robot URDF file using Rviz.
 
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
  
  # Set the path to this package.
  pkg_share = FindPackageShare(package='robot_urdf').find('robot_urdf')
  
  # Set the path to the URDF file
  model_name = 'KUKA_robots.xacro' #'robot_urdf.urdf.xacro'
  default_urdf_model_path = os.path.join(pkg_share, 'urdf', model_name)
  
  ########### YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE ##############  
  # Launch configuration variables specific to simulation
  gui = LaunchConfiguration('gui')
  urdf_model = LaunchConfiguration('urdf_model')
  use_robot_state_pub = LaunchConfiguration('use_robot_state_pub')
  use_rviz = LaunchConfiguration('use_rviz')
  use_sim_time = LaunchConfiguration('use_sim_time')
 
  # Declare the launch arguments  
  declare_urdf_model_path_cmd = DeclareLaunchArgument(
    name='urdf_model', 
    default_value=default_urdf_model_path, 
    description='Absolute path to robot urdf file')
     
  declare_use_joint_state_publisher_cmd = DeclareLaunchArgument(
    name='gui',
    default_value='True',
    description='Flag to enable joint_state_publisher_gui')
   
  declare_use_robot_state_pub_cmd = DeclareLaunchArgument(
    name='use_robot_state_pub',
    default_value='True',
    description='Whether to start the robot state publisher')
     
  declare_use_sim_time_cmd = DeclareLaunchArgument(
    name='use_sim_time',
    default_value='True',
    description='Use simulation (Gazebo) clock if true')
    
  # Specify the actions
 
  # Publish the joint state values for the non-fixed joints in the URDF file.
  start_joint_state_publisher_cmd = Node(
    condition=UnlessCondition(gui),
    package='joint_state_publisher',
    executable='joint_state_publisher',
    name='joint_state_publisher')
 
  # A GUI to manipulate the joint state values
  start_joint_state_publisher_gui_node = Node(
    condition=IfCondition(gui),
    package='joint_state_publisher_gui',
    #namespace="robot1",
    executable='joint_state_publisher_gui',
    name='joint_state_publisher_gui',
    # remappings=[
    #     ('/robot_description', '/robot1/robot_description'),
    #     ('/joint_states','/robot1/joint_states')]
    )
 

  with open(default_urdf_model_path, 'r') as infp:
        robot_desc = infp.read()

  # Subscribe to the joint states of the robot, and publish the 3D pose of each link.
  start_robot_state_publisher_cmd = Node(
    condition=IfCondition(use_robot_state_pub),
    package='robot_state_publisher',
    #namespace="robot1",
    executable='robot_state_publisher',
    parameters=[{'use_sim_time': use_sim_time,
                 'robot_description': ParameterValue(Command(["xacro ", default_urdf_model_path]),
                                                     value_type=str)}])
  
  # start_robot_state_publisher_cmd2 = Node(
  #   condition=IfCondition(use_robot_state_pub),
  #   package='robot_state_publisher',
  #   namespace="robot2",
  #   executable='robot_state_publisher',
  #   parameters=[{'use_sim_time': use_sim_time, 
  #   'robot_description': ParameterValue(Command(["xacro ", default_urdf_model_path]),
  #                                       value_type=str)}])
 
  # Launch RViz
  start_rviz_cmd = Node(
    package='rviz2',
    executable='rviz2',
    name='rviz2',
    arguments=["-d" + os.path.join(pkg_share, 'config', 'default.rviz')],
    output='screen')
   
  # Create the launch description and populate
  ld = LaunchDescription()
 
  # Declare the launch options
  ld.add_action(declare_urdf_model_path_cmd)
  ld.add_action(declare_use_joint_state_publisher_cmd)
  ld.add_action(declare_use_robot_state_pub_cmd)
  ld.add_action(declare_use_sim_time_cmd)
 
  # Add any actions
  ld.add_action(start_robot_state_publisher_cmd)
  #ld.add_action(start_robot_state_publisher_cmd2)
  ld.add_action(start_joint_state_publisher_cmd)
  ld.add_action(start_joint_state_publisher_gui_node)
  ld.add_action(start_rviz_cmd)
 
  return ld