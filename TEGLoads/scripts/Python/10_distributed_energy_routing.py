import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# STAGE 10
# DISTRIBUTED ENERGY ROUTING
# ==========================================================

grid_size = 20

time_steps = 600

dt = 0.1

# ==========================================================
# NODE PARAMETERS
# ==========================================================

generation_base = 4.0

load_power = 2.5

sharing_gain = 0.08

# ==========================================================
# INITIAL ENERGY GRID
# ==========================================================

energy_grid = np.random.uniform(
    4,
    7,
    (grid_size, grid_size)
)

# ==========================================================
# RANDOM NODE FAILURES
# ==========================================================

failure_map = np.zeros(
    (grid_size, grid_size)
)

for _ in range(25):

    x = np.random.randint(0, grid_size)
    y = np.random.randint(0, grid_size)

    failure_map[x, y] = 1

# ==========================================================
# STORAGE
# ==========================================================

average_energy_history = []

# ==========================================================
# SIMULATION LOOP
# ==========================================================

for step in range(time_steps):

    new_grid = energy_grid.copy()

    for i in range(grid_size):

        for j in range(grid_size):

            # ==============================================
            # NODE FAILURE
            # ==============================================

            if failure_map[i, j] == 1:

                generation = 0.0

            else:

                thermal_variation = (
                    1.0
                    * np.sin(
                        0.02 * step
                        + i * 0.2
                        + j * 0.2
                    )
                )

                generation = (
                    generation_base
                    + thermal_variation
                )

            # ==============================================
            # LOCAL ENERGY UPDATE
            # ==============================================

            new_grid[i, j] += (
                generation
                - load_power
            ) * dt

            # ==============================================
            # NEIGHBOR ENERGY SHARING
            # ==============================================

            neighbors = []

            if i > 0:
                neighbors.append((i-1, j))

            if i < grid_size-1:
                neighbors.append((i+1, j))

            if j > 0:
                neighbors.append((i, j-1))

            if j < grid_size-1:
                neighbors.append((i, j+1))

            for ni, nj in neighbors:

                energy_difference = (
                    energy_grid[i, j]
                    - energy_grid[ni, nj]
                )

                shared_energy = (
                    sharing_gain
                    * energy_difference
                    * dt
                )

                new_grid[i, j] -= shared_energy

            # ==============================================
            # ENERGY LIMITS
            # ==============================================

            new_grid[i, j] = np.clip(
                new_grid[i, j],
                0,
                20
            )

    energy_grid = new_grid.copy()

    average_energy_history.append(
        np.mean(energy_grid)
    )

# ==========================================================
# FINAL ENERGY MAP
# ==========================================================

plt.figure(figsize=(8,6))

plt.imshow(
    energy_grid,
    cmap='hot'
)

plt.colorbar(
    label='Stored Energy'
)

plt.title(
    'Distributed Energy Routing'
)

plt.tight_layout()

plt.savefig(
    'stage10_energy_map.png',
    dpi=300
)

plt.show()

# ==========================================================
# FAILURE MAP
# ==========================================================

plt.figure(figsize=(8,6))

plt.imshow(
    failure_map,
    cmap='gray'
)

plt.title(
    'Random Node Failures'
)

plt.tight_layout()

plt.savefig(
    'stage10_failure_map.png',
    dpi=300
)

plt.show()

# ==========================================================
# ENERGY STABILITY
# ==========================================================

plt.figure(figsize=(9,5))

plt.plot(
    average_energy_history,
    linewidth=2
)

plt.xlabel('Time Step')
plt.ylabel('Average Grid Energy')

plt.title(
    'Distributed Energy Stability'
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    'stage10_energy_stability.png',
    dpi=300
)

plt.show()