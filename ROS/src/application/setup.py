from setuptools import find_packages, setup

package_name = 'application'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=[
        'setuptools',
        'PyQt6',
        'opencv-python',
        'pygame',
        'rclpy',
        'numpy',
        'pyyaml',
        'pyserial',
        'Cython'
        ],
    zip_safe=True,
    maintainer='umerghafoor',
    maintainer_email='umerghafoor@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robot_control_app = application.main:main',
        ],
    },
)
