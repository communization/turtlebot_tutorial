from setuptools import setup

package_name = 'turtlebot4_python_tutorials'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lee',
    maintainer_email='lee@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'turtlebot4_first_python_node = turtlebot4_python_tutorials.turtlebot4_first_python_node:main',
            'button_test = turtlebot4_python_tutorials.button_test:main',
            'light_on = turtlebot4_python_tutorials.light_on:main',
            'UCheck = turtlebot4_python_tutorials.UCheck:main',
        ],
    },
)
