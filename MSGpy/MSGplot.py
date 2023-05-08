def MSG_plot(gal_posA, gal_posB, par_posA, particle_Na, step, par_posB = None, particle_Nb = None, tails = None,
             **kwargs):
    """this function plots the positions of all particles at a given timestep
    ---------------------------------------------------------------------------
    gal_posA [numpy array]: outputed x,y,z positions for companion galaxy bulge 
    shape: (timesteps, 3)
    
    gal_posB [numpy array]: outputed x,y,z positions for primary galaxy bulge 
    shape: (timesteps, 3)
    
    par_posA [numpy array]: outputed x,y,z positions for primary galaxy disk
    shape: (X, 3) 
    X = timesteps * particle_Na + particle_Na
    
    particle_Na [integer]: number of particles in primary galaxy disk
    
    step [integer]: simulation step to be plotted; must be within simulation timestep range
    ---------------------------------------------------------------------------------------
    [OPTIONAL]:
    par_posB [numpy array]: outputed x,y,z positions for companion galaxy disk
    by default set to None. if array is provided, please also defined particle_Nb
    shape: (Y, 3)
    Y = timesteps * particle_Nb + particle_Nb
    
    particle_Nb [integer]: number of particles in companion galaxy disk
    
    tails [boolean]: if True, will plot companion bulge trail showing motion through space, starting at 
    timestep = 0 to timestep = step
    
    [**kwargs]:
    elev [float / integer]: sets z height camera viewing angle; can be float or integer
    0 = edge on; 90 = bird's eye view
    
    azim [float / integer]: sets azimuthal camera pan angle; can be float or integer
    0 = facing yz plane, 90 = facing xz plane
    -------------------------------------------------------------------------------------------------------------
    OUTPUT [matplotlib 3d plot]: yay!!! simulation visualized <|:^0 
    in jupyter notebook add " %matplotlib notebook " at the top of cell to make plot interactive and drag mouse on plot to pan camera! 
    =^._.^= 
    """
    
    # import plotting packages
    import matplotlib.pyplot as plt
    from mpl_toolkits import mplot3d

    # default camera viewing angles
    elev = 45 # z viewing angle (0 = edge on; 90 = Bird's eye view)
    azim = 90 # xy plane rotation angle
    
    # change viewing angles if in **kwargs
    if ('elev') in kwargs:
        elev = kwargs['elev']
    if ('azim') in kwargs:
        azim = kwargs['azim']
        
    # if plotting particles for companion disk, number of particles in companion disk must be defined
    if par_posB is not None:
        if particle_Nb is None:
            print('FATALE ERROR: please ensure both disk2 positions [par_posB] and disk2 paritcle count [particle_Nb] are defined \n /ᐠ_ ꞈ _ᐟ\ <(fix it...)')
            return
        print('ploting....  \n[^._.^]')
        # make sure step is integer
        step = int(step)
        # shift step by number of particles for correct slicing
        stepA = int(particle_Na * step)
        endA = int(stepA + particle_Na)
        stepB = int(particle_Nb * step)
        endB = int(stepB + particle_Nb)

        # define figure
        fig = plt.figure(figsize=(10,10), dpi = 100) # create figure
        ax = plt.axes(projection='3d') # 3d plot

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
        
        # plot galaxy bulges and disks
        ax.scatter3D(gal_posA[step,0], gal_posA[step,1], gal_posA[step,2], s = 300, color = 'darkslateblue') # bulge 1
        ax.scatter3D(gal_posB[step,0], gal_posB[step,1], gal_posB[step,2], s = 300, color = 'black') # bulge 2
        ax.scatter3D(par_posA[stepA:endA,0], par_posA[stepA:endA,1], par_posA[stepA:endA,2], s = 15, color = 'orchid') # particles 
        ax.scatter3D(par_posB[stepB:endB,0], par_posB[stepB:endB,1], par_posB[stepB:endB,2], s = 15, color = 'mediumslateblue') # particles 
        
        if tails is not None:
            ax.scatter3D(gal_posA[:step,0], gal_posA[:step,1], gal_posA[:step,2], s = 15, color = 'darkslateblue', 
                         alpha = .05) # bulge 1
        plt.show()
        
    else:
        print('ploting....  \n [^._.^]')
        # make sure step is integer
        step = int(step)
        # shift step by number of particles for correct slicing
        stepA = int(particle_Na * step)
        endA = int(stepA + particle_Na)

        # define figure
        fig = plt.figure(figsize=(10,10), dpi = 100) # create figure
        ax = plt.axes(projection='3d') # 3d plot

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
        
        # plot galaxy bulges and disks
        ax.scatter3D(gal_posA[step,0], gal_posA[step,1], gal_posA[step,2], s = 300, color = 'darkslateblue') # bulge 1
        ax.scatter3D(gal_posB[step,0], gal_posB[step,1], gal_posB[step,2], s = 300, color = 'black') # bulge 2
        ax.scatter3D(par_posA[stepA:endA,0], par_posA[stepA:endA,1], par_posA[stepA:endA,2], s = 15, color = 'orchid') # particles 
        
        if tails is not None:
            ax.scatter3D(gal_posA[:step,0], gal_posA[:step,1], gal_posA[:step,2], s = 15, color = 'darkslateblue', 
                         alpha = .05) # bulge 1
        plt.show()
