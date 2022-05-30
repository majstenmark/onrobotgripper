## Python script for controlling OnRobot gripper over the gripper's web interface

From what I understand, the KUKA Iiwa with Sunrise OS cannot communicate with the OnRobot gripper over Ethernet IP and the IO is undocumented. To get started, this Python program use the OnRobot web interface to set the width of the gripper and read the status (Grip detected) etc. It uses Selenium and a Chrome Driver. 

## Installation
1. Download and install Chrome and the ChromeDriver: https://chromedriver.chromium.org/getting-started. 

2. Make sure that Chrome is updated so that the driver version matches the browser version: To update Chrome, open the Chrome browser, select Settings in the three-dot menu in the upper right corner and finally About Chrome in the left-side menu, Chrome will be updated automatically. Press the Relaunch button to finish the update. 

3. Install the Python requirements by running the command

     ` pip install -r requirements.txt`
4. Run the script with the command

    ` python3 OnRobotGripper.py -u yourusername -pw yourpassword`

## Feature requests
- Java class to communicate directly with gripper. 
