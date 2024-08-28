import component_properties as comp_table
from datetime import datetime
from numba import jit


from multiprocessing import Process
import vlhc_srk_eos as hc
import aq_hb_eos as aq
import h_vdwpm_eos as hyd

def alg1(Temp):
    import numpy as np

    startTime = datetime.now()

    import flashalgorithm as fc
    flash = fc.FlashController(components=['water', 'methane', "ethane", "propane", "i-butane", "n-butane", "i-pentane", "n-pentane", "n-hexane", "meoh"])
    output = flash.main_handler(
                compobjs=flash.compobjs,
                z=np.asarray([0.0220, 0.9258, 0.0299, 0.005, 0.0058, 0.0025, 0.002, 0.00025, 0.00025, 0.0065]),
                T=Temp,
                P=140.0)
    stable_dict = {phase: ii for ii, (phase, alpha) in
                       enumerate(zip(flash.phases, flash.alpha_calc))
                       if alpha > 1e-10}

    for phase, index in stable_dict.items():
        if phase == "s2":
            print(phase, "гидрат s2 тута")
        elif phase == "s1":
            print(phase, "гидрат s1 тута")
        else:
            print("нет гидрата")

    print('Calculation considers the following phases:\n{0}\n'.format(flash.phases))

    print('The stable phases are:')
    for phase, index in stable_dict.items():

            print('\n{0}: {1:3.4f} mol.%'.format(phase, flash.alpha_calc[index]))
            for ii, comp in enumerate(flash.compobjs):
                print('\twith {0:3.4f} mol.% {1}'.format(
                    flash.x_calc[ii, index],
                    comp.compname))
    print(Temp)
    endTime = datetime.now()
    print("Время выполнения: ", endTime - startTime)

def alg2():
    import numpy as np

    startTime = datetime.now()

    import flashalgorithm as fc

    flash = fc.FlashController(components=['water', 'methane', "ethane", "propane", "i-butane", "n-butane", "i-pentane", "n-pentane", "n-hexane", "meoh"])
    output = flash.main_handler(
                compobjs=flash.compobjs,
                z=np.asarray([0.0220, 0.9258, 0.0299, 0.005, 0.0058, 0.0025, 0.002, 0.00025, 0.00025, 0.0065]),
                T=279.3,
                P=140.0)
    stable_dict = {phase: ii for ii, (phase, alpha) in
                       enumerate(zip(flash.phases, flash.alpha_calc))
                       if alpha > 1e-10}
    print('Calculation considers the following phases:\n{0}\n'.format(flash.phases))
    print('The stable phases are:')
    for phase, index in stable_dict.items():
            print('\n{0}: {1:3.4f} mol.%'.format(phase, flash.alpha_calc[index]))
            for ii, comp in enumerate(flash.compobjs):
                print('\twith {0:3.4f} mol.% {1}'.format(
                    flash.x_calc[ii, index],
                    comp.compname))

    print('T=279.3')
    endTime = datetime.now()
    print("Время выполнения: ", endTime - startTime)



if __name__ == '__main__':
    p1 = Process(target=alg1, args=(278.5,), daemon=True)
    p2 = Process(target=alg1, args=(278.6,), daemon=True)
    p1.start()
    p2.start()
    p1.join()
    p2.join()