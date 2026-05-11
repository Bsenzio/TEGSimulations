import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# SIMULATION PARAMETERS
# ==========================================================

dt = 0.1
time_steps = 1500

ambient_temperature = -5.0
target_temperature = 2.0

thermal_capacity = 8.0
heat_loss = 0.06

# ==========================================================
# PID PARAMETERS
# ==========================================================

# Classical PID
Kp = 2.5
Ki = 0.12
Kd = 0.55

# Adaptive PID
Kp_adaptive = 2.2
Ki_adaptive = 0.09
Kd_adaptive = 0.65

# ==========================================================
# INITIAL CONDITIONS
# ==========================================================

temperature_pid = 0.0
temperature_adaptive = 0.0

integral_pid = 0.0
integral_adaptive = 0.0

previous_error_pid = 0.0
previous_error_adaptive = 0.0

# ==========================================================
# KALMAN FILTER PARAMETERS
# ==========================================================

estimated_temperature = 0.0

P = 1.0
Q = 0.005
R = 0.05

# ==========================================================
# STORAGE
# ==========================================================

time_axis = []

pid_response = []
adaptive_response = []

measured_signal = []
estimated_signal = []

# ==========================================================
# SIMULATION LOOP
# ==========================================================

for step in range(time_steps):

    t = step * dt

    # ======================================================
    # ENVIRONMENTAL DISTURBANCE
    # ======================================================

    wind_disturbance = 0.18 * np.sin(0.10 * t)

    thermal_noise = np.random.normal(0, 0.025)

    # ======================================================
    # CLASSICAL PID
    # ======================================================

    error_pid = (
        target_temperature
        - temperature_pid
    )

    integral_pid += error_pid * dt

    integral_pid = np.clip(
        integral_pid,
        -8,
        8
    )

    derivative_pid = (
        error_pid
        - previous_error_pid
    ) / dt

    control_pid = (
        Kp * error_pid
        + Ki * integral_pid
        + Kd * derivative_pid
    )

    control_pid = np.clip(
        control_pid,
        0,
        4.0
    )

    dT_pid = (
        control_pid
        - heat_loss * (
            temperature_pid
            - ambient_temperature
        )
        - wind_disturbance
    ) / thermal_capacity

    temperature_pid += dt * dT_pid

    previous_error_pid = error_pid

    # ======================================================
    # SENSOR MEASUREMENT
    # ======================================================

    measured_temp = (
        temperature_adaptive
        + thermal_noise
    )

    # ======================================================
    # KALMAN FILTER
    # ======================================================

    predicted_temperature = estimated_temperature

    P = P + Q

    K = P / (P + R)

    estimated_temperature = (
        predicted_temperature
        + K * (
            measured_temp
            - predicted_temperature
        )
    )

    P = (1 - K) * P

    # ======================================================
    # ADAPTIVE PID
    # ======================================================

    adaptive_gain = (
        1.0
        + abs(
            target_temperature
            - estimated_temperature
        ) * 0.04
    )

    Kp_current = (
        Kp_adaptive
        * adaptive_gain
    )

    Ki_current = Ki_adaptive

    Kd_current = Kd_adaptive

    error_adaptive = (
        target_temperature
        - estimated_temperature
    )

    integral_adaptive += (
        error_adaptive * dt
    )

    integral_adaptive = np.clip(
        integral_adaptive,
        -8,
        8
    )

    derivative_adaptive = (
        error_adaptive
        - previous_error_adaptive
    ) / dt

    control_adaptive = (
        Kp_current * error_adaptive
        + Ki_current * integral_adaptive
        + Kd_current * derivative_adaptive
    )

    control_adaptive = np.clip(
        control_adaptive,
        0,
        4.0
    )

    dT_adaptive = (
        control_adaptive
        - heat_loss * (
            temperature_adaptive
            - ambient_temperature
        )
        - wind_disturbance
    ) / thermal_capacity

    temperature_adaptive += (
        dt * dT_adaptive
    )

    previous_error_adaptive = (
        error_adaptive
    )

    # ======================================================
    # STORE DATA
    # ======================================================

    time_axis.append(t)

    pid_response.append(
        temperature_pid
    )

    adaptive_response.append(
        temperature_adaptive
    )

    measured_signal.append(
        measured_temp
    )

    estimated_signal.append(
        estimated_temperature
    )

# ==========================================================
# CONTROLLER COMPARISON
# ==========================================================

plt.figure(figsize=(9,5))

plt.plot(
    time_axis,
    pid_response,
    label='Classical PID',
    linewidth=2
)

plt.plot(
    time_axis,
    adaptive_response,
    label='Adaptive PID + Kalman',
    linewidth=2
)

plt.axhline(
    target_temperature,
    linestyle='--',
    label='Target Temperature'
)

# Y AXIS EVERY 0.1°C
plt.yticks(
    np.arange(0, 2.21, 0.1)
)

plt.ylim(0, 2.2)

plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')

plt.title(
    'Adaptive PID vs Classical PID'
)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.savefig(
    'adaptive_pid_vs_pid.png',
    dpi=300
)

plt.show()

# ==========================================================
# KALMAN ESTIMATION
# ==========================================================

plt.figure(figsize=(9,5))

plt.plot(
    time_axis,
    measured_signal,
    label='Noisy Measurement',
    alpha=0.45
)

plt.plot(
    time_axis,
    estimated_signal,
    label='Kalman Estimation',
    linewidth=2
)

# Y AXIS EVERY 0.1°C
plt.yticks(
    np.arange(-0.2, 2.21, 0.1)
)

plt.ylim(-0.2, 2.2)

plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')

plt.title(
    'Kalman Thermal State Estimation'
)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.savefig(
    'kalman_estimation.png',
    dpi=300
)

plt.show()