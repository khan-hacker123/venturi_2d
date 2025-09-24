import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

P_atm_mmHg = 749  
T_atm_C = 25
rho_water = 1000  # kg/m^3
g = 9.81  # mm h2o to pa
R_air = 287  # J/(kg K)

P_atm_Pa = P_atm_mmHg * 133.322  # 1 mmHg = 133.322 Pa
T_atm_K = T_atm_C + 273.15  # K

rho_air = P_atm_Pa / (R_air * T_atm_K)

u_inlet_1 = 10
u_inlet_2 = 20

x_locations_mm = np.array([0, 45, 90, 135, 185, 230, 275, 320, 365, 410, 455])
x_labels = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11']
x_labels_full = ['Inlet'] + x_labels[:-1]

pressures_case1_mmH2O = np.array([-6.6, -8.0, -10.3, -13.0, -13.7, -13.8, -12.5, -11.1, -10.0, -9.0, -8.5])
pressures_case2_mmH2O = np.array([-25.2, -29.9, -38.0, -49.0, -54.0, -54.5, -49.5, -43.2, -39.6, -35.7, -33.5])

areas_mm2 = np.array([22350, 19860, 17370, 15000, 15000, 15000, 16395, 17902.5, 19410, 20910, 22410])
area_inlet_mm2 = 22500

def calculate_continuity_velocities(u_inlet, A_inlet, areas):
    return (A_inlet / areas) * u_inlet

# --- Function to calculate velocities using Bernoulli's Equation ---
def calculate_bernoulli_velocities(u_inlet, p_inlet_mmH2O, pressures_mmH2O, rho_air):
    pressures_Pa = pressures_mmH2O * rho_water * g * 0.001
    p_inlet_Pa = p_inlet_mmH2O * rho_water * g * 0.001
    
    v_i_squared = u_inlet**2 + (2 / rho_air) * (p_inlet_Pa - pressures_Pa)
    return np.sqrt(v_i_squared)


v_continuity_case1 = calculate_continuity_velocities(u_inlet_1, area_inlet_mm2, areas_mm2)
v_bernoulli_case1 = calculate_bernoulli_velocities(u_inlet_1, pressures_case1_mmH2O[0], pressures_case1_mmH2O, rho_air)

v_continuity_case2 = calculate_continuity_velocities(u_inlet_2, area_inlet_mm2, areas_mm2)
v_bernoulli_case2 = calculate_bernoulli_velocities(u_inlet_2, pressures_case2_mmH2O[0], pressures_case2_mmH2O, rho_air)


print("--- Calculated Velocities ---")
data_case1 = {
    'Port': x_labels,
    'x (mm)': x_locations_mm,
    'Area (mm^2)': areas_mm2,
    'Pressure (mmH2O)': pressures_case1_mmH2O,
    'Velocity (Continuity)': v_continuity_case1.round(2),
    'Velocity (Bernoulli)': v_bernoulli_case1.round(2)
}
df_case1 = pd.DataFrame(data_case1)
print(f"\nCase 1: Inlet Velocity = {u_inlet_1} m/s")
print(df_case1.to_string())

data_case2 = {
    'Port': x_labels,
    'x (mm)': x_locations_mm,
    'Area (mm^2)': areas_mm2,
    'Pressure (mmH2O)': pressures_case2_mmH2O,
    'Velocity (Continuity)': v_continuity_case2.round(2),
    'Velocity (Bernoulli)': v_bernoulli_case2.round(2)
}
df_case2 = pd.DataFrame(data_case2)
print(f"\nCase 2: Inlet Velocity = {u_inlet_2} m/s")
print(df_case2.to_string())


plt.style.use('seaborn-v0_8-darkgrid')
plt.figure(figsize=(12, 8))

plt.plot(x_locations_mm, v_continuity_case1, 'o-', label=f'Continuity (u_inf={u_inlet_1} m/s)', color='royalblue')
plt.plot(x_locations_mm, v_bernoulli_case1, 's--', label=f'Bernoulli (u_inf={u_inlet_1} m/s)', color='forestgreen')

plt.plot(x_locations_mm, v_continuity_case2, '^:', label=f'Continuity (u_inf={u_inlet_2} m/s)', color='darkorange')
plt.plot(x_locations_mm, v_bernoulli_case2, 'x-', label=f'Bernoulli (u_inf={u_inlet_2} m/s)', color='darkred')

plt.title('Calculated Velocities using Continuity and Bernoulli Equations', fontsize=16, fontweight='bold')
plt.xlabel('Distance from Inlet (x) [mm]', fontsize=12)
plt.ylabel('Velocity (V) [m/s]', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

