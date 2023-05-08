# Merging Simulator for Galaxies [MSG]
<br> This python code simulates the motion of massless test particles (galactic disk) through a gravitational potential field created by 2 galactic bulges. This restricted N-Body simulation is modeled after the Toomre and Toomre 1972 simulations and allows for 3D visualization of galaxy mergers.
<br>
<br>
## running the code:
```python
### IMPORT STATEMENTS
from MSGpy import MSGgalaxy
from MSGpy import MSGdisk
from MSGpy import MSGplot
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
                        dt = .01, timesteps = 1000, soft_param = .1, disk2 = com_p, diskvel = com_v)
### PLOT LAST TIMESTEP
MSG_plot(gal_posA = a, gal_posB = b, par_posA = c, particle_Na = 597, step = 999,  par_posB = d, particle_Nb = 324, tails = True, elev = 45, azim = 90)
```
