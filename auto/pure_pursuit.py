def make_car_2d(desired_v:float=20.0, dt:float=0.1) -> dict:
    """ 
    Generates a dictionary that holds all the car's values. Keeps track of state varaibles.
    """
    car_state_dictionary : dict[str, float] = {
        "v" : 0, #velocity of your car 
        "a" : 0, #acceleration of your car
        "t" : 0, #time of your car
        "x" : 0, #position of your car
        "y" : 0, #car can move up and down? so x and y?
        "yaw" : 0, # direction car is pointing in radiants 
        "W" : wheelbase, # distance between back and front axles in meters , decides how sharp the car cna turn
        "target_index" : 0, #which waypoint the car is closest to on the track
        # "lookahead_distance" : 2 # distance it looks ahead on
        "dt" : dt, #time step of your car, how much the time changes every time you update/step
        "desired_v" : desired_v, #desired velocity of your car, the velocity you want to maintain
        "step" : 0,
    
        #hint: use these variables in the integral and derivative portion of your PID control (steps 5 and 6 )
        "error_prev" : None,
        "net_integral" : 0.0
    }
    return car_state_dictionary

def update_2(car: dict, throttle_perc: float, steer: float, mass: float = 1000, max_throttle_force: float = 5000, friction: float = 2.0) -> None:
     
     #pedal ,  force ,  acceleration (minus friction), new speed
        force = throttle_perc * max_throttle_force
        car["a"] = (force / mass) - friction
        car["v"] += car["a"] * car["dt"]
        """
        tania notes: friction - 2, if car is barely moving + 0 throttle car would go backwards
         
        four functions: 
        1. the car only goes in the front, doesnt roll back
        2. car moves in x direction
        3. car moves in y direction
        4. turning the car 
        """
        car["v"] = max(car["v"], 0.0) # picks bigger of two velocity so doesnt role back 
        car["x"] += car["v"] * np.cos(car["yaw"]) * car["dt"] # how far the car moves in one tick (longitudinal) * how much of that distance goes in the the x direction (lateral)
        car["y"] += car["v"] * np.sin(car["yaw"]) * car["dt"] # how far car moves in one tick(time) * how far car goes in the y direction
        car["yaw"] += car["v"] / car["W"] * np.tan(steer) * car["dt"] # turn ur car, how fast the car is rotating in radiants/sec * how much it rotates during 

        

        car["t"] += car["dt"]
        car["step"] += 1

def make_waypoints(n: int = 400): #making waypoints

    xvalues = np.linspace(0, 200, n) # 400 nums from 0 to 200
    yvalues = np.where(xvalues < 20, 0.0, 6 * (1 - np.cos((xs - 20) / 15))) # if x is less than 20 then y = 0 so the first 20 m is straight
    return np.column_stack((xvalues, yvalues))