import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# SIMULATION PARAMETERS
# ==========================================================

dt = 0.1
time_steps = 2500

# ==========================================================
# THERMAL PARAMETERS
# ==========================================================

ambient_temperature = -8.0
target_temperature = 2.0

thermal_capacity = 10.0
heat_loss = 0.06

# ==========================================================
# TEG PARAMETERS
# ==========================================================

seebeck_coefficient = 0.045

# ==========================================================
# SUPERCAPACITOR PARAMETERS
# ==========================================================

C_supercap = 8.0

supercap_voltage = 0.0

# ==========================================================
# HEATING LOAD
# ==========================================================

R_heater = 6.0

# ==========================================================
# INITIAL CONDITIONS
# ==========================================================

roof_temperature = -6.0

# ==========================================================
# STORAGE
# ==========================================================

time_axis = []

temperature_data = []

teg_voltage_data = []

supercap_voltage_data = []

heater_power_data = []

# ==========================================================
# SIMULATION LOOP
# ==========================================================

for step in range(time_steps):

    t = step * dt

    # ======================================================
    # THERMAL DIFFERENCE
    # ======================================================

    delta_T = roof_temperature - ambient_temperature

    # ======================================================
    # TEG VOLTAGE GENERATION
    # ======================================================

    teg_voltage = (
        seebeck_coefficient
        * delta_T
    )

    # ======================================================
    # SUPERCAP CHARGING
    # ======================================================

    charging_current = (
        teg_voltage
        - supercap_voltage
    ) * 0.15

    dV_supercap = (
        charging_current
        / C_supercap
    )

    supercap_voltage += (
        dt * dV_supercap
    )

    # ======================================================
    # HEATER POWER
    # ======================================================

    heater_power = (
        supercap_voltage ** 2
    ) / R_heater

    # ======================================================
    # THERMAL DYNAMICS
    # ======================================================

    wind_disturbance = (
        0.3 * np.sin(0.02 * t)
    )

    dT = (
        heater_power
        - heat_loss
        * (
            roof_temperature
            - ambient_temperature
        )
        - wind_disturbance
    ) / thermal_capacity

    roof_temperature += dt * dT

    # ======================================================
    # STORE DATA
    # ======================================================

    time_axis.append(t)

    temperature_data.append(
        roof_temperature
    )

    teg_voltage_data.append(
        teg_voltage
    )

    supercap_voltage_data.append(
        supercap_voltage
    )

    heater_power_data.append(
        heater_power
    )

# ==========================================================
# TEMPERATURE RESPONSE
# ==========================================================

plt.figure(figsize=(10,5))

plt.plot(
    time_axis,
    temperature_data,
    linewidth=2,
    label='Roof Temperature'
)

plt.axhline(
    target_temperature,
    linestyle='--',
    label='Target Temperature'
)

plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')

plt.title(
    'Thermal Regulation Using TEG + Supercapacitor'
)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.show()

# ==========================================================
# TEG AND SUPERCAP VOLTAGE
# ==========================================================

plt.figure(figsize=(10,5))

plt.plot(
    time_axis,
    teg_voltage_data,
    label='TEG Voltage'
)

plt.plot(
    time_axis,
    supercap_voltage_data,
    linewidth=2,
    label='Supercapacitor Voltage'
)

plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')

plt.title(
    'TEG Energy Harvesting and Supercapacitor Charging'
)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.show()

# ==========================================================
# HEATER POWER
# ==========================================================

plt.figure(figsize=(10,5))

plt.plot(
    time_axis,
    heater_power_data,
    linewidth=2
)

plt.xlabel('Time (s)')
plt.ylabel('Power (W)')

plt.title(
    'Thermal Resistive Heating Power'
)

plt.grid(True)

plt.tight_layout()

plt.show()