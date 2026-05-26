import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# STAGE 4
# MPPT + BOOST CONVERTER + SUPERCAPACITOR
# ==========================================================

# ==========================================================
# SIMULATION PARAMETERS
# ==========================================================

dt = 0.05
time_steps = 3500

# ==========================================================
# THERMAL PARAMETERS
# ==========================================================

ambient_temperature = -8.0

roof_temperature = -6.0

target_temperature = 2.0

thermal_capacity = 10.0

heat_loss = 0.05

# ==========================================================
# TEG PARAMETERS
# ==========================================================

seebeck_coefficient = 0.06

internal_resistance = 2.0

# ==========================================================
# BOOST CONVERTER PARAMETERS
# ==========================================================

duty_cycle = 0.45

max_duty = 0.90

min_duty = 0.10

mppt_step = 0.003

previous_power = 0.0

boost_efficiency = 0.92

# ==========================================================
# SUPERCAPACITOR
# ==========================================================

C_supercap = 10.0

supercap_voltage = 0.0

# ==========================================================
# THERMAL LOAD
# ==========================================================

R_heater = 5.0

# ==========================================================
# STORAGE
# ==========================================================

time_axis = []

temperature_data = []

teg_voltage_data = []

boost_voltage_data = []

supercap_voltage_data = []

heater_power_data = []

duty_data = []

power_data = []

# ==========================================================
# SIMULATION LOOP
# ==========================================================

for step in range(time_steps):

    t = step * dt

    # ======================================================
    # ENVIRONMENT DISTURBANCE
    # ======================================================

    wind_disturbance = (
        0.25 * np.sin(0.02 * t)
    )

    # ======================================================
    # TEMPERATURE DIFFERENCE
    # ======================================================

    delta_T = (
        roof_temperature
        - ambient_temperature
    )

    # ======================================================
    # TEG VOLTAGE
    # ======================================================

    teg_voltage = (
        seebeck_coefficient
        * delta_T
    )

    # ======================================================
    # TEG CURRENT
    # ======================================================

    teg_current = (
        teg_voltage
        / internal_resistance
    )

    # ======================================================
    # INPUT POWER
    # ======================================================

    teg_power = (
        teg_voltage
        * teg_current
    )

    # ======================================================
    # MPPT CONTROL
    # PERTURB AND OBSERVE
    # ======================================================

    if teg_power > previous_power:

        duty_cycle += mppt_step

    else:

        duty_cycle -= mppt_step

    duty_cycle = np.clip(
        duty_cycle,
        min_duty,
        max_duty
    )

    previous_power = teg_power

    # ======================================================
    # BOOST CONVERTER
    # ======================================================

    boost_voltage = (
        teg_voltage
        / (1.0 - duty_cycle)
    )

    boost_voltage *= boost_efficiency

    # ======================================================
    # SUPERCAP CHARGING
    # ======================================================

    charging_current = (
        boost_voltage
        - supercap_voltage
    ) * 0.12

    dV_supercap = (
        charging_current
        / C_supercap
    )

    supercap_voltage += (
        dt * dV_supercap
    )

    # ======================================================
    # HEATER LOAD
    # ======================================================

    heater_power = (
        supercap_voltage ** 2
    ) / R_heater

    # ======================================================
    # THERMAL DYNAMICS
    # ======================================================

    dT = (
        heater_power
        - heat_loss
        * (
            roof_temperature
            - ambient_temperature
        )
        - wind_disturbance
    ) / thermal_capacity

    roof_temperature += (
        dt * dT
    )

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

    boost_voltage_data.append(
        boost_voltage
    )

    supercap_voltage_data.append(
        supercap_voltage
    )

    heater_power_data.append(
        heater_power
    )

    duty_data.append(
        duty_cycle
    )

    power_data.append(
        teg_power
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
    'Stage 4 - Thermal Regulation with MPPT'
)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.show()

# ==========================================================
# VOLTAGE RESPONSE
# ==========================================================

plt.figure(figsize=(10,5))

plt.plot(
    time_axis,
    teg_voltage_data,
    label='TEG Voltage'
)

plt.plot(
    time_axis,
    boost_voltage_data,
    linewidth=2,
    label='Boost Converter Voltage'
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
    'MPPT Boost Converter Behavior'
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
    'Thermal Heater Power'
)

plt.grid(True)

plt.tight_layout()

plt.show()

# ==========================================================
# DUTY CYCLE EVOLUTION
# ==========================================================

plt.figure(figsize=(10,5))

plt.plot(
    time_axis,
    duty_data,
    linewidth=2
)

plt.xlabel('Time (s)')
plt.ylabel('Duty Cycle')

plt.title(
    'MPPT Duty Cycle Adaptation'
)

plt.grid(True)

plt.tight_layout()

plt.show()

# ==========================================================
# TEG POWER EXTRACTION
# ==========================================================

plt.figure(figsize=(10,5))

plt.plot(
    time_axis,
    power_data,
    linewidth=2
)

plt.xlabel('Time (s)')
plt.ylabel('Power (W)')

plt.title(
    'TEG Extracted Power'
)

plt.grid(True)

plt.tight_layout()

plt.show()