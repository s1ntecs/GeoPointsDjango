import component_properties as comp_table
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import flashalgorithm as fc

# Функция для создания списка компонентов
def create_components(comps):
    comp_list = [comp_table.Component(ii) for ii in comps]
    return comp_list

# Функция для выполнения расчета фазового равновесия и возврата фракций фаз S1 и S2
def run_flash_analysis(comp_list, P, T, meoh):
    # Обновляем состав компонента с измененным содержанием MeOH
    z = np.array([0.22, 0.65, 0.03, 0.08, meoh])
    
    # Инициализация FlashController
    flash = fc.FlashController(components=[comp.compname for comp in comp_list])
    output = flash.main_handler(compobjs=flash.compobjs, z=z, T=T, P=P)
    
    # Определяем стабильные фазы
    stable_dict = {phase: ii for ii, (phase, alpha) in enumerate(zip(flash.phases, flash.alpha_calc)) if alpha > 1e-10}
    
    # Возвращаем фракции фаз S1 и S2
    s1_fraction = flash.alpha_calc[stable_dict.get('S1', -1)] if 'S1' in stable_dict else 0
    s2_fraction = flash.alpha_calc[stable_dict.get('S2', -1)] if 'S2' in stable_dict else 0
    
    return s1_fraction, s2_fraction

# Параметры для анализа
P_list = np.linspace(50, 150, 5)  # Давление от 50 до 150 бар
T_list = np.linspace(250, 350, 5)  # Температура от 250 до 350 К
meoh_list = np.linspace(0.01, 0.1, 5)  # Содержание MeOH от 1% до 10%

# Определение изначальных компонентов
comps = ['h2o', 'n2', 'co2', 'ch4', 'meoh']
comp_list = create_components(comps)

# Подготовка данных для графиков
s1_data = []
s2_data = []
params = []

for P in P_list:
    for T in T_list:
        for meoh in meoh_list:
            s1_fraction, s2_fraction = run_flash_analysis(comp_list, P, T, meoh)
            s1_data.append(s1_fraction)
            s2_data.append(s2_fraction)
            params.append((P, T, meoh))

# Построение графиков

# График для фазы S1
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
for i in range(len(P_list) * len(T_list)):
    plt.plot(meoh_list, s1_data[i*len(meoh_list):(i+1)*len(meoh_list)], label=f'P={params[i][0]} bar, T={params[i][1]} K')
plt.xlabel('Содержание MeOH')
plt.ylabel('Фракция фазы S1')
plt.title('Фаза S1 в зависимости от содержания MeOH')
plt.legend()
plt.grid(True)

# График для фазы S2
plt.subplot(1, 2, 2)
for i in range(len(P_list) * len(T_list)):
    plt.plot(meoh_list, s2_data[i*len(meoh_list):(i+1)*len(meoh_list)], label=f'P={params[i][0]} bar, T={params[i][1]} K')
plt.xlabel('Содержание MeOH')
plt.ylabel('Фракция фазы S2')
plt.title('Фаза S2 в зависимости от содержания MeOH')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
