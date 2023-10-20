import numpy as np
from scipy.optimize import curve_fit
import scipy.constants as spc
from scipy.constants import Avogadro, Boltzmann
from pymatgen.core import Composition

boltzmann_constant = Boltzmann * 1e7         # Boltzmann const (erg/K)
bohr_magneton = spc.physical_constants['Bohr magneton'][0]  # Bohr magneton (SI)
bohr_magneton = bohr_magneton * (10**3)      # Bohr magneton (cgs)

def liner_Curie_Weiss(temperature, curie_constant, weiss_temp) :
     return (temperature - weiss_temp) / curie_constant

def Curie_Weiss(temperature, curie_constant, weiss_temp, chi0) :
     return (temperature - weiss_temp) / (chi0 * (temperature - weiss_temp) + curie_constant)

def MomentFunction(curie_constant) :
     return ((3*boltzmann_constant*curie_constant/Avogadro)**0.5) / bohr_magneton

filename = '230217_MT_ZFC_EWO_0p1T.dat'
mass = 25.94   # mass (mg)
comp_name = 'EuWO3'
n = 1     # the number of magnetic ion in unit cell

H_temp_start = 230.0
H_temp_end = 300.0
chi0_start = 0.0    # initial value of chi0

datsave = 0
python_plot = 1
igor_plot = 1
width_chi = 0
width_inv = 0
width_temp = 50
n_divide = 6

mass = mass * (10**(-3))
comp = Composition(comp_name)
molecular_weight = comp.weight

data = np.genfromtxt(filename, skip_header=36, unpack=True, delimiter="," , filling_values='0')
temperature = data[2, :]
field = data[3, :]
moment = data[4, :]

susceptability = (moment / field) * (molecular_weight / mass) / n
inverse_susceptability = 1 / susceptability

high_temperature = []
high_susceptability = []
high_inverse_susceptability = []
for i in range(len(temperature)):
     if H_temp_start <= temperature[i] <= H_temp_end:
          high_temperature.append(temperature[i])
          high_susceptability.append(susceptability[i])
          high_inverse_susceptability.append(inverse_susceptability[i])


# liner Curie-Weiss fitting
guess1 = [0.1, 0.1]
popt1 , pcov1 = curve_fit(liner_Curie_Weiss , high_temperature, high_inverse_susceptability, guess1)
Curie_cons = popt1[0]
eff_moment = MomentFunction(Curie_cons)
weiss_temperature = popt1[1]
print('Curie-Weiss liner fitting')
print("Curie constant {:.{}f}".format(Curie_cons, 3))
print("Magnetic moment {:.{}f}".format(eff_moment, 3))
print("Weiss temperature {:.{}f}".format(weiss_temperature, 3))

# Curie-Weiss fitting (initial values are previous values)
guess2 = np.append(popt1, chi0_start)
popt2 , pcov2 = curve_fit(Curie_Weiss , high_temperature, high_inverse_susceptability, guess2)
Curie_cons = popt2[0]
eff_moment = MomentFunction(Curie_cons)
weiss_temperature = popt2[1]
chi0_final = popt2[2]
print('Curie-Weiss fitting')
print("Curie constant {:.{}f}".format(Curie_cons, 3))
print("Magnetic moment {:.{}f}".format(eff_moment, 3))
print("Weiss temperature {:.{}f}".format(weiss_temperature, 3))
print("Chi0 {:.{}f}".format(chi0_final, 3))
temp = np.arange(weiss_temperature, 300, 0.1)
CW = Curie_Weiss(temp, *popt2)

if python_plot == 1 :
     from graph import PythonPlotDouble
     graphname = filename.replace(".dat", "_CWfitting_" + str(comp_name) + ".png")
     xlabel = 'Temperature (K)'
     ylabel1 = r'$\chi$  $\rm{(emu\  Oe^{-1}\  mol^{-1})}$'
     ylabel2 = r'$\chi^{-1}$  $\rm{{(emu\  Oe^{-1}\  mol^{-1})}^{-1}}$'
     text = r'$\mu$ = ' + "{:.{}f}".format(eff_moment, 3) + ' ' + r'$\mu_{\rm{B}}$' + '\n' \
          + r'$\theta$ = ' + "{:.{}f}".format(weiss_temperature, 3) + ' K' + '\n'\
          + r'$\chi_{0}$ = ' + "{:.{}f}".format(chi0_final, 3) + ' ' + r'emu $\rm{Oe^{-1}}$ $\rm{mol^{-1}}$'
     PythonPlotDouble(graphname, temperature, temp, susceptability, inverse_susceptability, CW, xlabel, ylabel1, ylabel2, width_temp, width_chi, width_inv, text, n_divide)

if igor_plot == 1 :
     from graph import IgorPlotDouble
     outputfilename_itx = filename.replace('.dat', '_' + str(comp_name) + '.itx')
     fsize_text = 25
     xname1 = 'Temperature'
     xname2 = 'temp'
     yname1 = 'Susceptability'
     yname2 = 'Inverse_susceptability'
     yname3 = 'CW_fitting'
     xlabel1 = '\\\\f02T\\\\f00 (K)'
     ylabel1 = '\\\\f02χ\\\\f00 (emu Oe\\\\S-1\\\\M mol\\\\S-1\\\\M)'
     ylabel2 = '\\\\f02χ\\\\f00\\\\S-1\\\\M (emu Oe\\\\S-1\\\\M mol\\\\S-1\\\\M)\\\\S-1\\\\M'
     text = '\\\\Z' + str(fsize_text) + str(comp_name) \
          + '\\r\\\\f02μ\\\\f00 = ' + "{:.{}f}".format(eff_moment, 3) \
          + ' \\\\f02μ\\\\f00\\\\BB\\\\M\\\\Z' + str(fsize_text) \
          + '\\r\\\\f02θ\\\\f00 = ' + "{:.{}f}".format(weiss_temperature, 3) \
          + ' K\\r\\\\f02χ\\\\B0\\\\M\\\\Z' + str(fsize_text) \
          + '\\\\f00 = ' + "{:.{}f}".format(chi0_final, 3) \
          + ' emu Oe\\\\S-1\\\\M\\\\Z' + str(fsize_text) + ' mol\\\\S-1\\\\M'
     IgorPlotDouble(outputfilename_itx, temperature, temp, susceptability, inverse_susceptability, CW, xname1, xname2, yname1, yname2, yname3, xlabel1, ylabel1, ylabel2, width_temp, width_chi, width_inv, text, n_divide)

if datsave == 1 :
     output_filename = filename.replace('.dat', '_susceptability_' + str(comp_name) + '.dat')
     output_filename_1 = filename.replace('.dat', '_CWfitting_' + str(comp_name) + '.dat')
     with open(output_filename, mode = 'w') as f:
          f.write('Temperature Field Moment Susceptablity Inverse_susceptability \n')
          for i in range(len(temperature)) :
               f.write(f'{temperature[i]} {field[i]} {moment[i]} {susceptability[i]} {inverse_susceptability[i]} \n')
     with open(output_filename_1, mode = 'w') as f:
          f.write('Temperature CW_fitting \n')
          for i in range(len(temp)) :
               f.write(f'{temp[i]} {CW[i]} \n')