import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ==========================================================
# GRID PARAMETERS
# ==========================================================

GRID_SIZE = 10

dt = 0.1
time_steps = 400

ambient_temperature = -5.0

thermal_diffusion = 0.15
heat_loss = 0.02

target_temperature = 2.0

# ==========================================================
# INITIAL TEMPERATURE GRID
# ==========================================================

T = np.ones((GRID_SIZE, GRID_SIZE)) * ambient_temperature

# Central heated area
for i in range(3, 7):
    for j in range(3, 7):
        T[i, j] = 0.0

# ==========================================================
# SIMPLE LOCAL HEATING MODEL
# ==========================================================

def local_heating(temp):

    if temp < target_temperature:
        return 0.8

    return 0.0

# ==========================================================
# STORE HISTORY
# ==========================================================

history = []

# ==========================================================
# SIMULATION LOOP
# ==========================================================

for step in range(time_steps):

    T_new = T.copy()

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):

            center = T[i, j]

            up = T[i - 1, j] if i > 0 else center
            down = T[i + 1, j] if i < GRID_SIZE - 1 else center
            left = T[i, j - 1] if j > 0 else center
            right = T[i, j + 1] if j < GRID_SIZE - 1 else center

            laplacian = (
                up + down + left + right - 4 * center
            )

            diffusion_term = thermal_diffusion * laplacian

            heating_term = local_heating(center)

            loss_term = heat_loss * (center - ambient_temperature)

            dT = diffusion_term + heating_term - loss_term

            T_new[i, j] = center + dt * dT

    T = T_new

    history.append(T.copy())

# ==========================================================
# FINAL THERMAL MAP
# ==========================================================

plt.figure(figsize=(6, 5))

plt.imshow(
    T,
    cmap='inferno',
    origin='lower'
)

plt.colorbar(label='Temperature (°C)')

plt.title('Thermal Rooftop Distribution')

plt.xlabel('Node X')
plt.ylabel('Node Y')

plt.tight_layout()

plt.savefig(
    'thermal_map.png',
    dpi=300
)

plt.show()

# ==========================================================
# TRANSIENT RESPONSE
# ==========================================================

center_temperature = []

for frame in history:
    center_temperature.append(frame[5, 5])

time_axis = np.arange(time_steps) * dt

plt.figure(figsize=(7, 4))

plt.plot(
    time_axis,
    center_temperature,
    linewidth=2
)

plt.axhline(
    target_temperature,
    linestyle='--'
)

plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')

plt.title('Transient Thermal Response')

plt.grid(True)

plt.tight_layout()

plt.savefig(
    'transient_response.png',
    dpi=300
)

plt.show()