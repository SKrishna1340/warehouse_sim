from glob import glob
from setuptools import find_packages, setup

package_name = 'wh_robot_urdf'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/urdf', glob("urdf/*")),
        ('share/' + package_name + '/config', glob("config/*")),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mskrishna',
    maintainer_email='33370500+SKrishna1340@users.noreply.github.com',
    description='Robot urdf models for warehouse simulation.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
