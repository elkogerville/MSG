def MSG_galaxy(gal_pos, gal_vel, mass, particle_pos, particle_vel, dt, timesteps, soft_param, 
               disk2 = None, diskvel = None):
    """
    [MegingSimulator:Galaxies]
    this function runs a restricted N-Body simulation given initial positions and velocities and outputs the 
    positions of each particle after n timesteps
    -----------------------------------------------------------------------------------------------------------
    gal_pos [numpy array]: initial x,y,z positions of the two massive particles representing the galactic bulge
    format: np.array([[X1, Y1, Z1], [X2, Y2, Z2]])
    data type: float
    shape: (2, 3)
    
    gal_vel [numpy array]: initial x,y,z velocities of the two massive particles representing the galactic bulge
    format: np.array([[Vx1, Vy1, Vz1], [Vx2, Vy2, Vz2]])
    data type: float
    shape: (2, 3)
    
    mass [numpy array]: mass of 'galactic bulges'
    format: np.array([[M1], [M2]])
    data type: float
    shape: (2, 1)
    
    particle_pos [numpy array]: initial x,y,z positions of each massless test particle in galactic disk
    format: np.array([[X1, Y1, Z1], [X2, Y2, Z2], ... , [Xn, Yn, Zn]])
    data type: float
    shape: (N, 3)
    
    particle_vel [numpy array]: initial x,y,z velocities of each massless test particle
    format: np.array([Vx1, Vy1, Vz1], [Vx2, Vy2, Vz2], ... , [Vxn, Vyn, Vzn]])
    data type: float
    shape: (N, 3)
    
    dt [float]: timescale interval for simulation
    example: .001
    
    timesteps [float]: number of timesteps
    example: 1000
    
    soft_param [float]: softening parameter for Plummer Potential 
    example = .1
    ------------------------------------------------------------------------------------------------------------
    [OPTIONAL]: by providing disk2 and diskvel, you can seperately calculate the positions of the companion disk
    test particles to output them in a seperate array, allowing for different color settings when plotting
    
    disk2 [numpy array]: initial x,y,z positions of each massless test particle in companion disk
    by default set to None, if provided please also define diskvel in function
    format: np.array([[X1, Y1, Z1], [X2, Y2, Z2], ... , [Xm, Ym, Zm]])
    data type: float
    shape: (M, 3)
    
    diskvel [numpy array]: initial x,y,z velocities of each massless test particle in companion disk
    by default set to None
    format: np.array([Vx1, Vy1, Vz1], [Vx2, Vy2, Vz2], ... , [Vxm, Vym, Vzm]])
    data type: float
    shape: (M, 3)
    ---------------------------------------------------------------------------
    OUTPUT [numpy array]: Bulge_1_position, Bulge_2_position, Particle_position
    format: function returns 3, (N, 3) numpy arrays
    example: bulge_a, bulge_b, particles = MSG_galaxy(*args)
    if disk2 and diskvel are provided, will output a second Particle_position array
    =^._.^=
    """
    
    # IMPORT STATEMENTS
    import numpy as np #computational
    
    # FUNCTIONS
    def accelerator(POSITION, MASS, Sf):
        """this function calculates the gravitational acceleration for the two massive particles"""
        # gravitational constant
        G = 1
        # number of particles from position array
        N = POSITION.shape[0]
        # empty acceleration 3-dimensional array for storing accelerations
        a = np.zeros((N,3))
        del_x, del_y, del_z = [],[],[]

        # calculate acceleration for each particle
        for i in range(N):
            for k in range(N):
                # vectorized form of GMm/r**2
                delx = POSITION[k,0] - POSITION[i,0] 
                dely = POSITION[k,1] - POSITION[i,1]
                delz = POSITION[k,2] - POSITION[i,2]

                g = (delx**2 + dely**2 + delz**2 + Sf**2)**(-1.5)
                
                #store each acceleration component
                a[i, 0] += G * (delx * g) * MASS[k]
                a[i, 1] += G * (dely * g) * MASS[k]
                a[i, 2] += G * (delz * g) * MASS[k]

        return np.array(a)
    
    def particle_init(POS_GAL, POS_P, MASS, Sf):
        """this function calculates the acceleration induced by a gravitational potential field onto test particles"""
        # gravitational constant
        G = 1
        # number of massless particles
        N = POS_P.shape[0]

        # empty 3-dimensional arrays for storing accelerations, assuming 2 massive 'bulges'
        Aa = np.zeros((N,3))
        Ab = np.zeros((N,3))

        del_xa, del_ya, del_za = [],[],[]
        del_xb, del_yb, del_zb = [],[],[] 

        # calculate acceleration for each particle by looping through them
        for i in range(len(POS_P)):
            # galaxy a
            delxa = POS_GAL[0, 0] - POS_P[i, 0]
            delya = POS_GAL[0, 1] - POS_P[i, 1]
            delza = POS_GAL[0, 2] - POS_P[i, 2] 
            # galaxy b
            delxb = POS_GAL[1, 0] - POS_P[i, 0]
            delyb = POS_GAL[1, 1] - POS_P[i, 1] 
            delzb = POS_GAL[1, 2] - POS_P[i, 2] 

            ga = (delxa**2 + delya**2 + delza**2 + Sf**2)**(-1.5)
            gb = (delxb**2 + delyb**2 + delzb**2 + Sf**2)**(-1.5) 
            
            # save accelerations to array
            Aa[i, 0] += G * (delxa * ga) * MASS[0, 0]
            Aa[i, 1] += G * (delya * ga) * MASS[0, 0]
            Aa[i, 2] += G * (delza * ga) * MASS[0, 0]

            Ab[i, 0] += G * (delxb * gb) * MASS[1, 0]
            Ab[i, 1] += G * (delyb * gb) * MASS[1, 0]
            Ab[i, 2] += G * (delzb * gb) * MASS[1, 0]

        return np.array(Aa + Ab) # sum accelerations 
    
    # ensure values are integers
    timesteps = int(timesteps)
    
    # initialize position arrays for plotting
    pos_arr1, pos_arr2 = np.zeros((timesteps, 3)), np.zeros((timesteps, 3))
    pos_arr1[0], pos_arr2[0] = gal_pos[0], gal_pos[1]
    particle_arr = particle_pos

    
    # calculate initial accelerations 
    gal_accel = accelerator(gal_pos, mass, soft_param)
    particle_accel = particle_init(gal_pos, particle_pos, mass, soft_param)
    
    # check if companion galaxy has test particles
    if disk2 is not None: 
        # calculate initial accelerations for second galaxy
        disk_accel = particle_init(gal_pos, disk2, mass, soft_param)
        disk2_arr = disk2
    
    print('simulation running....  /ᐠ –ꞈ –ᐟ\<[pls be patient]')
    # simulation code
    for n in range(timesteps): # loop through every timestep
                         
        # GALAXIES
        # calculate velocity using acceleration and 1/2 timestep
        gal_vel += gal_accel * dt/2.0

        # drift particle
        gal_pos += gal_vel * dt
        
        # store positions from timestep into array
        pos_arr1[n], pos_arr2[n] = gal_pos[0], gal_pos[1] 
        
        # update accelerations
        gal_accel = accelerator(gal_pos, mass, soft_param)
    
        # update velocities
        gal_vel += gal_accel * dt/2.0
        
        # PARTICLES
        # calculate velocity using acceleration and 1/2 timestep
        particle_vel += particle_accel * dt/2.0
    
        # drift particle
        particle_pos += particle_vel * dt

        # store positions from timestep into array
        particle_arr = np.append(particle_arr, particle_pos, 0)
    
        # update accelerations
        particle_accel = particle_init(gal_pos, particle_pos, mass, soft_param)
    
        # update velocities
        particle_vel += particle_accel * dt/2.0
        
        # check if companion galaxy has particles
        if disk2 is not None: 
            # repeat above calculations onto companion disk particles
            diskvel += disk_accel * dt/2.0 # calculate velocities
            disk2 += diskvel * dt # calculate positions
            disk2_arr = np.append(disk2_arr, disk2, 0) # store positions
            disk_accel = particle_init(gal_pos, disk2, mass, soft_param) # update accelerations
            diskvel += disk_accel * dt/2.0 # update velocity
    
    print('simulation complete [yay!!! (ﾐΦ ﻌ Φﾐ)✿ *ᵖᵘʳʳ*]')
    # output position arrays
    if disk2 is not None:
        # if companion galaxy has stars, output 4 position arrays; 1 for each bulge, and 1 for each disk
        return pos_arr1, pos_arr2, particle_arr, disk2_arr
    else:
        # if companion galaxy does not have stars, output one less array
        return pos_arr1, pos_arr2, particle_arr