
import component_properties as comp_table
from datetime import datetime
from numba import jit

startTime = datetime.now()

comps = ['h2o', 'n2', 'co2', "ch4", "meoh"]
comp_list = [comp_table.Component(ii) for ii in comps]
for comp in comp_list:
    print('{0:3s}: Tc={1:5.1f} K, Pc={2:5.1f} bar, MW={3:3.1f} g/mol'.format(
        comp.compname, comp.Tc, comp.Pc, comp.MW))

import vlhc_srk_eos as hc
import aq_hb_eos as aq
import h_vdwpm_eos as hyd
import numpy as np

# Composition, pressure, temperature
x = np.ones(len(comps)) / len(comps)  # equal amounts of each component
P = 60  # bar
T = 230  # Kelvin

# Create instances of each equation of state
SRK_obj = hc.SrkEos(comp_list, T, P)
Aq_obj = aq.HegBromEos(comp_list, T, P)

# Access the fugacity of each component in each phase
hc_fug = SRK_obj.calc(comp_list, T, P, x, phase='vapor')
aq_fug = Aq_obj.calc(comp_list, T, P, x)
for ii, comp in enumerate(comp_list):
    print('fugacity of {0} in the hydrocarbon phase is {1:3.2f} bar'.format(
        comp.compname, hc_fug[ii]))
    print('fugacity of {0} in the aqueous phase is {1:3.2f} bar \n'.format(
        comp.compname, aq_fug[ii]))


import flashalgorithm as fc

flash = fc.FlashController(components=['water', 'methane', "ethane", "propane", "i-butane", "n-butane", "i-pentane", "n-pentane", "n-hexane", "meoh"])
output = flash.main_handler(
            compobjs=flash.compobjs,
            z=np.asarray([0.0220,
                          0.9258,
                          0.0299,
                          0.005,
                          0.0058,
                          0.0025,
                          0.002,
                          0.00025,
                          0.00025,
                          0.0075]),
            T=277.3,
            P=140.0)
print(list(zip(flash.phases, flash.alpha_calc)))
stable_dict = {phase: ii for ii, (phase, alpha) in
                   enumerate(zip(flash.phases, flash.alpha_calc))
                   if alpha > 1e-10}
print('Calculation considers the following phases:\n{0}\n'.format(flash.phases))
print('The stable phases are:')
print(f"STABLE DICT = {stable_dict}")
for phase, index in stable_dict.items():
        print('\n{0}: {1:3.4f} mol.%'.format(phase, flash.alpha_calc[index]))
        for ii, comp in enumerate(flash.compobjs):
            print('\twith {0:3.4f} mol.% {1}'.format(
                flash.x_calc[ii, index],
                comp.compname))

endTime = datetime.now()
print("Время выполнения: ", endTime - startTime)

