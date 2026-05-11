import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# SIMULATION PARAMETERS
# ==========================================================

dt = 0.1
time_steps = 400

ambient_temperature = -5.0
target_temperature = 2.0

thermal_capacity = 8.0
heat_loss = 0.08

# ==========================================================
# PID PARAMETERS
# ==========================================================

Kp = 2.5
Ki = 0.12
Kd = 0.8

# ==========================================================
# INITIAL CONDITIONS
# ==========================================================

temperature_pid = 0.0
temperature_onoff = 0.0

integral = 0.0
previous_error = 0.0

# ==========================================================
# STORAGE
# ==========================================================

time_axis = []

pid_response = []
onoff_response = []

# ==========================================================
# SIMULATION LOOP
# ==========================================================

for step in range(time_steps):

    t = step * dt

    # ======================================================
    # ON/OFF CONTROLLER
    # ======================================================

    if temperature_onoff < target_temperature:
        heating_onoff = 1.2
    else:
        heating_onoff = 0.0

    dT_onoff = (
        heating_onoff
        - heat_loss * (temperature_onoff - ambient_temperature)
    ) / thermal_capacity

    temperature_onoff += dt * dT_onoff

    # ======================================================
    # PID CONTROLLER
    # ======================================================

    error = target_temperature - temperature_pid

    integral += error * dt

    derivative = (error - previous_error) / dt

    control_signal = (
        Kp * error
        + Ki * integral
        + Kd * derivative
    )

    control_signal = max(0.0, min(control_signal, 5.0))

    dT_pid = (
        control_signal
        - heat_loss * (temperature_pid - ambient_temperature)
    ) / thermal_capacity

    temperature_pid += dt * dT_pid

    previous_error = error

    # ======================================================
    # STORE DATA
    # ======================================================

    time_axis.append(t)

    pid_response.append(temperature_pid)
    onoff_response.append(temperature_onoff)

# ==========================================================
# PLOT
# ==========================================================

plt.figure(figsize=(8,5))

plt.plot(
    time_axis,
    onoff_response,
    label='ON/OFF Control',
    linewidth=2
)

plt.plot(
    time_axis,
    pid_response,
    label='PID Control',
    linewidth=2
)

plt.axhline(
    target_temperature,
    linestyle='--',
    label='Target Temperature'
)

plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')

plt.title('Controller Comparison')

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.savefig(
    'controller_comparison.png',
    dpi=300
)

plt.show()