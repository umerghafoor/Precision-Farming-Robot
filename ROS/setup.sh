#!/bin/bash

# Exit on error
set -e

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Ensure setuptools is installed
echo "Installing setuptools..."
pip install setuptools

# Install project dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r src/application/application/requirements.txt

# ROS setup
echo "Setting up ROS workspace..."
ROS_VERSION=${1:-rolling}
echo "Using ROS version: $ROS_VERSION"
source /opt/ros/$ROS_VERSION/setup.bash

# Set up the ROS workspace
echo "Setting up the workspace..."
# cd ~/Precision-Farming-Robot/ROS
colcon build

# Final setup message
echo "Setup complete! To activate your virtual environment, run 'source venv/bin/activate'."
