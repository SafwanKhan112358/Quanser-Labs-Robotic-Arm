## ----------------------------------------------------------------------------------------------------------
## TEMPLATE
## Please DO NOT change the naming convention within this template. Some changes may
## lead to your program not functioning as intended.

import sys
from typing import Container
sys.path.append('../')

from Common_Libraries.p2_sim_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = qarm()
update_thread = repeating_timer(2, update_sim)

#---------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------

# write function to get autoclave drop off locations
def identify_autoclave_location(Container_ID):

    #function takes in Container_ID based on spawned container 

    #conditional statements which provide autoclave location coordinates
    #based on Container_ID

    #return coordinates

    if Container_ID == 1:
        return [-0.590,0.240,0.400]
        # small red
    elif Container_ID == 2:
        return [0.0,-0.640,0.400]
        # small green
    elif Container_ID == 3:
        return [0.0,0.640,0.400]
        #small blue
    elif Container_ID == 4:
        return [-0.390,0.165,0.485]
        # large red
    elif Container_ID == 5:
        return [0,-0.390,0.485]
        # large green
    elif Container_ID == 6:
        return [0,0.390,0.485]
        # large blue

# write function for moving end effector
def moveEndEffector(pos):
    # assign x, y, z based on list values
    # x = pos[0]
    # y = pos[1]
    # z = pos[2]
    # while loop for threshold value of 0.5
    while True:
        if (arm.emg_left() < 0.5) and (arm.emg_right() >= 0.5):
            time.sleep(1)
        # move arm to x, y, z
            arm.move_arm(pos[0], pos[1], pos[2])
            time.sleep(1)
            break

# write function for gripping container
def controlGripper():
    global openGripper # define global var openGripper
    while True:
        if (arm.emg_left() >= 0.5) and (arm.emg_right() < 0.5):
            #check gripper state
            if openGripper:
                openGripper = False # set close gripper
                arm.control_gripper(45) # move gripper to 45 deg
                time.sleep(1)
            elif openGripper == False:
                openGripper = True # set open gripper
                arm.control_gripper(-45) # move gripper to -45 deg
                time.sleep(1)
            break

# write autoclave drawer function
def autoclave_drawer(Container_ID):
    # create global var for large containers
    global openRed
    global openGreen
    global openBlue

    #function takes in Container_ID based on spawned container 

    # conditional statements for 1,2,3 (small containers)
    # small containers are not placed in autoclave bin, so these IDs
    # are passed

    if Container_ID == 1 or 2 or 3:
        pass

    # conditional statements for 4,5,6 (large containers)
    #large containers are placed inside autoclave bins

    # Sample case
    # if Container_ID is 4
    # implement sub condition to ensure muscle sensor is greater or equal to
    #than threshold
    # if above, open/close autoclave drawer
    # if autoclave drawer is open, close it
    # if autoclave drawer is closed, open it

    if Container_ID == 4:
        while 1:
            if arm.emg_right() >= 0.5 and arm.emg_left() >= 0.5:
                # check autoclave bin state
                if openRed:
                    arm.open_red_autoclave(False) # close the bin
                    openRed = False # set bin closed
                    time.sleep(1)
                elif not openRed:
                    arm.open_red_autoclave(True) # open the bin
                    openRed = True # set bin open
                    time.sleep(1)
                break

    elif Container_ID == 5:
        while 1:
            if arm.emg_right() >= 0.5 and arm.emg_left() >= 0.5:
                # check autoclave bin state
                if openGreen:
                    arm.open_green_autoclave(False) # close the bin
                    openGreen = False # set bin closed
                    time.sleep(1) 
                elif not openGreen:
                    arm.open_green_autoclave(True) # open the bin
                    openGreen = True # set bin open
                    time.sleep(1)
                break

    elif Container_ID == 6:
        while 1:
            if arm.emg_right() >= 0.5 and arm.emg_left() >= 0.5:
                # check autoclave bin state 
                if openBlue:
                    arm.open_blue_autoclave(False) # close the bin
                    openBlue = False # set bin closed
                    time.sleep(1)
                elif not openBlue:
                    arm.open_blue_autoclave(True) # open the bin
                    openBlue = True # set bin open
                    time.sleep(1)
                break

# import libraries
import random
# define variables
totalContainers = [1, 2, 3, 4, 5 ,6]
openGripper = True
openRed = False
openGreen = False
openBlue = False
pickup = [0.534, 0.0, 0.044]
home =   [0.406, 0.0, 0.483]

# write final program while loop
while len(totalContainers) >= 1: # while the amount of containers is equal to or greater than 1
    # spawn containers
    container = totalContainers[random.randint(0, len(totalContainers)-1)]
    totalContainers.remove(container)
    arm.spawn_cage(container)
    # q arm goes to pickup and goes home
    moveEndEffector(pickup) # go to pickup
    controlGripper() # pickup container
    moveEndEffector(home) # go home pos
    # q arm goes to dropoff
    pos = identify_autoclave_location(container) # retrieve dropoff location
    moveEndEffector(pos) # go to dropoff location
    # q arm completes large container procedure
    autoclave_drawer(container) # open autoclave bin if required (large containers)
    controlGripper() # drop container
    autoclave_drawer(container) # close autoclave bin if opened
    # q arm goes home
    moveEndEffector(home) # go home pos
    time.sleep(1) # sleep for 1 
#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------