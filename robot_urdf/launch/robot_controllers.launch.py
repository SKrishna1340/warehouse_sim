import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    # Set the path to this package.
    robot_urdf_pkg_share = FindPackageShare(package='robot_urdf').find('robot_urdf')

    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster',],
    )

    robot_controllers = os.path.join(robot_urdf_pkg_share, 'config', 'cart_controller.yaml')
    joint_trajectory_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'robot_controller',
            '--param-file',
            robot_controllers,
            ],
    )

    return LaunchDescription([
        joint_state_broadcaster_spawner,
        joint_trajectory_controller_spawner
    ])