import numpy as np
import scipy.constants as spc
from scipy.constants import Avogadro, Boltzmann
from pymatgen.core import Composition

boltzmann_constant = Boltzmann * 1e7         # Boltzmann const (erg/K)
bohr_magneton = spc.physical_constants['Bohr magneton'][0]  # Bohr magneton (SI)
bohr_magneton = bohr_magneton * (10**3)      # Bohr magneton (cgs)

filename = '230217_MH_1p8K_EWO.dat'
mass = 25.94   # mass (mg)
comp_name = 'EuWO3'
n = 1     # the number of magnetic ion in unit cell

datsave = 1
python_plot = 1
igor_plot = 1
width_field = 1
width_moment = 0
n_divide = 6

mass = mass * (10**(-3))
comp = Composition(comp_name)
molecular_weight = comp.weight

data = np.genfromtxt(filename, skip_header=36, unpack=True, delimiter="," , filling_values='0')
temperature = data[2, :] 
field = data[3, :] 
moment = data[4, :] 

field_T = field / 10000
moment_normalized = (moment * molecular_weight) / (mass * Avogadro * bohr_magneton * n) 

print("saturation magnetization {:.{}f}".format(max(moment_normalized), 3))

if python_plot == 1 :
     from graph import PythonPlot
     graphname = filename.replace(".dat", "_norm_" + str(comp_name) + ".png")
     xlabel = 'Magnetic Field (T)'
     ylabel = r'$\rm{Moment}\  (\mu_{\rm{B}}/\rm{atom})$'
     PythonPlot(graphname, field_T, moment_normalized, xlabel, ylabel, width_field, width_moment, n_divide)

if igor_plot == 1 :
     from graph import IgorPlot
     outputfilename_itx = filename.replace(".dat", "_" + str(comp_name) + ".itx")
     xname = 'Field'
     yname = 'Moment'
     xlabel = '\\\\f02H\\\\f00 (T)'
     ylabel = 'Moment (\\\\f02μ\\\\f00\\\\BB\\\\M/atom)'
     IgorPlot(outputfilename_itx, field_T, moment_normalized, xname, yname, xlabel, ylabel, width_field, width_moment, n_divide)

if datsave == 1 :
     outputfilename = filename.replace(".dat", "_norm_" + str(comp_name) + ".dat")
     with open(outputfilename, mode = 'w') as f:
          f.write('Temperature Field Moment Moment_norm \n')
          for i in range(len(temperature)) :
               f.write(f'{temperature[i]} {field[i]} {moment[i]} {moment_normalized[i]} \n')