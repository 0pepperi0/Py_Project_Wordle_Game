import time
from settings import *
from botVector import *
from person_stream import *
from Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi.Code.Server.Motor import *
from Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi.Code.Server.Light import *
from enum import Enum

# this class is used for setting the robot's status when an event occurs
class RobotStatus(Enum):
    IDLE = 1
    DUTY = 2
    LOST = 3

# initialize robot's components
motor = Motor()
status = RobotStatus(1)

# check if robot is near to the person or not
# accept distance is the radius of the area marking the robot has arrived
def approached(accept_distance: float) -> bool:
    #change function of robot
    r_location = settings.collector.getRobotLocation()
    r_x = r_location.getX()
    r_y = r_location.getY()

    #change function of person
    p_location = settings.collector.getPersonLocation()
    p_x = p_location.getX()
    p_y = p_location.getY()

    value = math.sqrt((p_x - r_x)**2 + (p_y - r_y)**2)
    if(value > accept_distance):
        return False
    else:
        return True
    

def rotate(angle: float, r_locationCurrent: Point, p_location: Point) -> None:
    rotate_angle = 0
    if(r_locationCurrent.getX() >= p_location.getX()):
        rotate_angle = 180-angle
    else:
        rotate_angle = angle
    rotation_time = rotate_angle* (0.88/90)
    if(r_locationCurrent.getY >= p_location.getY()):
        motor.setMotorModel(2000,2000,-2000,-2000)
    else:
        motor.setMotorModel(-2000,-2000,2000,2000)
    time.sleep(rotation_time)
    motor.setMotorModel(0,0,0,0)


# check if values of variables are the same to the values of Collector class attributes
def moveToPerson() -> None:
    time.sleep(1.5)
    prevRobotLocation = settings.collector.getInitRobotLocation()
    motor.setMotorModel(1000,1000,1000,1000)
    time.sleep(2)
    motor.setMotorModel(0,0,0,0)
    time.sleep(1)
    
    currPersonLocation = settings.collector.getPersonLocation()
    settings.addInitPersonLocation(currPersonLocation)
    currRoborLocation = settings.collector.getRobotLocation()

    r_vector = Vector(currRoborLocation, prevRobotLocation)
    r_p_vector = Vector(currPersonLocation, currRoborLocation)
    angle = angleBetweenVectors(r_vector, r_p_vector)
                #calibration is required 
    rotate(angle, r_locationCurrent, p_location)
    
    while(approached(30) or not personMove(30)):
        motor.setMotorModel(1000,1000,1000,1000)
        time.sleep(1.8)
        motor.setmotorModel(0,0,0,0)
        #set a value of curr location to previous location
        settings.Collector.addInitRobotLocation(currRoborLocation)
        settings.Collector.addInitPersonLocation(currPersonLocation)
        
        currRoborLocation = settings.Collector.getRobotLocation()
        currPersonLocation = settings.Collector.getPersonLocation()
        r_vector = Vector(currRoborLocation, prevRobotLocation)
        p_vector = Vector(currPersonLocation, currRoborLocation)
        angle = angleBetweenVectors(r_vector, p_vector)
        rotate(angle, currRoborLocation, currPersonLocation)
    
    status = RobotStatus.IDLE
        


def personMove(approp_error: float) -> bool:
    #checks if person is moving or not
    personLocationPrev = settings.Collector.getInitialPersonLocation() #change the method to the correct one 
    personLocationCurr = settings.Collector.getPersonLocation()
    prev_x = personLocationPrev.getX()
    prev_y = personLocationPrev.getY()
    curr_x = personLocationCurr.getX()
    curr_y = personLocationCurr.getY()
    if(abs(prev_x - curr_x) > approp_error and 
       abs(prev_y - curr_y) > approp_error):
        return True
    else:
        return False


#Final version of the movement algorithm
def movement():
    status = RobotStatus.IDLE

    while True:
        match (status):
            case RobotStatus.IDLE:
                if(settings.is_button_pressed):
                    status = RobotStatus.DUTY
                    continue
                else:
                    time.sleep(2)
                continue
            
            case RobotStatus.DUTY:
                moveToPerson()
