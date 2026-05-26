import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# STAGE 9
# DC/DC BOOST CONVERTER
# ==========================================================

dt = 0.01
time_steps = 4000

# ==========================================================
# TEG PARAMETERS
# ==========================================================

seebeck_coefficient = 0.020

hot_temperature = 8.0
cold_temperature = -6.0

base_delta_T = (
    hot_temperature
    - cold_temperature
)

# ==========================================================
# BOOST CONVERTER PARAMETERS
# ==========================================================

target_voltage = 5.0

duty_cycle = 0.45

inductor = 0.002
capacitor = 0.01

load_resistance = 15.0

# ==========================================================
# CONTROL PARAMETERS
# ==========================================================

kp = 0.015

# ==========================================================
# INITIAL CONDITIONS
# ==========================================================

inductor_current = 0.0
output_voltage = 0.0

# ==========================================================
# STORAGE
# ==========================================================

time_axis = []

vin_history = []
vout_history = []

duty_history = []

current_history = []

# ==========================================================
# SIMULATION LOOP
# ==========================================================

for step in range(time_steps):

    t = step * dt

    # ======================================================
    # ENVIRONMENTAL THERMAL VARIATION
    # ======================================================

    thermal_variation = (
        2.0
        * np.sin(0.015 * t)
    )

    delta_T = (
        base_delta_T
        + thermal_variation
    )

    # ======================================================
    # TEG INPUT VOLTAGE
    # ======================================================

    vin = (
        seebeck_coefficient
        * delta_T
    )

    vin = max(vin, 0.05)

    # ======================================================
    # BOOST CONVERTER IDEAL MODEL
    # ======================================================

    ideal_vout = (
        vin
        / (1.0 - duty_cycle)
    )

    # ======================================================
    # OUTPUT FILTER DYNAMICS
    # ======================================================

    dv = (
        ideal_vout
        - output_voltage
    ) * 0.08

    output_voltage += dv

    # ======================================================
    # LOAD CURRENT
    # ======================================================

    load_current = (
        output_voltage
        / load_resistance
    )

    # ======================================================
    # INDUCTOR CURRENT
    # ======================================================

    di = (
        vin
        / inductor
    ) * dt

    inductor_current += di

    # ======================================================
    # FEEDBACK CONTROL
    # ======================================================

    error = (
        target_voltage
        - output_voltage
    )

    duty_cycle += (
        kp * error
    )

    duty_cycle = np.clip(
        duty_cycle,
        0.05,
        0.90
    )

    # ======================================================
    # STORE
    # ======================================================

    time_axis.append(t)

    vin_history.append(vin)

    vout_history.append(output_voltage)

    duty_history.append(duty_cycle)

    current_history.append(load_current)

# ==========================================================
# INPUT VS OUTPUT VOLTAGE
# ==========================================================

plt.figure(figsize=(9,5))

plt.plot(
    time_axis,
    vin_history,
    label='TEG Input Voltage',
    linewidth=2
)

plt.plot(
    time_axis,
    vout_history,
    label='Boost Output Voltage',
    linewidth=2
)

plt.axhline(
    target_voltage,
    linestyle='--',
    label='Target Voltage'
)

plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')

plt.title(
    'DC/DC Boost Converter Regulation'
)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.savefig(
    'stage9_boost_voltage.png',
    dpi=300
)

plt.show()

# ==========================================================
# DUTY CYCLE
# ==========================================================

plt.figure(figsize=(9,5))

plt.plot(
    time_axis,
    duty_history,
    linewidth=2
)

plt.xlabel('Time (s)')
plt.ylabel('Duty Cycle')

plt.title(
    'Adaptive Duty Cycle Regulation'
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    'stage9_duty_cycle.png',
    dpi=300
)

plt.show()

# ==========================================================
# LOAD CURRENT
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
    'Load Current Response'
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    'stage9_load_current.png',
    dpi=300
)

plt.show()