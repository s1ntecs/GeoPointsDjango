import component_properties as comp_table
from datetime import datetime
import numpy as np
import flashalgorithm as fc
import vlhc_srk_eos as hc
import aq_hb_eos as aq
import h_vdwpm_eos as hyd
import matplotlib.pyplot as plt

startTime = datetime.now()

# Определение компонентов
comps = ['h2o', 'n2', 'co2', "ch4", "meoh"]
comp_list = [comp_table.Component(ii) for ii in comps]

# Инициализация параметров
meoh = 0.006
MEOH_LIM = 0.008
MEOH_STEP = 0.001
P_values = np.arange(130, 136, 5)  # Давление от 130 до 135 с шагом 5
T_values = np.arange(260, 266, 5)  # Температура от 260 до 265 с шагом 5

results = []

flash = fc.FlashController(components=['water',
                                       'methane',
                                       "ethane",
                                       "propane",
                                       "i-butane",
                                       "n-butane",
                                       "i-pentane",
                                       "n-pentane",
                                       "n-hexane",
                                       "meoh"])

# Основной цикл расчета
for P in P_values:
    for T in T_values:
        meoh = 0.006
        while meoh <= MEOH_LIM:
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
                                    meoh]),
                        T=T,
                        P=P)
            stable_dict = {phase: ii for ii, (phase, alpha) in
                            enumerate(zip(flash.phases, flash.alpha_calc))}
            for phase, index in stable_dict.items():
                if phase == 's2':  # Извлекаем только данные для s2
                    results.append({
                        "Pressure": P,
                        "Temperature": T,
                        "MeOH": meoh,
                        "s2": flash.alpha_calc[index]
                    })
            meoh += MEOH_STEP

endTime = datetime.now()
print("Время выполнения: ", endTime - startTime)

# Построение графиков зависимости S2 от объема метанола при различных давлениях и температурах
plt.figure(figsize=(14, 8))

# График для каждого значения давления
for P in P_values:
    plt.subplot(2, 1, 1)
    subset = [res for res in results if res["Pressure"] == P]
    meoh_values = [res["MeOH"] for res in subset]
    s2_values = [res["s2"] for res in subset]
    plt.plot(meoh_values, s2_values, marker='o', label=f'P = {P} bar')

plt.title("S2 vs MeOH Volume for Different Pressures")
plt.xlabel("MeOH Volume (fraction)")
plt.ylabel("S2")
plt.legend()
plt.grid(True)

# График для каждого значения температуры
for T in T_values:
    plt.subplot(2, 1, 2)
    subset = [res for res in results if res["Temperature"] == T]
    meoh_values = [res["MeOH"] for res in subset]
    s2_values = [res["s2"] for res in subset]
    plt.plot(meoh_values, s2_values, marker='o', label=f'T = {T} K')

plt.title("S2 vs MeOH Volume for Different Temperatures")
plt.xlabel("MeOH Volume (fraction)")
plt.ylabel("S2")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
