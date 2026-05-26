import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# SIMULATION PARAMETERS
# ==========================================================

dt = 0.1
time_steps = 2000

# ==========================================================
# THERMOELECTRIC PARAMETERS
# ==========================================================

# Seebeck coefficient (V/K)
alpha = 0.02

# ==========================================================
# ELECTRICAL PARAMETERS
# ==========================================================

# Resistive thermal load
R_load = 5.0

# ==========================================================
# THERMAL PARAMETERS
# ==========================================================

thermal_capacity = 12.0

heat_loss_coefficient = 0.08

# ==========================================================
# ENVIRONMENTAL CONDITIONS
# ==========================================================

ambient_temperature = -8.0

# Initial hot side
T_hot = 3.0

# Initial cold side
T_cold = ambient_temperature

# ==========================================================
# STORAGE VARIABLES
# ==========================================================

time_axis = []

hot_temperature = []
cold_temperature = []

delta_T_values = []

voltage_values = []
current_values = []
power_values = []

heating_temperature = []

# ==========================================================
# SIMULATION LOOP
# ==========================================================

for step in range(time_steps):

    t = step * dt

    # ======================================================
    # ENVIRONMENTAL DISTURBANCE
    # ======================================================

    ambient_variation = (
        0.6 * np.sin(0.01 * t)
    )

    current_ambient = (
        ambient_temperature
        + ambient_variation
    )

    # ======================================================
    # TEMPERATURE DIFFERENCE
    # ======================================================

    delta_T = T_hot - T_cold

    # ======================================================
    # TEG VOLTAGE
    # ======================================================

    V_teg = alpha * delta_T

    # ======================================================
    # CURRENT
    # ======================================================

    I_teg = V_teg / R_load

    # ======================================================
    # GENERATED POWER
    # ======================================================

    P_teg = (
        V_teg ** 2
    ) / R_load

    # ======================================================
    # JOULE HEATING
    # ======================================================

    Q_heating = P_teg

    # ======================================================
    # THERMAL LOSSES
    # ======================================================

    Q_loss = (
        heat_loss_coefficient
        * (T_hot - current_ambient)
    )

    # ======================================================
    # THERMAL DYNAMICS
    # ======================================================

    dT = (
        Q_heating - Q_loss
    ) / thermal_capacity

    T_hot += dt * dT

    # ======================================================
    # COLD SIDE DYNAMICS
    # ======================================================

    T_cold = (
        current_ambient
        + 0.2 * np.sin(0.03 * t)
    )

    # ======================================================
    # STORE DATA
    # ======================================================

    time_axis.append(t)

    hot_temperature.append(T_hot)
    cold_temperature.append(T_cold)

    delta_T_values.append(delta_T)

    voltage_values.append(V_teg)
    current_values.append(I_teg)
    power_values.append(P_teg)

    heating_temperature.append(T_hot)

# ==========================================================
# TEMPERATURE EVOLUTION
# ==========================================================

plt.figure(figsize=(10,5))

plt.plot(
    time_axis,
    hot_temperature,
    label='Heating Surface Temperature',
    linewidth=2
)

plt.plot(
    time_axis,
    cold_temperature,
    label='Cold Side Temperature',
    linewidth=2
)

plt.axhline(
    0,
    linestyle='--',
    label='Snow Melting Threshold'
)

plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')

plt.title(
    'Electro-Thermal Heating Dynamics'
)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.savefig(
    'electro_thermal_heating.png',
    dpi=300
)

plt.show()

# ==========================================================
# GENERATED VOLTAGE
# ==========================================================

plt.figure(figsize=(10,5))

plt.plot(
    time_axis,
    voltage_values,
    linewidth=2
)

plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')

plt.title(
    'TEG Generated Voltage'
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    'teg_voltage_stage2.png',
    dpi=300
)

plt.show()

# ==========================================================
# GENERATED POWER
# ==========================================================

plt.figure(figsize=(10,5))

plt.plot(
    time_axis,
    power_values,
    linewidth=2
)

plt.xlabel('Time (s)')
plt.ylabel('Power (W)')

plt.title(
    'Generated Thermal Power'
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    'generated_thermal_power.png',
    dpi=300
)

plt.show()

# ==========================================================
# FINAL RESULTS
# ==========================================================

print("\n===== FINAL RESULTS =====")

print(
    f"Final Hot Temperature: "
    f"{T_hot:.2f} °C"
)

print(
    f"Final Cold Temperature: "
    f"{T_cold:.2f} °C"
)

print(
    f"Final Delta T: "
    f"{delta_T:.2f} °C"
)

print(
    f"Final Voltage: "
    f"{V_teg:.4f} V"
)

print(
    f"Final Current: "
    f"{I_teg:.4f} A"
)

print(
    f"Final Generated Power: "
    f"{P_teg:.4f} W"
)