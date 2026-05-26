import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# STAGE 5
# DISTRIBUTED THERMOELECTRIC GRID
# ==========================================================

# ==========================================================
# SIMULATION PARAMETERS
# ==========================================================

dt = 0.1

time_steps = 800

# ==========================================================
# GRID PARAMETERS
# ==========================================================

grid_size = 20

# ==========================================================
# THERMAL PARAMETERS
# ==========================================================

ambient_temperature = -8.0

target_temperature = 2.0

thermal_capacity = 12.0

heat_loss = 0.04

thermal_diffusion = 0.18

# ==========================================================
# TEG PARAMETERS
# ==========================================================

seebeck_coefficient = 0.05

# ==========================================================
# SUPERCAP PARAMETERS
# ==========================================================

supercap_capacity = 5.0

# ==========================================================
# HEATER PARAMETERS
# ==========================================================

heater_resistance = 5.0

# ==========================================================
# INITIAL STATES
# ==========================================================

temperature_grid = np.full(
    (grid_size, grid_size),
    -6.0
)

supercap_grid = np.zeros(
    (grid_size, grid_size)
)

# ==========================================================
# STORAGE
# ==========================================================

average_temperature = []

average_voltage = []

time_axis = []

# ==========================================================
# SIMULATION LOOP
# ==========================================================

for step in range(time_steps):

    t = step * dt

    new_temperature_grid = (
        temperature_grid.copy()
    )

    # ======================================================
    # PROCESS EACH NODE
    # ======================================================

    for i in range(grid_size):

        for j in range(grid_size):

            # ==============================================
            # LOCAL TEMPERATURE
            # ==============================================

            local_temp = temperature_grid[i, j]

            # ==============================================
            # TEMPERATURE DIFFERENCE
            # ==============================================

            delta_T = (
                local_temp
                - ambient_temperature
            )

            # ==============================================
            # TEG VOLTAGE
            # ==============================================

            teg_voltage = (
                seebeck_coefficient
                * delta_T
            )

            # ==============================================
            # SUPERCAP CHARGING
            # ==============================================

            charging_current = (
                teg_voltage
                - supercap_grid[i, j]
            ) * 0.08

            dV = (
                charging_current
                / supercap_capacity
            )

            supercap_grid[i, j] += (
                dt * dV
            )

            # ==============================================
            # HEATER POWER
            # ==============================================

            heater_power = (
                supercap_grid[i, j] ** 2
            ) / heater_resistance

            # ==============================================
            # THERMAL DIFFUSION
            # ==============================================

            diffusion_term = 0.0

            neighbors = 0

            # UP
            if i > 0:

                diffusion_term += (
                    temperature_grid[i - 1, j]
                    - local_temp
                )

                neighbors += 1

            # DOWN
            if i < grid_size - 1:

                diffusion_term += (
                    temperature_grid[i + 1, j]
                    - local_temp
                )

                neighbors += 1

            # LEFT
            if j > 0:

                diffusion_term += (
                    temperature_grid[i, j - 1]
                    - local_temp
                )

                neighbors += 1

            # RIGHT
            if j < grid_size - 1:

                diffusion_term += (
                    temperature_grid[i, j + 1]
                    - local_temp
                )

                neighbors += 1

            if neighbors > 0:

                diffusion_term /= neighbors

            # ==============================================
            # WIND DISTURBANCE
            # ==============================================

            wind_disturbance = (
                0.15
                * np.sin(
                    0.03 * t
                    + i * 0.2
                    + j * 0.1
                )
            )

            # ==============================================
            # THERMAL DYNAMICS
            # ==============================================

            dT = (
                heater_power
                - heat_loss
                * (
                    local_temp
                    - ambient_temperature
                )
                + thermal_diffusion
                * diffusion_term
                - wind_disturbance
            ) / thermal_capacity

            # ==============================================
            # UPDATE NODE
            # ==============================================

            new_temperature_grid[i, j] += (
                dt * dT
            )

    # ======================================================
    # UPDATE ENTIRE GRID
    # ======================================================

    temperature_grid = (
        new_temperature_grid
    )

    # ======================================================
    # STORE DATA
    # ======================================================

    average_temperature.append(
        np.mean(temperature_grid)
    )

    average_voltage.append(
        np.mean(supercap_grid)
    )

    time_axis.append(t)

# ==========================================================
# TEMPERATURE EVOLUTION
# ==========================================================

plt.figure(figsize=(10,5))

plt.plot(
    time_axis,
    average_temperature,
    linewidth=2,
    label='Average Roof Temperature'
)

plt.axhline(
    target_temperature,
    linestyle='--',
    label='Target Temperature'
)

plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')

plt.title(
    'Distributed Thermal Grid Regulation'
)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.show()

# ==========================================================
# SUPERCAP VOLTAGE EVOLUTION
# ==========================================================

plt.figure(figsize=(10,5))

plt.plot(
    time_axis,
    average_voltage,
    linewidth=2
)

plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')

plt.title(
    'Average Supercapacitor Voltage'
)

plt.grid(True)

plt.tight_layout()

plt.show()

# ==========================================================
# FINAL THERMAL MAP
# ==========================================================

plt.figure(figsize=(8,7))

plt.imshow(
    temperature_grid,
    cmap='hot',
    interpolation='nearest'
)

plt.colorbar(
    label='Temperature (°C)'
)

plt.title(
    'Final Distributed Thermal Map'
)

plt.tight_layout()

plt.show()

# ==========================================================
# FINAL SUPERCAP MAP
# ==========================================================

plt.figure(figsize=(8,7))

plt.imshow(
    supercap_grid,
    cmap='viridis',
    interpolation='nearest'
)

plt.colorbar(
    label='Voltage (V)'
)

plt.title(
    'Distributed Supercapacitor Voltage Map'
)

plt.tight_layout()

plt.show()