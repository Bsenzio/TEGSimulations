import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# STAGE 8
# MPPT THERMOELECTRIC ENERGY HARVESTING
# ==========================================================

dt = 0.1
time_steps = 2000

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

open_circuit_voltage = (
    seebeck_coefficient
    * delta_T
)

internal_resistance = 3.0

# ==========================================================
# MPPT PARAMETERS
# ==========================================================

load_resistance = 5.0

step_size = 0.05

previous_power = 0.0

direction = 1

# ==========================================================
# STORAGE
# ==========================================================

time_axis = []

voltage_history = []
current_history = []

power_history = []

resistance_history = []

# ==========================================================
# SIMULATION LOOP
# ==========================================================

for step in range(time_steps):

    t = step * dt

    # ======================================================
    # ENVIRONMENTAL TEMPERATURE FLUCTUATION
    # ======================================================

    thermal_variation = (
        1.5
        * np.sin(0.01 * t)
    )

    delta_T_dynamic = (
        delta_T
        + thermal_variation
    )

    # ======================================================
    # TEG VOLTAGE
    # ======================================================

    teg_voltage = (
        seebeck_coefficient
        * delta_T_dynamic
    )

    # ======================================================
    # CURRENT
    # ======================================================

    current = (
        teg_voltage
        / (
            internal_resistance
            + load_resistance
        )
    )

    # ======================================================
    # LOAD VOLTAGE
    # ======================================================

    load_voltage = (
        current
        * load_resistance
    )

    # ======================================================
    # OUTPUT POWER
    # ======================================================

    output_power = (
        load_voltage
        * current
    )

    # ======================================================
    # MPPT ALGORITHM
    # ======================================================

    if output_power > previous_power:

        load_resistance += (
            direction
            * step_size
        )

    else:

        direction *= -1

        load_resistance += (
            direction
            * step_size
        )

    # ======================================================
    # LIMITS
    # ======================================================

    load_resistance = np.clip(
        load_resistance,
        1.0,
        20.0
    )

    previous_power = output_power

    # ======================================================
    # STORE
    # ======================================================

    time_axis.append(t)

    voltage_history.append(
        load_voltage
    )

    current_history.append(
        current
    )

    power_history.append(
        output_power
    )

    resistance_history.append(
        load_resistance
    )

# ==========================================================
# POWER RESPONSE
# ==========================================================

plt.figure(figsize=(9,5))

plt.plot(
    time_axis,
    power_history,
    linewidth=2
)

plt.xlabel('Time (s)')
plt.ylabel('Power (W)')

plt.title(
    'MPPT Thermoelectric Power Extraction'
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    'stage8_mppt_power.png',
    dpi=300
)

plt.show()

# ==========================================================
# LOAD RESISTANCE TRACKING
# ==========================================================

plt.figure(figsize=(9,5))

plt.plot(
    time_axis,
    resistance_history,
    linewidth=2
)

plt.xlabel('Time (s)')
plt.ylabel('Resistance (Ohms)')

plt.title(
    'MPPT Load Resistance Adaptation'
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    'stage8_mppt_resistance.png',
    dpi=300
)

plt.show()

# ==========================================================
# VOLTAGE RESPONSE
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
    'TEG Output Voltage'
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    'stage8_voltage.png',
    dpi=300
)

plt.show()

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
    'TEG Output Current'
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    'stage8_current.png',
    dpi=300
)

plt.show()