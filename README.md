# MPMS
Curie_Weiss.py
This is the code for performing Curie-Weiss fitting from MPMS data(Moment vs Temperature). The cgs unit system is used, such as emu, Oe.

20th line: Data file name obtained from MPMS.
21st line: Mass of the sample (mg).
22nd line: Assumed composition for fitting.
23rd line: Number of magnetic ions contained in comp_name.
25,26th lines: Temperature range for performing Curie-Weiss fitting.
27th line: Initial value for chi0 when conducting the fitting.
29th line: When datsave=1, the fitting result is saved in a dat file with the following columns:
First file("filename"+_susceptability_+"compname".dat)
Temperature (K), Magnetic Field (Oe), Magnetic Moment (emu), Molar Susceptibility (emu/Oe mol), and Inverse Susceptibility (emu/Oe mol)^(-1). 
Second file("filename"+_CWfitting_"compname".dat)
Temperature (K), Fitting result(emu/Oe mol)^(-1)
Graph plotting uses temperature on the x-axis, susceptibility on the left y-axis, and inverse susceptibility on the right y-axis.
30th line: When python_plot=1, the results are output using Python (matplotlib) for plotting.
31st line: When igor_plot=1, the results are output in Igor format (.itx) for plotting.
32nd, 33rd, 34th lines: Specifies the width of one tick mark on the graph for each data.
35th line: When width=0, the data's maximum and minimum values are divided into n_divide segments to specify tick marks.


MH.py
This is the code for normalizing magnetic moments and generating graphs from MPMS data(Moment vs Field).
10th line: Data file name obtained from MPMS.
11st line: Mass of the sample (mg).
12nd line: Assumed composition.
13rd line: Number of magnetic ions contained in comp_name.
15th line: When datsave=1, the fitting result is saved in a dat file with the following columns:
First file("filename"+_norm_+"compname".dat)
Temperature (K), Magnetic Field (Oe), Magnetic Moment (emu), Molar Magnetization (emu/mol). 
Graph plotting uses magnetic field on the x-axis, molar magnetization on the y-axis.
16th line: When python_plot=1, the results are output using Python (matplotlib) for plotting.
17st line: When igor_plot=1, the results are output in Igor format (.itx) for plotting.
18,19th lines: Specifies the width of one tick mark on the graph for each data.
20th line: When width=0, the data's maximum and minimum values are divided into n_divide segments to specify tick marks.
