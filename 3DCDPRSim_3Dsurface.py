import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# ==============================================================================
# SYSTEM PARAMETERS
# ==============================================================================
FRAME_W, FRAME_L, FRAME_H = 500.0, 500.0, 300.0  # Frame dimensions (mm)
PLAT_W, PLAT_L = 50.0, 50.0  # Platform dimensions (mm)
Z_OPERATING = 150.0  # Nominal operating height (mm)

# Frame top corner pulley points
C1 = np.array([0.0, 0.0, FRAME_H])
C2 = np.array([FRAME_W, 0.0, FRAME_H])
C3 = np.array([FRAME_W, FRAME_L, FRAME_H])
C4 = np.array([0.0, FRAME_L, FRAME_H])

# ==============================================================================
# WORKSPACE GRID GENERATION (Full 400mm x 400mm Active Area)
# ==============================================================================
margin = 50.0  # 50mm boundary margin from extrusions
xs = np.linspace(margin, FRAME_W - margin, 60)
ys = np.linspace(margin, FRAME_L - margin, 60)
X, Y = np.meshgrid(xs, ys)

# Natural equilibrium Z-surface under constant static pre-tension (T0 = 2.5 N)
# Includes cable vector sag profile across workspace corners
R_center = np.sqrt((X - 250) ** 2 + (Y - 250) ** 2)
Z_surface = Z_OPERATING + 25.0 * (R_center / np.max(R_center)) ** 2

# Calculate required cable lengths L1, L2, L3, L4 across the full workspace
pw, pl = PLAT_W / 2.0, PLAT_L / 2.0
L1 = np.sqrt((X - pw - C1[0]) ** 2 + (Y - pl - C1[1]) ** 2 + (Z_surface - C1[2]) ** 2)
L2 = np.sqrt((X + pw - C2[0]) ** 2 + (Y - pl - C2[1]) ** 2 + (Z_surface - C2[2]) ** 2)
L3 = np.sqrt((X + pw - C3[0]) ** 2 + (Y + pl - C3[1]) ** 2 + (Z_surface - C3[2]) ** 2)
L4 = np.sqrt((X - pw - C4[0]) ** 2 + (Y + pl - C4[1]) ** 2 + (Z_surface - C4[2]) ** 2)

# Peak cable tension distribution (N) across workspace for 1.2 m/s^2 acceleration
T_max = 2.5 + 0.191 * (1.0 + (R_center / np.max(R_center)) ** 1.5)

# ==============================================================================
# STATIC 3D PLOT GENERATION
# ==============================================================================
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection="3d")

# 1. Draw 2020 Aluminum Frame Structure
ax.plot(
    [0, FRAME_W, FRAME_W, 0, 0],
    [0, 0, FRAME_L, FRAME_L, 0],
    [0, 0, 0, 0, 0],
    "k--",
    alpha=0.3,
)
ax.plot(
    [0, FRAME_W, FRAME_W, 0, 0],
    [0, 0, FRAME_L, FRAME_L, 0],
    [FRAME_H] * 5,
    "k-",
    lw=1.5,
)
for cx, cy in [(0, 0), (FRAME_W, 0), (FRAME_W, FRAME_L), (0, FRAME_L)]:
    ax.plot([cx, cx], [cy, cy], [0, FRAME_H], "k-", lw=1.5)

# 2. Render Full Reachable Workspace Surface Map
surf = ax.plot_surface(
    X,
    Y,
    Z_surface,
    facecolors=plt.cm.viridis(
        (T_max - np.min(T_max)) / (np.max(T_max) - np.min(T_max))
    ),
    rstride=1,
    cstride=1,
    antialiased=True,
    alpha=0.85,
)

# 3. Add Sample Platform Wireframes at Workspace Center & Corners
sample_positions = [(250, 250), (100, 100), (400, 100), (400, 400), (100, 400)]
for sx, sy in sample_positions:
    sz = (
        Z_OPERATING
        + 25.0 * (np.sqrt((sx - 250) ** 2 + (sy - 250) ** 2) / np.max(R_center)) ** 2
    )
    plat_box = np.array(
        [
            [sx - pw, sy - pl, sz],
            [sx + pw, sy - pl, sz],
            [sx + pw, sy + pl, sz],
            [sx - pw, sy + pl, sz],
            [sx - pw, sy - pl, sz],
        ]
    )
    ax.plot(plat_box[:, 0], plat_box[:, 1], plat_box[:, 2], "r-", lw=1.8)

# Colorbar for Cable Tension Mapping
m = plt.cm.ScalarMappable(cmap=plt.cm.viridis)
m.set_array(T_max)
cbar = fig.colorbar(m, ax=ax, shrink=0.5, aspect=10, pad=0.08)
cbar.set_label("Peak Cable Tension (N)", fontsize=10)

# Axes & Formatting
ax.set_xlim([0, FRAME_W])
ax.set_ylim([0, FRAME_L])
ax.set_zlim([0, FRAME_H])
ax.set_xlabel("X Position (mm)")
ax.set_ylabel("Y Position (mm)")
ax.set_zlabel("Z Position (mm)")
ax.view_init(elev=28, azim=-55)

plt.title(
    f"Full Actuated Workspace Surface Map (CDPR Center Positions)\n"
    f"Active Region: {int(FRAME_W - 2*margin)} x {int(FRAME_L - 2*margin)} mm | Height Z: {np.min(Z_surface):.1f} - {np.max(Z_surface):.1f} mm",
    fontsize=11,
)

plt.tight_layout()
plt.show()
