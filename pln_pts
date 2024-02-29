"""Grasshopper Script"""
# Best Fit Plane from Points
# Copyright (C) 2024 Yan Peng <pydeoxy@gmail.com>

# This code is for a Python 3 Script component in Grasshopper with Rhino 8.
# To use this code, just copy the whole content into a Python 3 Script Script component,
# and to change the INPUTs and OUTPUTs according to the Args and Returns.
# Or, just use the pln_pts_example.gh file.

# This componet is to generate the best fit plane for a group of points.
# The output include the plane and the points with new z-coordinates on the best fit plane.
# Linear regression is used to find the plane's coefficients.

"""
Best Fit Plane from Points.
    Find the best fit plane for a group of points with linear regression.

Args:
    pts: The points to fit.    

Returns:
    plane: The best fit plane.
    pts_new: The points with new z-coordinates on the best fit plane.
    
"""

__author__ = "yan.peng"
__version__ = "2024.02.29"

import numpy as np
import Rhino as rh

def pln_pts(pts):
    
    # Convert the coordinates of points into numpy array
    pts_array = np.array([[pt[0],pt[1],pt[2]] for pt in pts])
    # Using matrices, vectors and linear regression to calculate the planes coefficients
    x= np.c_[pts_array[:, :2], np.ones(len(pts))]
    y = pts_array[:, 2].flatten()
    c = np.linalg.lstsq(x, y)[0]

    # Create plane from the coefficients
    c_z = np.insert(c, 2, -1)
    co_l = c_z.tolist()
    pl = rh.Geometry.Plane(co_l[0],co_l[1],co_l[2],co_l[3])

    # Get the new points on the plane
    new_z = x @ c
    pts_arr = np.c_[pts_array[:, :2], new_z]
    pts_coor = pts_arr.tolist()
    ptns = []
    for p in pts_coor:
        ptn = rh.Geometry.Point3d(p[0],p[1],p[2])
        ptns.append(ptn)

    return pl, ptns

pts_n = pln_pts(pts)[1]
pln = pln_pts(pts)[0]
