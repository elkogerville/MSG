def MSG_rotate(gal_pos, gal_vel, par_pos, par_vel, theta, Xrot = None, Yrot = None, Zrot = None, 
               pos_shift = [0.,0.,0.], vel_shift = [0.,0.,0.]):
    """
    this function rotates the x, y, z positions and velocities of a disk to add disk inclination
    --------------------------------------------------------------------------------------------
    gal_pos [numpy array]: x, y, z bulge positions to be rotated
    
    gal_vel [numpy array]: x, y, z bulge velocities to be rotated
    
    par_pos [numpy array]: x, y, z disk positions to be rotated
    
    par_vel [numpy array]: x, y, z disk velocities to be rotated
    
    velocities [numpy array]: x, y, z velocities to be rotated
    
    theta [float]: angle of rotation in degrees
    
    Xrot, Yrot, Zrot [boolean]: by default set to None; set one to True to perform rotation about respective axis
    
    pos_shift [numpy array]: center of galaxy disk
    
    vel_shift [numpy array]: initial velocity for galaxy bulge
    -------------------------------------------------------------------------------------------------------------
    OUTPUT [numpy array]: rotated x, y, z positions and velocities
    example: perform 90º rotation about X axis
    rotated_pos, rotated_vel = Rotation_Matrix(positions, 90, Xrot = True)
    """
    import numpy as np # computational
    radian = theta * (np.pi / 180)
    
    # X AXIS ROTATION
    if Xrot is not None: 
        if Yrot or Zrot is not None: # ensure only one axis of rotation is given
            print('ERROR: please only specify one axis of rotation; set only one axis of rotation to True \n /ᐠ=ᆽ=ᐟ\ <(hisss.....)')
            raise SystemExit # exit program if error is raised
        # x axis rotation matrix
        R_x = np.array([[1., 0., 0.], [0., np.cos(radian), -np.sin(radian)], [0., np.sin(radian), np.cos(radian)]])
        # shift position and velocities to disk centered around 0,0,0 at rest
        GP_diff = gal_pos - pos_shift
        GV_diff = gal_vel - vel_shift
        PP_diff = par_pos - pos_shift   
        PV_diff = par_vel - vel_shift
        # matrix dot product to rotate pos, vel
        A, B, C, D = GP_diff @ R_x, GV_diff @ R_x, PP_diff @ R_x, PV_diff @ R_x
        # translate disk positions and velocities back to original state
        return A + pos_shift, B + vel_shift, C + pos_shift, D + vel_shift

    # Y AXIS ROTATION
    if Yrot is not None:
        if Xrot or Zrot is not None: # ensure only one axis of rotation is given
            print('ERROR: please only specify one axis of rotation; set only one axis of rotation to True \n /ᐠ=ᆽ=ᐟ\ <(hisss.....)')
            raise SystemExit # exit program if error is raised
        # y axis rotation matrix
        R_y = np.array([[np.cos(radian), 0., np.sin(radian)], [0., 1., 0.], [-np.sin(radian), 0., np.cos(radian)]])
        # shift position and velocities to disk centered around 0,0,0 at rest
        GP_diff = gal_pos - pos_shift
        GV_diff = gal_vel - vel_shift
        PP_diff = par_pos - pos_shift   
        PV_diff = par_vel - vel_shift
        # matrix dot product to rotate pos, vel
        A, B, C, D = GP_diff @ R_y, GV_diff @ R_y, PP_diff @ R_y, PV_diff @ R_y
        # translate disk positions and velocities back to original state
        return A + pos_shift, B + vel_shift, C + pos_shift, D + vel_shift
   
    # Z AXIS ROTATION
    if Zrot is not None:
        if Xrot or Yrot is not None: # ensure only one axis of rotation is given
            print('ERROR: please only specify one axis of rotation; set only one axis of rotation to True \n /ᐠ=ᆽ=ᐟ\ <(hisss.....)')
            raise SystemExit # exit program if error is raised
        # z axis rotation matrix
        R_z = np.array([[np.cos(radian), -np.sin(radian), 0.], [np.sin(radian), np.cos(radian), 0.], [0., 0., 1.]])
        # shift position and velocities to disk centered around 0,0,0 at rest
        GP_diff = gal_pos - pos_shift
        GV_diff = gal_vel - vel_shift
        PP_diff = par_pos - pos_shift   
        PV_diff = par_vel - vel_shift
        # matrix dot product to rotate pos, vel
        A, B, C, D = GP_diff @ R_z, GV_diff @ R_z, PP_diff @ R_z, PV_diff @ R_z
        # translate disk positions and velocities back to original state
        return A + pos_shift, B + vel_shift, C + pos_shift, D + vel_shift

    # ensure axis of rotation is specified
    else:
        print('ERROR: please specify which axis of rotation is required \n /ᐠ=ᆽ=ᐟ\ <(hisss.....)')
        raise SystemExit