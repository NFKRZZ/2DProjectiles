#A program to plot trajectories of a single orbiting object using the RK4 Method
 
#Import the necessary libraries
import matplotlib.pyplot as plt #Necessary to plot stuff
import math
from numpy import * #For things like pi, linspace, etc
 
def f(t, u): #This is the (vector) f(t,u) in the ODE; du/dt=f(t,u)
    x = u[0]
    vx = u[1]
    y = u[2]
    vy = u[3]
    v = sqrt(vx**2+vy**2)
    #mvt = (vy-(-gravity-(k*v**2)*(vy/v)))
    #print("This is mvt result"+str(mvt))
   # r = sqrt(x**2 + y**2)
    return [vx, -(k*v**2)*(vx/v), vy, -gravity-(k*v**2)*(vy/v)]
 
#Define the starting values, number of points, and the step
t_initial = 0.0
x_initial = 0.0
y_initial = 0.0
v_initial = 15.0
initial_angle = 45 * pi/180
gravity = 1
k=1
step = 0.01
points = 10000
desired_x = 2
desired_y = 2
 
#Start the t and u values lists
t_values = [t_initial]
u_values = [[x_initial, v_initial*cos(initial_angle), y_initial, 
v_initial*sin(initial_angle)]] #As u is a list, you'll need a list of lists (array)to store the u values
 
#Define a function to handle the RK4 Method update (this function does not need to be modified for different sized systems)
def RK4Meth(t, u):
    k1 = f(t, u)
    k2 = f(t + step/2, add(u, multiply(step/2, k1))) #Need to use the add( and multiply( functions to do the operations to each list item
    k3 = f(t + step/2, add(u, multiply(step/2, k2)))
    k4 = f(t + step, add(u, multiply(step, k3)))
    return add(u, multiply(step/6, add(k1, add(multiply(2, k2), add(multiply(2, k3), k4))))) #The add( function can only handle two lists at a time, so to add all the lists together we need to nest the function :(
 
#Actually calculate the u values
def Simulate():
    u_values.append(RK4Meth(t_values[-1],u_values[-1]))
    t_values.append(t_values[-1]+step)
    for i in range(points):
        if(u_values[-1][2]>0):
            u_values.append(RK4Meth(t_values[-1], u_values[-1])) #Add the next u value (the [-1] calls the last item in the current list)
            t_values.append(t_values[-1] + step) #Add the next t value
            #print(i,u_values[i])
angles = []
velocities = []
min_angle = 0
tolerance = 0.05
angleFound = False
for z in range(1,91,1):
    if(angleFound==False):
        initial_angle = z*(pi/180)
        #print("Initial Angle is "+str(initial_angle*(180/pi)))
        Simulate()
        xx_values = transpose(u_values)[0]
        yy_values = transpose(u_values)[2]
        for j in range(len(xx_values)):
            #print(str(xx_values[j])+" - "+str(desired_x)+" = "+str(abs(xx_values[j]-desired_x))+" X Value Found: " +str(j))
            if(abs(xx_values[j]-desired_x)<=tolerance):
                #print(str(yy_values[j])+" - "+str(desired_y)+" = "+str(abs(yy_values[j]-desired_y))+" Y value found: "+str(j))
                if(abs(yy_values[j]-desired_y)<=tolerance):
                    print("Min Angle Found"+str(min_angle*(180/pi)))
                    min_angle = z*(pi/180)
                    angleFound = True
                else:
                    u_values.clear()
                    t_values.clear()
                    u_values.append([x_initial,v_initial*cos(initial_angle+(pi/180)),y_initial, v_initial*sin(initial_angle+(pi/180))])
                    t_values.append(t_initial)
    else:
        None
            
print("Min Angle is "+str(min_angle*(180/pi)))
angles = []
velocities = []
u_values.clear()
t_values.clear()
u_values.append([x_initial,v_initial*cos(initial_angle+(pi/180)),y_initial,v_initial*sin(initial_angle+(pi/180))])
print("hello"+str(u_values))
t_values.append(t_initial)
rang = round(80-(min_angle*(180/pi)))
v_initial = 1
angleFound = False
for b in range(rang):
    angleFound = False
    print("Iteration: "+str(b))
    initial_angle = (b+((min_angle)*(180/pi))+2)*(pi/180)
    FoundSpeed = False
    stuff = linspace(1,200,4000)
    for veloc in stuff:
        if(angleFound==False):
            print("This is veloc "+str(veloc)+" For angle "+str(initial_angle*(180/pi)))
            u_values.clear()
            t_values.clear()
            v_initial = veloc
            t_values.append(t_initial)
            u_values.append([x_initial,v_initial*cos(initial_angle),y_initial,v_initial*sin(initial_angle)])
            Simulate()
            xval = transpose(u_values)[0]
            yval = transpose(u_values)[2]
            if(max(yval)<desired_y):
                None
            else:
                for j in range(len(xval)):
                    #print("XVALUES CALC"+str(xval[j])+" - "+str(desired_x)+" = "+str(abs(xval[j]-desired_x)))
                    if(abs(xval[j]-desired_x)<=tolerance):
                        print("X&Y VALUE CALC, X:"+str(xval[j])+" - "+str(desired_x)+" = "+str(abs(xval[j]-desired_x))+" Y VALUE CALC "+str(yval[j])+" - "+str(desired_y)+" = "+str(abs(yval[j]-desired_y)))
                        if(abs(yval[j]-desired_y)<=tolerance):
                            print("Velocity Found For Current Angle"+str(v_initial)+" "+str(initial_angle*(180/pi)))
                            angles.append(initial_angle*(180/pi))
                            velocities.append(v_initial)
                            angleFound = True
                            break
            u_values.clear()
            t_values.clear()
            t_values.append(t_initial)
            u_values.append([x_initial,v_initial*cos(initial_angle+(pi/180)),y_initial,v_initial*sin(initial_angle+(pi/180))])
        else:
            u_values.clear()
            t_values.clear()
            t_values.append(t_initial)
            u_values.append([x_initial,v_initial*cos(initial_angle+(pi/180)),y_initial,v_initial*sin(initial_angle+(pi/180))])
                    
            
u_values.clear()
t_values.clear()
u_values.append([x_initial,v_initial*cos(initial_angle),y_initial, v_initial*sin(initial_angle)])
t_values.append(t_initial)
Simulate()
#Extract the x_values from the u_values array (the only values we're interested in plotting for this example)
x_values = transpose(u_values)[0] #The transpose turns the u_values array into a list of two lists, i.e. transpose(u_values) is [x_values, v_values]
y_values = transpose(u_values)[2]
vx_values = transpose(u_values)[1]
vy_values = transpose(u_values)[3]
print("With Inital Velocity of :"+str(v_initial)+" and an initial angle of "+str(initial_angle*(180/pi)))
print("Total iterations: "+str(size(x_values)))
print("The range was : "+str(x_values[-1]-x_values[0]))
print("Highest point acheived was: "+str(max(y_values)))
print("Minimum Angle is "+str(min_angle*180/pi))
#Plot that stuff
plt.figure()
plt.plot(angles, velocities)
plt.show()
