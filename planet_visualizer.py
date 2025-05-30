# Emerson's Planet Evolution Visualizer!
#   Download a copy of this file to use.
#   ASTR 9, Spring 2025

import numpy as np
import matplotlib.pyplot as plt

# constants
Gyr = 3.15e16       #Seconds in 1 Gyr
M_e = 5.97237e24    #Earth mass (kg)
R_e = 6.371e6       #Earth radius (m)


# --- LOAD IN YOUR DATA ------------------ #
# Data should be imported in mkgs units (meters, kilograms, seconds)
# location = './evolution-data/gp-evo/5000_xp/' #I used one of my generated planets
# file = 'planet_999-5000_evolution_data.csv'

location = './'     # local path to your data--
                    # don't change if data + script are in the same folder
file = 'TOI_178b_evolution.csv' # <-replace with your file name
path = location + file
print('Path:', path)

planet = 'TOI 178b' # name of your planet

time, mass, radius, wmf = np.loadtxt(path,\
                               usecols=(0,1,2,3),unpack=True)  # we only need these 4
print(f'Loading {planet} data.')


# --- DATA TABLE ------------------------- #
# I like viewing my planet data in a table through astropy,
# but feel free to comment this section
from astropy.table import Table
print('\nPLANET INFORMATION:',planet)
ptable = Table()
ptable["Time (Gyr)"] = time #/Gyr
ptable["Mass (M🜨)"] = mass #/M_e
ptable["Radius (R🜨)"] = radius #/R_e
ptable["WMF"] = wmf

ptable["Time (Gyr)"].format = "{:.3f}"
ptable["Mass (M🜨)"].format = "{:.3f}"
ptable["Radius (R🜨)"].format = "{:.3f}"
ptable["WMF"].format = "{:.3f}"
print(ptable)
print(f'Data loaded.')


# --- PLOTS ------------------------------ #

# 1. Visualizer (not necessary) ---------- #
# Fraction of initial value rather than the
# triple axes thing. since I'm lazy
# Un-comment the savefig line to download the plot locally
plt.plot(time,mass/mass[0], c='sienna',lw=3, label='mass')
plt.plot(time,radius/radius[0], c='olivedrab', ls='--', lw=3, label='radius')
plt.plot(time,wmf/wmf[0], c='teal', ls=':', lw=3, label='wmf')
plt.xscale('log')
plt.title(f'{planet} Evolution')
plt.xlabel('time (Gyr)')
plt.ylabel('fraction of initial state')
plt.legend()
# plt.savefig(f'{planet}_visualizer.png', dpi=600)
print('Showing plot 1/2')
plt.show()

# 2. The Money Plot. --------------------- #
# DO NOT edit this one!
plt.figure(figsize=(10,6))
plt.plot(time,mass/mass[0], c='white', lw=5)
plt.plot(time,radius/radius[0], c='white', ls='--', lw=5)
plt.plot(time,wmf/wmf[0], c='white', ls=(0, (1, 3)),markevery=5000,lw=5)
plt.xscale('log')
plt.axis('off')
# plt.xticks([])
# plt.yticks([])
plt.savefig(f'{planet}_fin.png', dpi=600, transparent=True)
print('Showing plot 2/2')
plt.show() # The Matplotlib preview will look blank, that's ok!

print('Yippee!')
