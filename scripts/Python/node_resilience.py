import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------
# PARAMETERS
# -----------------------------------

GRID_SIZE = 30
TIME_STEPS = 150

ambient_temp = -6.0
target_temp = 1.0

diffusion = 0.18
heating_power = 0.30

# Failure parameters
failure_ratio = 0.20

# -----------------------------------
# INITIAL GRID
# -----------------------------------

temperature = np.ones((GRID_SIZE, GRID_SIZE)) * ambient_temp

# Central heating region
for i in range(10, 20):
    for j in range(10, 20):
        temperature[i, j] = 1.0

# -----------------------------------
# NODE FAILURE MAP
# -----------------------------------

failure_map = np.ones((GRID_SIZE, GRID_SIZE))

num_failures = int(GRID_SIZE * GRID_SIZE * failure_ratio)

failed_indices = np.random.choice(
    GRID_SIZE * GRID_SIZE,
    num_failures,
    replace=False
)

for idx in failed_indices:
    x = idx // GRID_SIZE
    y = idx % GRID_SIZE
    failure_map[x, y] = 0

# -----------------------------------
# STORAGE
# -----------------------------------

avg_temp_normal = []
avg_temp_failure = []

# -----------------------------------
# NORMAL OPERATION
# -----------------------------------

temp_normal = temperature.copy()

for t in range(TIME_STEPS):

    new_temp = temp_normal.copy()

    for i in range(1, GRID_SIZE - 1):
        for j in range(1, GRID_SIZE - 1):

            laplacian = (
                temp_normal[i+1, j]
                + temp_normal[i-1, j]
                + temp_normal[i, j+1]
                + temp_normal[i, j-1]
                - 4 * temp_normal[i, j]
            )

            control = heating_power * (
                target_temp - temp_normal[i, j]
            )

            new_temp[i, j] += (
                diffusion * laplacian
                + 0.05 * control
            )

    temp_normal = new_temp
    avg_temp_normal.append(np.mean(temp_normal))

# -----------------------------------
# FAILURE + ADAPTIVE RECOVERY
# -----------------------------------

temp_failure = temperature.copy()

for t in range(TIME_STEPS):

    new_temp = temp_failure.copy()

    for i in range(1, GRID_SIZE - 1):
        for j in range(1, GRID_SIZE - 1):

            laplacian = (
                temp_failure[i+1, j]
                + temp_failure[i-1, j]
                + temp_failure[i, j+1]
                + temp_failure[i, j-1]
                - 4 * temp_failure[i, j]
            )

            # Failed node
            if failure_map[i, j] == 0:

                control = -0.08

            else:

                # Neighbor-aware adaptive recovery
                nearby_failures = (
                    failure_map[i+1, j] == 0
                    or failure_map[i-1, j] == 0
                    or failure_map[i, j+1] == 0
                    or failure_map[i, j-1] == 0
                )

                adaptive_gain = 1.1 if nearby_failures else 1.0

                control = (
                    adaptive_gain
                    * heating_power
                    * (target_temp - temp_failure[i, j])
                )

            new_temp[i, j] += (
                diffusion * laplacian
                + 0.05 * control
            )

    temp_failure = new_temp
    avg_temp_failure.append(np.mean(temp_failure))

# -----------------------------------
# THERMAL MAPS
# -----------------------------------

fig, axs = plt.subplots(
    1,
    3,
    figsize=(14, 4)
)

# Normal thermal distribution
im1 = axs[0].imshow(
    temp_normal,
    cmap='inferno',
    aspect='auto',
    vmin=-6,
    vmax=1.5
)

axs[0].set_title(
    "Normal Distribution",
    fontsize=10
)

axs[0].axis('off')

# Failure map
im2 = axs[1].imshow(
    failure_map,
    cmap='gray',
    aspect='auto'
)

axs[1].set_title(
    "Failure Map",
    fontsize=10
)

axs[1].axis('off')

# Adaptive recovery distribution
im3 = axs[2].imshow(
    temp_failure,
    cmap='inferno',
    aspect='auto',
    vmin=-6,
    vmax=1.5
)

axs[2].set_title(
    "Adaptive Recovery",
    fontsize=10
)

axs[2].axis('off')

# Compact colorbar
cbar = fig.colorbar(
    im3,
    ax=axs,
    shrink=0.75,
    pad=0.02
)

cbar.ax.tick_params(labelsize=8)

# Compact spacing
plt.subplots_adjust(
    left=0.04,
    right=0.96,
    top=0.88,
    bottom=0.10,
    wspace=0.08
)

plt.savefig(
    "fault_tolerant_thermal_maps.png",
    dpi=300,
    bbox_inches='tight'
)

# -----------------------------------
# STABILITY RESPONSE
# -----------------------------------

plt.figure(figsize=(8, 4))

plt.plot(
    avg_temp_normal,
    label='Normal Operation',
    linewidth=2
)

plt.plot(
    avg_temp_failure,
    label='Failure + Recovery',
    linewidth=2
)

plt.axhline(
    target_temp,
    linestyle='--',
    label='Target Temperature'
)

plt.xlabel("Time Step")
plt.ylabel("Average Temperature (°C)")

plt.title(
    "Fault-Tolerant Thermal Regulation",
    fontsize=11
)

plt.legend(fontsize=8)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "fault_tolerant_response.png",
    dpi=300,
    bbox_inches='tight'
)

plt.show()