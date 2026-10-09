import matplotlib.pyplot as plt
from pid_template import make_car
from pid_template import update
from pid_template import calculate_desired_acceleration
from pid_template import acceleration_to_throttle_percentage

# K_P = 0.1 , 0.1 * 20 = 2 , but fiction takes away 2 so car never moves...
K_P = 0.5
K_I = 0.03
K_D = 0.1
 
# lowered K_I from 0.1 to 0.03 cut the overshoot from about 26.5 to about 20.3 (step 7)

STEPS = 550
 
car = make_car(desired_v=20.0, dt=0.1)


#three list for velocity, errors, times
velocities = []
errors = []
times = []

for step in range(STEPS): # repeats 550 times
    desired_acceleration, error = calculate_desired_acceleration(car, K_P, K_I, K_D) # how much does car want to speed
    throttle = acceleration_to_throttle_percentage(desired_acceleration) # gas pedal position

# Add in additional forces against the car, increasing friction (simulation)
    if step < 150: # ticks from 0 to 199 
        friction = 2.0 # normal friction
    elif step < 250: # ticks from 200 to 349
        friction = 4.0 # abnormal friction (rough road)
    elif step < 350: 
        friction = 2.0 # back to normal, lets it recover
    elif step < 450:
        friction = 1.0 # less friction
    else:
        friction = 2.0     # back to normal
    update(car, throttle, friction=friction)

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

'''
steady state error = gap that's left over 
steady state - car stopped changing speed , in steady speed
error - distance it needs to catch up to reach the target
'''

'''
The closer the car gets to the target the less the controller presses the gas -  friction gets less its always pulling back by the same amount

so at some speed the gas gets so less that it only matches friction, then the car stops speeding up and jsut keeps movementum which is  short of target

when num is far from 20  the car speeds up fast 
near 16 -  the gas is weak - only as strong as friction
at 16 - gas is same as  friction so stays at 16
'''

'''
K_D * (de / dt)
de = tick's errors - last tick's error
dt = tick length (0,1)
de/dt - how fast error is changing 

P - how far off car is are right now
I - how long car has been off
D - how fast the error is changing

'''