import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# STAGE 6
# FAULT-TOLERANT DISTRIBUTED THERMAL GRID
# ==========================================================

# ==========================================================
# SIMULATION PARAMETERS
# ==========================================================

dt = 0.1

time_steps = 1000

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

thermal_diffusion = 0.20

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
# NODE FAILURE MAP
# ==========================================================

failure_map = np.ones(
    (grid_size, grid_size)
)

# ==========================================================
# RANDOM NODE FAILURES
# ==========================================================

np.random.seed(42)

failure_probability = 0.12

for i in range(grid_size):

    for j in range(grid_size):

        if np.random.rand() < failure_probability:

            failure_map[i, j] = 0

# ==========================================================
# STORAGE
# ==========================================================

average_temperature = []

active_nodes_history = []

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

            local_temp = (
                temperature_grid[i, j]
            )

            # ==============================================
            # FAILED NODE
            # ==============================================

            if failure_map[i, j] == 0:

                # failed node loses heat faster

                dT_failed = (
                    - heat_loss
                    * (
                        local_temp
                        - ambient_temperature
                    )
                ) / thermal_capacity

                new_temperature_grid[i, j] += (
                    dt * dT_failed
                )

                continue

            # ==============================================
            # TEMPERATURE DIFFERENCE
            # ==============================================

            delta_T = (
                local_temp
                - ambient_temperature
            )

            # ==============================================
            # TEG GENERATION
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
            # BASE HEATER POWER
            # ==============================================

            heater_power = (
                supercap_grid[i, j] ** 2
            ) / heater_resistance

            # ==============================================
            # NEIGHBOR FAILURE COMPENSATION
            # ==============================================

            compensation_factor = 1.0

            # UP
            if i > 0:

                if failure_map[i - 1, j] == 0:

                    compensation_factor += 0.15

            # DOWN
            if i < grid_size - 1:

                if failure_map[i + 1, j] == 0:

                    compensation_factor += 0.15

            # LEFT
            if j > 0:

                if failure_map[i, j - 1] == 0:

                    compensation_factor += 0.15

            # RIGHT
            if j < grid_size - 1:

                if failure_map[i, j + 1] == 0:

                    compensation_factor += 0.15

            heater_power *= compensation_factor

            # ==============================================
            # THERMAL DIFFUSION
            # ==============================================

            diffusion_term = 0.0

            neighbors = 0

            directions = [
                (-1,0),
                (1,0),
                (0,-1),
                (0,1)
            ]

            for di, dj in directions:

                ni = i + di
                nj = j + dj

                if (
                    0 <= ni < grid_size
                    and
                    0 <= nj < grid_size
                ):

                    diffusion_term += (
                        temperature_grid[ni, nj]
                        - local_temp
                    )

                    neighbors += 1

            if neighbors > 0:

                diffusion_term /= neighbors

            # ==============================================
            # ENVIRONMENT DISTURBANCE
            # ==============================================

            wind_disturbance = (
                0.18
                * np.sin(
                    0.03 * t
                    + i * 0.15
                    + j * 0.12
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
    # UPDATE GRID
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

    active_nodes_history.append(
        np.sum(failure_map)
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
    label='Average Temperature'
)

plt.axhline(
    target_temperature,
    linestyle='--',
    label='Target Temperature'
)

plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')

plt.title(
    'Fault-Tolerant Thermal Regulation'
)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.show()

# ==========================================================
# FAILURE MAP
# ==========================================================

plt.figure(figsize=(8,7))

plt.imshow(
    failure_map,
    cmap='gray_r',
    interpolation='nearest'
)

plt.colorbar(
    label='Node Status'
)

plt.title(
    'Fault Map (Black = Failed Node)'
)

plt.tight_layout()

plt.show()

# ==========================================================
# FINAL TEMPERATURE MAP
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
    'Final Thermal Distribution'
)

plt.tight_layout()

plt.show()

# ==========================================================
# SUPERCAP MAP
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
    'Distributed Supercapacitor Voltage'
)

plt.tight_layout()

plt.show()