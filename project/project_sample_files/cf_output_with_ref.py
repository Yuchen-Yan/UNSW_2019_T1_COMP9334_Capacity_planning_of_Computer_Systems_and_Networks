#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMP9334 Project sample file 

Compare output files. 

Comapre mrt_*.txt, fog_dep_*.txt against their  
reference version for * = 1, 2 and 3. 

This file assume mrt_*.txt, fog_dep_*.txt  
and their reference files
are in the same directory

@author: ctchou
"""

# import numpy for easy comparison 
import numpy as np

# Definitions
file_ext = '.txt' # File extension
TOL = 1e-3  # Absolute tolerance 

# Loop through Tests 1 to 3
for t in range(1,4):
    # Compare mrt against the reference
    mrt_stu = np.loadtxt('mrt_'+str(t)+file_ext)
    mrt_ref = np.loadtxt('mrt_'+str(t)+'_ref'+file_ext)
    
    if np.isclose(mrt_stu,mrt_ref,atol=TOL):
        print('Test '+str(t)+': Mean response time matches the reference')
    else: 
        print('Test '+str(t)+': Mean response time does NOT match the reference')

    # Compare fog_dep against the reference
    fog_dep_stu = np.loadtxt('fog_dep_'+str(t)+file_ext)
    fog_dep_ref = np.loadtxt('fog_dep_'+str(t)+'_ref'+file_ext)
    
    if np.all(np.isclose(fog_dep_stu,fog_dep_ref,atol=TOL)):
        print('Test '+str(t)+': Fog departure times matche the reference')
    else: 
        print('Test '+str(t)+': Fog departure times do NOT match the reference')

