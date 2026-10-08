import matplotlib.pyplot as plt
from pid_template import make_car
from pid_template import update
from pid_template import calculate_desired_acceleration
from pid_template import acceleration_to_throttle_percentage

# K_P = 0.1 , 0.1 * 20 = 2 , but fiction takes away 2 so car never moves...
K_P = 0.5
K_I = 0.1
K_D = 0.1
 
STEPS = 550
 
car = make_car(desired_v=20.0, dt=0.1)


#three list for velocity, errors, times
velocities = []
errors = []
times = []

for step in range(STEPS): # repeats 550 times
    desired_acceleration, error = calculate_desired_acceleration(car, K_P) # how much does car want to speed
    throttle = acceleration_to_throttle_percentage(desired_acceleration) # gas pedal position
    update(car, throttle) # upadates car speed - presses pedal so car moves
    print(car["v"]) # car new speed, car speed 0.3 (output)
    #adds num to list
    velocities.append(car["v"])
    errors.append(error)
    times.append(car["t"])

print(velocities[-1]) # car new speed , end of list 


plt.figure() #opens graph for velocity
plt.xlabel("time") #x axis
plt.ylabel("velocity") # y velocity
plt.plot(times, velocities) #draws line
plt.title("Velocity over Time") # title

plt.figure() # graph for error
plt.xlabel("time") # x axis
plt.ylabel("error") # y axis
plt.plot(times, errors) # draws line
plt.title("Error over Time") # title 

plt.show() # shows both graphs