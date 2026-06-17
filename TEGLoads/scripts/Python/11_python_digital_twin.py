import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ==========================================================
# DIGITAL TWIN PARAMETERS
# ==========================================================

GRID_X = 20
GRID_Y = 20

dt = 0.1

ambient_temperature = -6.0
target_temperature = 2.0

thermal_diffusion = 0.12

# ==========================================================
# THERMAL GRID
# ==========================================================

temperature = np.ones(
    (GRID_X, GRID_Y)
) * ambient_temperature

# ==========================================================
# ENERGY STORAGE
# ==========================================================

supercapacitor = np.zeros(
    (GRID_X, GRID_Y)
)

battery_soc = np.ones(
    (GRID_X, GRID_Y)
) * 0.5

# ==========================================================
# NODE STATES
# ==========================================================

fault_map = np.zeros(
    (GRID_X, GRID_Y)
)

# Random node failures

for _ in range(15):

    x = np.random.randint(0, GRID_X)
    y = np.random.randint(0, GRID_Y)

    fault_map[x,y] = 1

# ==========================================================
# PID STATES
# ==========================================================

integral_error = np.zeros(
    (GRID_X, GRID_Y)
)

previous_error = np.zeros(
    (GRID_X, GRID_Y)
)

# ==========================================================
# KALMAN FILTER STATES
# ==========================================================

estimated_temperature = np.copy(
    temperature
)

P = np.ones((GRID_X, GRID_Y))

Q = 0.01
R = 0.08

# ==========================================================
# FIGURE
# ==========================================================

fig, ax = plt.subplots(figsize=(8,8))

thermal_plot = ax.imshow(
    temperature,
    cmap='jet',
    vmin=-8,
    vmax=4
)

plt.colorbar(
    thermal_plot,
    label='Temperature (°C)'
)

ax.set_title(
    'Stage 11 Digital Twin Thermal Infrastructure'
)

# ==========================================================
# UPDATE FUNCTION
# ==========================================================

def update(frame):

    global temperature
    global estimated_temperature
    global P

    new_temperature = np.copy(
        temperature
    )

    # ======================================================
    # NODE SIMULATION
    # ======================================================

    for i in range(1, GRID_X-1):
        for j in range(1, GRID_Y-1):

            # ==============================================
            # NODE FAILURE
            # ==============================================

            if fault_map[i,j] == 1:

                continue

            # ==============================================
            # THERMAL DIFFUSION
            # ==============================================

            diffusion = (

                temperature[i+1,j]
                + temperature[i-1,j]
                + temperature[i,j+1]
                + temperature[i,j-1]

                - 4 * temperature[i,j]
            )

            # ==============================================
            # THERMOELECTRIC GENERATION
            # ==============================================

            deltaT = (
                temperature[i,j]
                - ambient_temperature
            )

            voltage = 0.02 * deltaT

            harvested_energy = (
                voltage * 0.08
            )

            # ==============================================
            # SUPERCAPACITOR CHARGING
            # ==============================================

            supercapacitor[i,j] += (
                harvested_energy * dt
            )

            supercapacitor[i,j] = np.clip(
                supercapacitor[i,j],
                0,
                5
            )

            # ==============================================
            # BATTERY CHARGING
            # ==============================================

            battery_soc[i,j] += (
                harvested_energy * 0.001
            )

            battery_soc[i,j] = np.clip(
                battery_soc[i,j],
                0,
                1
            )

            # ==============================================
            # SENSOR MEASUREMENT
            # ==============================================

            noisy_measurement = (
                temperature[i,j]
                + np.random.normal(0,0.08)
            )

            # ==============================================
            # KALMAN FILTER
            # ==============================================

            predicted_temp = (
                estimated_temperature[i,j]
            )

            P[i,j] = P[i,j] + Q

            K = (
                P[i,j]
                /
                (P[i,j] + R)
            )

            estimated_temperature[i,j] = (

                predicted_temp

                + K * (
                    noisy_measurement
                    - predicted_temp
                )
            )

            P[i,j] = (
                (1-K) * P[i,j]
            )

            # ==============================================
            # ADAPTIVE PID
            # ==============================================

            error = (
                target_temperature
                - estimated_temperature[i,j]
            )

            integral_error[i,j] += (
                error * dt
            )

            derivative = (
                error
                - previous_error[i,j]
            ) / dt

            adaptive_gain = (
                1
                + abs(error)*0.1
            )

            Kp = 2.0 * adaptive_gain
            Ki = 0.05
            Kd = 0.45

            control_signal = (

                Kp * error
                + Ki * integral_error[i,j]
                + Kd * derivative
            )

            control_signal = np.clip(
                control_signal,
                0,
                4
            )

            previous_error[i,j] = error

            # ==============================================
            # THERMAL UPDATE
            # ==============================================

            heat_loss = (
                temperature[i,j]
                - ambient_temperature
            ) * 0.03

            new_temperature[i,j] += (

                thermal_diffusion
                * diffusion

                + control_signal * 0.08

                - heat_loss
            )

    # ======================================================
    # FAULT COMPENSATION
    # ======================================================

    for i in range(1, GRID_X-1):
        for j in range(1, GRID_Y-1):

            if fault_map[i,j] == 1:

                neighbors = [

                    (i+1,j),
                    (i-1,j),
                    (i,j+1),
                    (i,j-1)
                ]

                for nx, ny in neighbors:

                    if fault_map[nx,ny] == 0:

                        new_temperature[nx,ny] += 0.03

    temperature = new_temperature

    # ======================================================
    # VISUALIZATION
    # ======================================================

    display_grid = np.copy(
        temperature
    )

    # Failed nodes shown colder

    display_grid[fault_map == 1] = -8

    thermal_plot.set_array(
        display_grid
    )

    return [thermal_plot]

# ==========================================================
# ANIMATION
# ==========================================================

ani = FuncAnimation(
    fig,
    update,
    interval=50,
    blit=True
)

plt.show()