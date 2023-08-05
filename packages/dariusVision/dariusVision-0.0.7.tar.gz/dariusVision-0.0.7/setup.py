from setuptools import setup

setup(
    name='dariusVision',
    version='0.0.7',
    description='Real-time video streaming utility for capturing the latest frame',
    long_description='dariusVision is a utility module for real-time video streaming applications. It uses OpenCV to capture frames from a video source and provides functionality to always fetch the latest frame. This is particularly useful in applications such as real-time video monitoring, analysis, and other scenarios where processing the most recent video frame is crucial.',
    packages=['dariusVision'],
    install_requires=[
        'numpy',
        # 'opencv-python',
        # 'pyrealsense2',
    ],
    author='gbox3d',
    author_email='gbox3d@gmail.com',
    url='https://github.com/gbox3d/dariusVision.git',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)