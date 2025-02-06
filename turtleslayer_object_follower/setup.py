from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'turtleslayer_object_follower'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        ('share/' + package_name + '/launch', glob(os.path.join('launch',
                            'lab2.launch.py'))),
        
        ('share/' + package_name + '/rviz', glob(os.path.join('rviz', 
                                    'lab2.launch.py'))),

        (os.path.join('share', package_name, 'launch'),
         glob(os.path.join('launch', '*.launch.py')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='justinsen',
    maintainer_email='justinsen@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "cam_v2_feed=turtleslayer_object_follower.cam_v2_feed:main",
            "find_object_node=turtleslayer_object_follower.find_object_node:main",
            "rotate_robot=turtleslayer_object_follower.rotate_robot:main"
        ],
    },
)
