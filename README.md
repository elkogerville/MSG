# Merging Simulator for Galaxies [MSG]
<br> This python code simulates the motion of massless test particles (galactic disk) through a gravitational potential field created by 2 central bulge particles. This restricted N-Body simulation is modeled after the Toomre and Toomre 1972 simulations and allows for 3D visualization of galaxy mergers.
<br>
<br>
## how code works:
the program performs a restricted N-Body calculation onto test particles in a potential field. two massive bulge particles are sent into each other and massless test particles are initialized to orbit bulge particles. the massless test particles follow circular keplerian orbits. the simulation calculates the gravitational acceleration from the two bulges onto each test particle in 3 dimensions using the equation 
<br> 
$$g_{i} =-Gm_{k}\sum_{n=i}^{N}\frac{r_{k}-r_{i}}{[|r_{k}-r_{i}|^{2}+\epsilon^{2}]^{3/2}}$$
where $r_{i}$ represents the x,y,z coordinates of each particle and $r_{k}$ the x,y,z coordinates of each bulge. each timestep new accelerations are calculated for each particle and used to determine the next position.
<br>
to run the code, first import simulation functions, and initialize bulge positions and velocities manually [see "initial conditions to try" for sample initial conditions]. use MSG_disk to automatically create matching positions and velocities for bulges. the actual simulation calculations are performed by calling MSG_galaxy and specifying the number of timesteps to run. plot a singular timeframe using MSG_plot or animate the timesteps with celluloid or matplotlib animations [sample code provided below]
## running the code:
```python
### IMPORT STATEMENTS
import numpy as np
from MSGpy import MSG_galaxy
from MSGpy import MSG_disk
from MSGpy import MSG_plot
### INITIAL CONDITIONS 
pos = np.array([[-12.5, 13.0, 0.0], [0.0, 0.0, 0.0]]) # companion and primary galaxy positions
vel = np.array([[1.5, -1.0, 0.0], [0.0, 0.0, 0.0]]) # respective velocities 
mas = np.array([[1.0], [3.0]]) # masses
# create primary disk
pos_p, vel_p, N = MSG_disk(number_of_rings = 6, mass = 3, rotation_dir = -1, density = 3.7) 
# create companion disk 
com_p, com_v, M = MSG_disk(number_of_rings = 3, mass = 1, rotation_dir = -1, density = 6, origin = [-12.5, 13.0, 0.0], 
                     velocity = [1.5, -1.0, 0.0])
### RUN SIMULATION for 1000 timesteps
a, b, c, d = MSG_galaxy(gal_pos = pos, gal_vel = vel, mass = mas, particle_pos = pos_p, particle_vel = vel_p, 
                        dt = .01, timesteps = 1000, soft_param = .1, disk2 = com_p, diskvel = com_v) # CHANGE TIMESTEPS HERE
### PLOT LAST TIMESTEP
MSG_plot(gal_posA = a, gal_posB = b, par_posA = c, particle_Na = 597, step = 999,  par_posB = d, particle_Nb = 324, tails = True, elev = 45, azim = 90)
```
### initial conditions to try
Z plane merger; recommended timesteps: 2000+
```python
pos = np.array([[4.0, 20.0, 10.0], [0.0, 0.0, 0.0]]) # bulge positions
vel = np.array([[0.0, -1.0, -0.7], [0.0, 0.0, 0.0]]) # bulge velocities
mas = np.array([[1.25], [4.0]]) # bulge masses
pos_p, vel_p, N = MSG_disk(7, 4, -1, 3) # primary disk
com_p, com_v, M = MSG_disk(3, 1.25, -1, 6, [4.0, 20.0, 10.0], [0.0, -1.0, -0.7]) # companion disk
```
XY plane merger; recommended timesteps 3000
```python
pos = np.array([[-15.0, 10.0, 0.0], [0.0, 0.0, 0.0]]) # bulge positions
vel = np.array([[1.5, 0.0, 0.0], [0.0, 0.0, 0.0]]) # bulge velocities
mas = np.array([[1.0], [3.0]]) # bulge masses
pos_p, vel_p, N = MSG_disk(7, 3, -1, 3) # primary disk
com_p, com_v, M = MSG_disk(3, 1.0, -1, 6, [-15.0, 10.0, 0.0], [1.5, 0.0, 0.0]) # companion disk
``` 

### setting up celluloid animations:
```python
### PLOT ANIMATION
try:
    import matplotlib.pyplot as plt
    from mpl_toolkits import mplot3d
    from celluloid import Camera
    from IPython.display import HTML

except:
    print('FATALE ERROR: please ensure celluloid and Ipython.display packages are pip installed \n /ᐠ=ᆽ=ᐟ\ <(hisss.....)')

# default camera viewing angles
elev = 45 # z viewing angle (0 = edge on; 90 = Bird's eye view)
azim = 90 # xy plane rotation angle


# make sure following values are integers
print('please input animation start and stop times; values must be integers within timestep range: ',' \n ex: \n start: 800 \n stop: 850')
start = int(input('animation start time: '))
stop = int(input('animation stop time: '))

# define figure
fig = plt.figure(figsize=(10, 10), dpi = 100)
ax = plt.axes(projection='3d')
camera = Camera(fig) # define celluloid camera

# formatting
plt.rcParams['font.family'] = 'sans-serif' # set font
# set border color to white
ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))

# set view angles
ax.view_init(elev = elev, azim = azim)
# set lables
ax.set_xlabel('\u03A7')
ax.set_ylabel('\u03A5')
ax.set_zlabel('Z')

for i in range(start, stop):
    # correct sclicing index
    end1 = N*i + N
    end2 = M*i + M

    ax.scatter3D(a[i,0], a[i,1], a[i,2], s = 100, color = 'darkslateblue') # bulge 1
    ax.scatter3D(b[i,0], b[i,1], b[i,2], s = 200, color = 'black') # bulge 2
    ax.scatter3D(c[N*i:end1,0], c[N*i:end1,1], c[N*i:end1,2], s = 15, color = 'darkorchid') # primary disk
    ax.scatter3D(d[M*i:end2,0], d[M*i:end2,1], d[M*i:end2,2], s = 15, color = 'slateblue') # companion disk 
    # save snapshots
    camera.snap()

animation = camera.animate() # compile snapshots
plt.close() # stop the empty plot from displaying
HTML(animation.to_html5_video()) # display animation
```

## matplotlib animations
this code works in jupyter notebooks and offers a non celluloid dependent alternative for plotting animations. place this code in a cell after the code found in the "running the code" section
```python
# create interactive plot
%matplotlib notebook
### MATPLOTLIB ANIMATION 
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import matplotlib.animation as animation

# default camera viewing angles
elev = 45 # z viewing angle (0 = edge on; 90 = Bird's eye view)
azim = 90 # xy plane rotation angle


# make sure following values are integers
print('please input animation start and stop times; values must be integers within timestep range: ',' \n ex: \n start: 800 \n stop: 850')
start = int(input('animation start time: '))
stop = int(input('animation stop time: '))

# define figure
fig = plt.figure(figsize=(10, 10), dpi = 100)
ax = plt.axes(projection='3d')

# formatting
plt.rcParams['font.family'] = 'sans-serif' # set font
# set border color to white
ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))

# set view angles
ax.view_init(elev = elev, azim = azim)
# set lables
ax.set_xlabel('\u03A7')
ax.set_ylabel('\u03A5')
ax.set_zlabel('Z')

# set up animation variables
b1, b2, p1, p2 = [], [], [], []
for i in range(start, stop):
    # correct slicing index
    end1 = N*i + N
    end2 = M*i + M
    # plot and append
    plota = ax.scatter3D(a[i,0], a[i,1], a[i,2], s = 100, color = 'darkslateblue') # bulges
    b1.append([plota])
    plotb = ax.scatter3D(b[i,0], b[i,1], b[i,2], s = 200, color = 'black') # bulge 1 
    b2.append([plotb])
    plotc = ax.scatter3D(c[N*i:end1,0], c[N*i:end1,1], c[N*i:end1,2], s = 15, color = 'darkorchid') # bulge 1 
    p1.append([plotc])
    plotd = ax.scatter3D(d[M*i:end2,0], d[M*i:end2,1], d[M*i:end2,2], s = 15, color = 'slateblue') # bulge 1 
    p2.append([plotd])
# create animations        
ani1 = animation.ArtistAnimation(fig, b1, interval=5, blit=False)
ani2 = animation.ArtistAnimation(fig, b2, interval=5, blit=False)
ani3 = animation.ArtistAnimation(fig, p1, interval=5, blit=False)
ani4 = animation.ArtistAnimation(fig, p2, interval=5, blit=False)
plt.show()
```
## Requirements
<br>numpy, matplotlib, random
<br>OPTIONAL: celluloid, IPython.display
## Acknowledgements
<br>Thank you to Professor Marla Geha and Will Cerny for their help. This project would have not been possible without them! =^._.^=
