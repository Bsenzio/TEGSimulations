import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# SIMULATION PARAMETERS
# ==========================================================

dt = 0.1
time_steps = 1200

# ==========================================================
# THERMOELECTRIC PARAMETERS
# ==========================================================

# Seebeck coefficient (Volts/Kelvin)
alpha = 0.0002

# Load resistance (Ohms)
R_load = 5.0

# ==========================================================
# TEMPERATURE CONDITIONS
# ==========================================================

# Hot side temperature
T_hot_base = 4.0

# Cold side temperature
T_cold_base = -8.0

# ==========================================================
# STORAGE VARIABLES
# ==========================================================

time_axis = []

hot_side = []
cold_side = []

delta_T_values = []

voltage_values = []
current_values = []
power_values = []

# ==========================================================
# SIMULATION LOOP
# ==========================================================

for step in range(time_steps):

    t = step * dt

    # ======================================================
    # ENVIRONMENTAL TEMPERATURE VARIATION
    # ======================================================

    hot_variation = (
        0.5 * np.sin(0.02 * t)
    )

    cold_variation = (
        0.8 * np.sin(0.015 * t + 1.5)
    )

    T_hot = (
        T_hot_base
        + hot_variation
    )

    T_cold = (
        T_cold_base
        + cold_variation
    )

    # ======================================================
    # TEMPERATURE DIFFERENCE
    # ======================================================

    delta_T = T_hot - T_cold

    # ======================================================
    # TEG VOLTAGE GENERATION
    # ======================================================

    V_teg = alpha * delta_T

    # ======================================================
    # ELECTRICAL RESPONSE
    # ======================================================

    I_teg = V_teg / R_load

    P_teg = (
        V_teg ** 2
    ) / R_load

    # ======================================================
    # STORE DATA
    # ======================================================

    time_axis.append(t)

    hot_side.append(T_hot)
    cold_side.append(T_cold)

    delta_T_values.append(delta_T)

    voltage_values.append(V_teg)
    current_values.append(I_teg)
    power_values.append(P_teg)

# ==========================================================
# TEMPERATURE DIFFERENCE
# ==========================================================

plt.figure(figsize=(9,5))

plt.plot(
    time_axis,
    hot_side,
    label='Hot Side Temperature'
)

plt.plot(
    time_axis,
    cold_side,
    label='Cold Side Temperature'
)

plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')

plt.title(
    'TEG Thermal Gradient'
)

plt.grid(True)
plt.legend()

plt.tight_layout()

plt.savefig(
    'teg_temperature_gradient.png',
    dpi=300
)

plt.show()

# ==========================================================
# GENERATED VOLTAGE
# ==========================================================

plt.figure(figsize=(9,5))

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
    'teg_generated_voltage.png',
    dpi=300
)

plt.show()

# ==========================================================
# GENERATED POWER
# ==========================================================

plt.figure(figsize=(9,5))

plt.plot(
    time_axis,
    power_values,
    linewidth=2
)

plt.xlabel('Time (s)')
plt.ylabel('Power (W)')

plt.title(
    'TEG Generated Power'
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    'teg_generated_power.png',
    dpi=300
)

plt.show()

# ==========================================================
# FINAL VALUES
# ==========================================================

print("\n===== FINAL RESULTS =====")

print(
    f"Final Delta T: "
    f"{delta_T_values[-1]:.2f} °C"
)

print(
    f"Final Voltage: "
    f"{voltage_values[-1]:.6f} V"
)

print(
    f"Final Current: "
    f"{current_values[-1]:.6f} A"
)

print(
    f"Final Power: "
    f"{power_values[-1]:.8f} W"
)