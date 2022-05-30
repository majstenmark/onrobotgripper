#!/usr/bin/env python3

import socket
import sys
from OnRobotGripper import OnRobotGripper
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=True, action='store', default='.', help="username")
    parser.add_argument('-pw', '--password', required=True, action='store', default='.', help="password")
    return parser.parse_args()

def main():
    args = get_args()

    gripper = OnRobotGripper('192.168.1.1', args.username, args.password)
    BUFFER = 1024
    HOST = "192.168.1.5"
    address = HOST, 30000
    connected = False
    force = 20
    speed = 10
 
    while not connected:
        try:            
            print('Waiting for Java client at ', socket.gethostbyname(HOST))
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            sock.bind(address)
            sock.listen(1)
            connected = True
            #address = 'localhost', 30000
        except:
            pass
    
    while True:
        connection, client_address = sock.accept()
        print('Got client', client_address)
        try:
            while True:
                data = connection.recv(BUFFER) 
                checkgrip = False

                if not data:
                    break
                msg = data.decode('UTF-8')
                print('Server got data', msg)
                
                response = 'ok'
                
                if msg.lower() == 'open':      
                    gripper.open(force, speed)
                  

                if msg.lower() == 'close':  
                    gripper.close()
                    checkgrip = True

                if msg.startswith('moveto'):
                    _, dists, forces, speeds = msg.split()
                    dist = int(dists)
                    force = int(forces)
                    speed = int(speeds)
                    gripper.moveto(dist, force, speed)
                    
                if msg.startswith('getposition'):
                    response = '' + str(gripper.getposition())

                if msg.startswith('setforce'):
                    _, forces = msg.split()
                    force = int(forces)
                if msg.startswith('setspeed'):
                    _, speeds = msg.split()
                    speed = int(speeds)

                while gripper.isBusy():
                    print('Busy')
                if checkgrip:
                    if gripper.gripDetected():
                        response = 'gripdetected'
                        
                
                connection.sendall(str.encode(response + '\n'))
                
        except Exception as e:
            print('Error', e)
            pass

        
if __name__ == "__main__":
    main()