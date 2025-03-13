# this module creates an interpolator in the grid of mr_all_2024

import numpy as np 
from scipy.interpolate import RegularGridInterpolator

# Load the data
path_models = "./models/"

path_aguichine = path_models + "Aguichine2021_mr_all_2024.dat"

listmbfull,listmafull,listrbfull,listrafull,listerrfull = np.loadtxt(path_aguichine,unpack=True,usecols=(4,5,6,7,8))

# Make IOP interpolator

dimcmf = np.linspace(0.0,0.9,10)
dimwmf = np.linspace(0.0,1.0,11)
dimteq = np.linspace(400.0,1300.0,10)
dimmass = np.logspace(np.log10(0.2),np.log10(20.0),20)

data_radius = np.transpose( np.reshape(listrbfull+listrafull,(10,10,11,20)) , (0,2,1,3))
data_errcode = np.transpose( np.reshape(listerrfull,(10,10,11,20)) , (0,2,1,3))

interp_radius_iop = RegularGridInterpolator((dimcmf, dimwmf, dimteq, dimmass), data_radius, method='linear', bounds_error=False, fill_value=None)
interp_errcode_iop = RegularGridInterpolator((dimcmf, dimwmf, dimteq, dimmass), data_errcode, method='linear', bounds_error=False, fill_value=None)

#computes the radius of a planet, using the IOP model from Aguichine+2021
#the planet input should contain:
# - planet reduced core mass fraction (cmf') - defined as M(iron core)/M(iron core + silicate mantle)
# - planet water mass fraction (wmf)
# - planet mass (mp)
# - planet equilibrium temperature (teq)
def radius_iop(cmf,wmf,teq,mp):
    # If all parameters are scalars, evaluate and return a single value
    if isinstance(cmf, (float, int)) and isinstance(wmf, (float, int)) and isinstance(teq, (float, int)) and isinstance(mp, (float, int)):
        return interp_radius_iop((cmf, wmf, teq, mp)).item()
    
    # If all are arrays of the same length, evaluate for each set of parameters
    elif isinstance(cmf, np.ndarray) and isinstance(wmf, np.ndarray) and isinstance(teq, np.ndarray) and isinstance(mp, np.ndarray):
        if len(cmf) == len(wmf) == len(teq) == len(mp):
            points = np.array([cmf, wmf, teq, mp]).T  # Stack the arrays into a 2D array of points
            return interp_radius_iop(points)  # This will return an array of results
        else:
            raise ValueError("Input arrays must have the same length.")
    
    # Handle invalid input types
    else:
        raise ValueError("Inputs must either be scalars or arrays of the same length.")


#determines if the radius from the IOP model is valid or not
# returns 0 if all data points are valid
# returns >0 if one or more data points are not valid
def error_iop(cmf,wmf,teq,mp):
    # If all parameters are scalars, evaluate and return a single value
    if isinstance(cmf, (float, int)) and isinstance(wmf, (float, int)) and isinstance(teq, (float, int)) and isinstance(mp, (float, int)):
        return interp_errcode_iop((cmf, wmf, teq, mp)).item()
    
    # If all are arrays of the same length, evaluate for each set of parameters
    elif isinstance(cmf, np.ndarray) and isinstance(wmf, np.ndarray) and isinstance(teq, np.ndarray) and isinstance(mp, np.ndarray):
        if len(cmf) == len(wmf) == len(teq) == len(mp):
            points = np.array([cmf, wmf, teq, mp]).T  # Stack the arrays into a 2D array of points
            return interp_errcode_iop(points)  # This will return an array of results
        else:
            raise ValueError("Input arrays must have the same length.")
    
    # Handle invalid input types
    else:
        raise ValueError("Inputs must either be scalars or arrays of the same length.")


