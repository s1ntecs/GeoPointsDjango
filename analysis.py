import component_properties as comp_table
from datetime import datetime
import vlhc_srk_eos as hc
import aq_hb_eos as aq
import h_vdwpm_eos as hyd
import numpy as np
import matplotlib.pyplot as plt
import flashalgorithm_old as fc
from tqdm import tqdm
from numpy.linalg import LinAlgError

# Функция для создания объектов компонентов
def create_components(comp_names):
    return [comp_table.Component(ii) for ii in comp_names]

# Функция для расчета фазового состава
def calculate_phases(flash, z, T, P):
    try:
        output = flash.main_handler(compobjs=flash.compobjs, z=z, T=T, P=P)
        stable_dict = {phase: ii for ii, (phase, alpha) in enumerate(zip(flash.phases, flash.alpha_calc)) if alpha > 1e-10}
        return stable_dict
    except LinAlgError as e:
        print(f"Numerical issue encountered at T={T} K, P={P} bar, methanol_ratio={z[-1]:.4f}")
        print(f"Error: {e}")
        return None

# Функция для анализа данных с прогресс-баром
def analyze_conditions(flash, comp_list, temperatures, pressures, methanol_ratio):
    results = []
    total_iterations = len(temperatures) * len(pressures)
    
    with tqdm(total=total_iterations, desc="Calculating phase behavior") as pbar:
        for T in temperatures:
            for P in pressures:
                # Создание объектов уравнений состояния для текущих T и P
                SRK_obj = hc.SrkEos(comp_list, T=T, P=P)
                Aq_obj = aq.HegBromEos(comp_list, T=T, P=P)

                # Пример расчета фугитивности
                x = np.ones(len(comp_list)) / len(comp_list)  # Равные количества каждого компонента
                hc_fug = SRK_obj.calc(comp_list, T, P, x, phase='vapor')
                aq_fug = Aq_obj.calc(comp_list, T, P, x)
                
                for ii, comp in enumerate(comp_list):
                    print('fugacity of {0} in the hydrocarbon phase is {1:3.2f} bar'.format(
                        comp.compname, hc_fug[ii]))
                    print('fugacity of {0} in the aqueous phase is {1:3.2f} bar \n'.format(
                        comp.compname, aq_fug[ii]))

                # Расчет фазового состава
                z = np.asarray([0.0220,
                                0.9258 * (1 - methanol_ratio),
                                0.0299,
                                0.005,
                                0.0058,
                                0.0025,
                                0.002,
                                0.00025,
                                0.00025,
                                methanol_ratio])
                stable_phases = calculate_phases(flash, z, T, P)
                if stable_phases is not None:
                    results.append((T, P, methanol_ratio, stable_phases))
                pbar.update(1)  # Обновление прогресс-бара после каждой итерации
    return results

# Функция для визуализации данных
def plot_pressure_temperature_analysis(results, phase_name):
    temperatures = []
    pressures = []
    phase_presence = []

    for T, P, methanol_ratio, stable_phases in results:
        temperatures.append(T)
        pressures.append(P)
        phase_presence.append(phase_name in stable_phases)

    plt.figure(figsize=(10, 6))
    plt.scatter(temperatures, pressures, c=phase_presence, cmap='coolwarm', marker='o')
    plt.title(f'{phase_name} presence vs Temperature and Pressure')
    plt.xlabel('Temperature (K)')
    plt.ylabel('Pressure (bar)')
    plt.colorbar(label='Presence of Phase')
    plt.show()

# Основная функция выполнения программы
def main():
    startTime = datetime.now()

    comps = ['h2o', 'n2', 'co2', "ch4", "meoh"]
    comp_list = create_components(comps)
    
    # Печать свойств компонентов
    for comp in comp_list:
        print('{0:3s}: Tc={1:5.1f} K, Pc={2:5.1f} bar, MW={3:3.1f} g/mol'.format(
            comp.compname, comp.Tc, comp.Pc, comp.MW))

    flash = fc.FlashController(components=['water', 'methane', "ethane", "propane", 
                                           "i-butane", "n-butane", "i-pentane", 
                                           "n-pentane", "n-hexane", "meoh"])
    
    # Диапазон температур и давлений для анализа
    temperatures = np.linspace(270, 290, 10)  # Температурный диапазон
    pressures = np.linspace(100, 200, 10)  # Диапазон давлений
    methanol_ratio = 0.05  # Фиксированный объем метанола

    results = analyze_conditions(flash, comp_list, temperatures, pressures, methanol_ratio)

    # Построение графиков для фаз S1 и S2
    plot_pressure_temperature_analysis(results, 'S1')
    plot_pressure_temperature_analysis(results, 'S2')

    endTime = datetime.now()
    print("Время выполнения: ", endTime - startTime)

if __name__ == "__main__":
    main()
