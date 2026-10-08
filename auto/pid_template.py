import numpy as np


def make_car(desired_v:float=20.0, dt:float=0.1) -> dict:
    """ 
    Generates a dictionary that holds all the car's values. Keeps track of state varaibles.
    """
    car_state_dictionary : dict[str, float] = {
        "v" : 0, #velocity of your car 
        "a" : 0, #acceleration of your car
        "t" : 0, #time of your car
        "x" : 0, #position of your car
        "dt" : dt, #time step of your car, how much the time changes every time you update/step
        "desired_v" : desired_v, #desired velocity of your car, the velocity you want to maintain
        "step" : 0,
    
        #hint: use these variables in the integral and derivative portion of your PID control (steps 5 and 6 )
        "error_prev" : None,
        "net_integral" : 0.0
    }
    return car_state_dictionary

def update(car: dict, throttle_perc: float, mass: float = 1000, max_throttle_force: float = 5000, friction: float = 2.0) -> None:
        """
        Updates the car's state variables based on the throttle percentage.
        Use this function after finding throttle percentage to update the car's state variables.

        Inputs:
        car: dictionary containing the car's state variables
        throttle_perc: float, throttle percentage (-1 to 1)

        Outputs:
        None, but updates the car's state variables
        """
        force = throttle_perc * max_throttle_force
        car["a"] = (force / mass) - friction
        car["v"] += car["a"] * car["dt"]
        car["x"] += car["v"] * car["dt"]
        car["t"] += car["dt"]
        car["step"] += 1

        """
       Tania notes:
        error = desired_v - car["v"] (how far you are from the target)
        desired acceleration = K_P * error (a bigger gap means more acceleration)

        friction takes aways 2 form acceleration 
        acceleration = push - 2
        steady state error: K_P * gap = 2
        """

        '''
        integral term - keeps running total of far off from desired velocity 
        --> adds to gas so the push gets stronger than friction , so car reaches 20 
        --> once error hits 0, stops growing and holds the push

        net_integral = (sum of error * dt)
        error * dt is error for one tick , how farr off times how long 

        '''

def calculate_desired_acceleration(car: dict, K_P: float, K_I: float = 0.0, K_D: float = 0.0) -> tuple[float, float]:
        #input: car["v"], car["desired_v"] (floats)
        #output: desired acceleration and error tuple(float, float)
        error = car["desired_v"] - car["v"] # desired velocity - current velocity (in car dictionary)
        car["net_integral"] += error * car["dt"] # error from right no added to total 
        if car["error_prev"] is None:
            de = 0
        else:
            de = error - car["error_prev"]  # how much the error changed since the last tick
        derivative = de / car["dt"] # how fast it's changing de/0.1
        desired_acceleration = K_P * error + K_I * car["net_integral"] # acceleration based on how far off the car is now (P) + how long it has been off (I)
        car["error_prev"] = error # saves tick error in the car dictionary
        return desired_acceleration, error # both acceleration then error
        
#first function states i want the car to speed up by abc, second function transaltes that into pedal position

'''
doesn't take acceleration
throttle percentage = how far down the gas pedal is pushed
acceleration = force/mass - full gass means motor pushes at full force, heavier car = accelerates less
max_acceleration = max_throttle_force/mass

pedal = what i want/ 5
'''


def acceleration_to_throttle_percentage(acceleration_desired: float, mass: float = 1000, max_throttle_force: float = 5000) -> float:
        #input: desired_acceleration(float)
        #output: throttle percentage (float, -1 to 1)
        max_acceleration = max_throttle_force / mass # full gass = 5000  - 5000/1000 = 5 = 100%
        throttle = acceleration_desired / max_acceleration #x/5
        throttle = np.clip(throttle, -1, 1) # np.clip(a, a_min, a_max)
        return throttle
