import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# STAGE 7
# RLC ENERGY BUFFER + THERMAL LOAD
# ==========================================================

dt = 0.01
time_steps = 4000

# ==========================================================
# TEG PARAMETERS
# ==========================================================

seebeck_coefficient = 0.020

hot_temperature = 8.0
cold_temperature = -6.0

delta_T = (
    hot_temperature
    - cold_temperature
)

teg_voltage = (
    seebeck_coefficient
    * delta_T
)

# ==========================================================
# RLC PARAMETERS
# ==========================================================

R = 4.0          # Ohms
L = 0.8          # Henry
C = 1.5          # Farads

# ==========================================================
# THERMAL LOAD
# ==========================================================

R_load = 6.0

# ==========================================================
# INITIAL CONDITIONS
# ==========================================================

current = 0.0
capacitor_voltage = 0.0
charge = 0.0

# ==========================================================
# STORAGE
# ==========================================================

time_axis = []

current_history = []
voltage_history = []

thermal_power_history = []
capacitor_energy_history = []

# ==========================================================
# SIMULATION LOOP
# ==========================================================

for step in range(time_steps):

    t = step * dt

    # ======================================================
    # RLC DYNAMICS
    # ======================================================

    dI_dt = (
        teg_voltage
        - R * current
        - capacitor_voltage
    ) / L

    current += dI_dt * dt

    # ======================================================
    # CAPACITOR UPDATE
    # ======================================================

    charge += current * dt

    capacitor_voltage = (
        charge / C
    )

    # ======================================================
    # THERMAL LOAD POWER
    # ======================================================

    thermal_power = (
        current ** 2
    ) * R_load

    # ======================================================
    # CAPACITOR ENERGY
    # ======================================================

    capacitor_energy = (
        0.5
        * C
        * capacitor_voltage ** 2
    )

    # ======================================================
    # STORE
    # ======================================================

    time_axis.append(t)

    current_history.append(current)

    voltage_history.append(
        capacitor_voltage
    )

    thermal_power_history.append(
        thermal_power
    )

    capacitor_energy_history.append(
        capacitor_energy
    )

# ==========================================================
# CURRENT RESPONSE
# ==========================================================

plt.figure(figsize=(9,5))

plt.plot(
    time_axis,
    current_history,
    linewidth=2
)

plt.xlabel('Time (s)')
plt.ylabel('Current (A)')

plt.title(
    'RLC Current Response'
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    'stage7_rlc_current.png',
    dpi=300
)

plt.show()

# ==========================================================
# CAPACITOR VOLTAGE
# ==========================================================

plt.figure(figsize=(9,5))

plt.plot(
    time_axis,
    voltage_history,
    linewidth=2
)

plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')

plt.title(
    'Supercapacitor Voltage'
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    'stage7_supercapacitor_voltage.png',
    dpi=300
)

plt.show()

# ==========================================================
# THERMAL POWER
# ==========================================================

plt.figure(figsize=(9,5))

plt.plot(
    time_axis,
    thermal_power_history,
    linewidth=2
)

plt.xlabel('Time (s)')
plt.ylabel('Thermal Power (W)')

plt.title(
    'Thermal Load Power'
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    'stage7_thermal_power.png',
    dpi=300
)

plt.show()

# ==========================================================
# STORED ENERGY
# ==========================================================

plt.figure(figsize=(9,5))

plt.plot(
    time_axis,
    capacitor_energy_history,
    linewidth=2
)

plt.xlabel('Time (s)')
plt.ylabel('Energy (J)')

plt.title(
    'Stored Supercapacitor Energy'
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    'stage7_capacitor_energy.png',
    dpi=300
)

plt.show()