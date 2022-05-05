## Python script for controlling OnRobot gripper over the gripper's web interface

From what I understand, the KUKA Iiwa with Sunrise OS cannot communicate with the OnRobot gripper over Ethernet IP and the IO is undocumented. To get started, this Python program use the OnRobot web interface to set the width of the gripper and read the status (Grip detected) etc. It uses Selenium and a Chrome Driver. 

## Installation
1. Download and install Chrome and the ChromeDriver: https://chromedriver.chromium.org/getting-started. Make sure that Chrome is updated so that the driver version matches the browser version.

2. Install the Python requirements by running the command

     ` pip install -r requirements.txt`
3. Run the script with the command

    ` python3 OnRobotGripper.py -u yourusername -pw yourpassword`

## Feature requests
- Java class to communicate directly with gripper. 
