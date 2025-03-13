# this module creates an interpolator in the grid of mr_all_2024

import numpy as np 
from scipy.interpolate import RegularGridInterpolator

# Load the data
path_models = "./models/"

# open files
list_met_lf14,list_age_lf14,list_finc_lf14,list_m_lf14,list_fenv_lf14,list_r_lf14 = np.loadtxt(path_models+"LF2014.dat",skiprows=11,unpack=True,usecols=(0,1,2,3,4,5))

dim_met_lf14 = np.array([1.0,50.0])
dim_age_lf14 = np.array([0.1,1.0,10.0])
dim_finc_lf14= np.array([0.1,10.0,1000.0])
dim_teq_lf14 = 278.0*(dim_finc_lf14)**(0.25)
dim_mass_lf14= np.array([1,1.5,2.4,3.6,5.5,8.5,13,20])
dim_fenv_lf14= np.array([0.01,0.02,0.05,0.1,0.2,0.5,1.0,2.0,5.0,10.0,20.0])

data_r_lf14 = np.reshape(list_r_lf14,(2,3,3,8,11))

interp_lf14 = RegularGridInterpolator((dim_met_lf14, dim_age_lf14, dim_teq_lf14, dim_mass_lf14, dim_fenv_lf14), data_r_lf14, method='linear', bounds_error=False, fill_value=np.inf)


#computes the radius of a planet, using the model from Lopez & Fortney 2014
#the planet input should contain:
# - atmosphere metallicity (met)
# - system age (age, in Gyr)
# - planet envelope mass fraction (fenv)
# - planet equilibrium temperature (teq)
# - planet mass (mp)
def radius_lf14(met,age,fenv,teq,mp):
    # If all parameters are scalars, evaluate and return a single value
    if isinstance(met, (float, int)) and isinstance(age, (float, int)) and isinstance(fenv, (float, int)) and isinstance(teq, (float, int)) and isinstance(mp, (float, int)):
        return interp_lf14((met,age,teq,mp,fenv)).item()
    
    # If all are arrays of the same length, evaluate for each set of parameters
    elif isinstance(met, np.ndarray) and isinstance(age, np.ndarray) and isinstance(fenv, np.ndarray) and isinstance(teq, np.ndarray) and isinstance(mp, np.ndarray):
        if len(met) == len(age) == len(fenv) == len(teq) == len(mp):
            points = np.array([met,age,teq,mp,fenv]).T  # Stack the arrays into a 2D array of points
            return interp_lf14(points)  # This will return an array of results
        else:
            raise ValueError("Input arrays must have the same length.")
    
    # Handle invalid input types
    else:
        raise ValueError("Inputs must either be scalars or arrays of the same length.")
