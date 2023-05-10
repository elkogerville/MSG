def MSG_disk(number_of_rings, mass, rotation_dir, density, origin = ([[0.,0.,0.]]), velocity = ([[0.,0.,0.]])):
    """
    this function calculates the x, y position and velocities for each particle in the galactic disk centered
    around the origin by default
    ----------------------------------------------------------------------
    number_of_rings [integer]: specifies number of rings in galactic plane
    
    mass [float]: mass of bulge, used to calculate velocities
    
    rotation_dir [integer]: either 1 or -1 for CCW [1] and CW [-1] disk rotation
    can be used as a scaling factor for velocities [ei. -2], however can lead to exceeding escape velocity
    
    density [float]: scales particle ring density using the equation y = density * (6x + 6)
    default of density = 1 recreates the TOOMRE and TOOMRE simulation particle density
    
    origin [numpy array]: centers the disk at these x,y,z coordinates
    must be set to same x,y,z postion as host galaxy bulge 
    format: np.array([[X, Y, Z]])
    
    velocity [numpy array]: corrects galactic disk particle velocities to match constant velocity of bulge
    must be set to same x,y,z velocity as host galaxy bulge
    format: np.array([[Vx, Vy, Vz]])
    ----------------------------------------------------------------------------------
    OUTPUT [numpy array]: particle_positions, particle_velocities, number_of_particles
    format: function returns 2, (N, 3) numpy arrays and a integer (# of particles)
    example: par_pos, par_vel, N = MSG_galaxy(*args)
    =^._.^=
    """
    
    import numpy as np # computational
    import random # necessary...
    
    def particles_per_ring(ring_number, scale_factor):
        """this function calculates the amount of particles for each ring using the equation y = 6x+6
        Using the default scale_factor of 1 will scale the number of particles per ring like TOOMRE et al. (1972)"""
        def particle_count(i, scale_factor):
            # outputs y = 6x + 6 for a given x
            return int(scale_factor * (6*i + 6)) # ensures only integer amount of particles
        
        Num = np.zeros((ring_number, 1)) # create (x by 1) array, where x is number of rings in disk
        Npar = np.zeros(1) # array for storing
        for n in range(ring_number): # loop through specified amount of rings in disk
            Num[n] = particle_count(n+1, scale_factor) # calculate number of particles for each ring
            Npar = np.append(Npar, Num[n], 0) # append number of particles into array
        return Npar[1:] # remove zeroth entry
    
    def init(RING_NUMB, MASS):
        """this function calculates the radius and velocity for each ring in the galaxy disk"""
        def calc_rad(i):
            """this function calculates the radius for a given ring assuming rings are equally spaced"""
            radius = i * 600/500 # distance between rings [parsecs] / number of parsecs in 1 distance unit
            return radius
        
        def get_velocity(RADIUS, M):
            """this function calculates the magnitude of the velocity for a given radius"""
            G = 1 # gravitational constant
            M = M # mass of host galaxy
            #calculate magnitude of velocity at given radius
            ring_vel = np.sqrt(G * M / RADIUS) # circular keplerian orbital velocity
            return ring_vel
        
        # generate radii and velocity for each ring
        rarr = np.zeros(RING_NUMB)
        varr = np.zeros(RING_NUMB)
        for r in range(1, RING_NUMB + 1): # loop starts at 1 to avoid radius of 0
            rarr[r-1] = calc_rad(r) # index starts at r-1 to overwrite 0th entry
            varr[r-1] = get_velocity(rarr[r-1], MASS) # calculate velocity using calculated radius
        return rarr, varr
    
    def galaxy(RADIUS, VELOCITY, PARTICLE_NUMBER):
        """this function generates positions and velocities for each particle, confined to orbit in xy plane"""
        # calculate angular spacing in radians to space each particle equally 
        angular_spacing = (360 * np.pi)/(PARTICLE_NUMBER * 180) 
        
        par_arr = np.zeros((PARTICLE_NUMBER, 3)) #initialize array for storing position values
        vel_arr = np.zeros((PARTICLE_NUMBER, 3)) #initialize array for storing velocity values
        for N in range(PARTICLE_NUMBER): # loop through number of particles in a given ring
            # calculate x, y positions and velocities for each particle
            X = RADIUS * np.cos(angular_spacing * N)
            Y = RADIUS * np.sin(angular_spacing * N)
            Vx = - VELOCITY * np.sin(angular_spacing * N) # neg sign ensures velocity vector points in correct direction
            Vy = VELOCITY * np.cos(angular_spacing * N)
            # store x and y values
            par_arr[N, 0] = X
            par_arr[N, 1] = Y
            vel_arr[N, 0] = Vx
            vel_arr[N, 1] = Vy
        return par_arr, vel_arr
    
    # ensure values are integers
    number_of_rings = int(number_of_rings)
    
    # number of particles per ring
    PAR_PER_RING = particles_per_ring(number_of_rings, density)
    Np = int(sum(PAR_PER_RING)) # total number of particles

    rand = random.randint(0, 5) # generate integer between 0 and 6 randomly
    if rand == 0:
        print('total number of particles: ', Np , '\n ﾐᐠዋ ﻌ ዋᐟﾐ') # tiger
    if rand == 1:
        print('total number of particles: ', Np , '\n /ᐠ｡ꞈ｡ᐟ\ ᨐ') # tiny cat
    if rand == 2:
        print('total number of particles: ', Np , '\n /ᐠ ̥ ̮ ̥ᐟ\ฅ  ฅ/ᐠ‧̫‧ᐟ\ฅ  ฅ/ᐠ. ̫.ᐟ\ฅ') # 3 kitties
    if rand == 3:
        print('total number of particles: ', Np , '\n =^._.^=') # awesome cat
    if rand == 4:
        print('total number of particles: ', Np , '\n (๑ↀᆺↀ๑)') # cool cat
    if rand == 5:
        print('total number of particles: ', Np , '\n ∧,,,∧ \n( ̳•·• ̳)\n/    づ💻') # izzy's cat
        
    # generate radii and velocities for each ring
    radii, velocities = init(number_of_rings, mass)

    # set up final position array
    final_pos = np.zeros((1, 3))
    final_vel = np.zeros((1, 3))
    
    # loop through each ring to generate positions and velocities for each particle in each ring
    for numb in range(number_of_rings):
        XY, Vxy = galaxy(radii[numb], velocities[numb], int(PAR_PER_RING[numb])) # ensure only integer # of particles
        final_pos = np.append(final_pos, XY, 0) # store positions
        final_vel = np.append(final_vel, Vxy, 0) # store velocities
        
    # remove 0th entry, and adjust disk rotation direction, bulge position and velocity
    final_pos = final_pos[1:] + origin # shift positions to be centered around 'origin'
    final_vel = rotation_dir * final_vel[1:] + velocity # shift velocities
    
    return final_pos, final_vel, Np # outputs positions, velocities and number of particles
