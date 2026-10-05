import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from scipy.optimize import minimize

# ==============================================================================
# DEFAULT TUNABLE PARAMETERS
# ==============================================================================
FRAME_W = 500.0  # Frame X dimension (mm)
FRAME_L = 500.0  # Frame Y dimension (mm)
FRAME_H = 300.0  # Frame Z height (mm)

PLAT_W = 50.0  # Platform X width (mm)
PLAT_L = 50.0  # Platform Y length (mm)

CABLE_L = 350.0  # Nominal cable length for all 4 corners (mm)
# ==============================================================================


def rotation_matrix(roll, pitch, yaw):
    """Calculates 3D rotation matrix from Euler angles (radians)."""
    Rx = np.array(
        [[1, 0, 0], [0, np.cos(roll), -np.sin(roll)], [0, np.sin(roll), np.cos(roll)]]
    )

    Ry = np.array(
        [
            [np.cos(pitch), 0, np.sin(pitch)],
            [0, 1, 0],
            [-np.sin(pitch), 0, np.cos(pitch)],
        ]
    )

    Rz = np.array(
        [[np.cos(yaw), -np.sin(yaw), 0], [np.sin(yaw), np.cos(yaw), 0], [0, 0, 1]]
    )

    return Rz @ Ry @ Rx


def solve_equilibrium(x, y, frame_dim, plat_dim, L_cables):
    """
    Solves for [z, roll, pitch, yaw] given target (x, y) coordinates
    such that cable distance constraints are satisfied.
    """
    fw, fl, fh = frame_dim
    # CORRECT
    pw, pl = plat_dim[0] / 2.0, plat_dim[1] / 2.0

    # Frame anchor coordinates (Top 4 corners)
    C = np.array([[0, 0, fh], [fw, 0, fh], [fw, fl, fh], [0, fl, fh]])

    # Platform local corner coordinates relative to center
    P_local = np.array([[-pw, -pl, 0], [pw, -pl, 0], [pw, pl, 0], [-pw, pl, 0]])

    def objective(vars):
        z, roll, pitch, yaw = vars
        R = rotation_matrix(roll, pitch, yaw)
        P_world = np.array([x, y, z]) + (R @ P_local.T).T
        lengths = np.linalg.norm(P_world - C, axis=1)

        # Cable length constraint error
        err = np.sum((lengths - L_cables) ** 2)
        return err

    # Initial guess: z centered, zero tilt
    x0 = [fh - 100.0, 0.0, 0.0, 0.0]
    bounds = [
        (0, fh),
        (-np.pi / 3, np.pi / 3),
        (-np.pi / 3, np.pi / 3),
        (-np.pi / 3, np.pi / 3),
    ]

    res = minimize(objective, x0, method="L-BFGS-B", bounds=bounds)
    z, roll, pitch, yaw = res.x

    R = rotation_matrix(roll, pitch, yaw)
    P_world = np.array([x, y, z]) + (R @ P_local.T).T
    return z, roll, pitch, yaw, P_world, C


# Build Interactive Figure
fig = plt.figure(figsize=(11, 8))
ax = fig.add_subplot(111, projection="3d")
plt.subplots_adjust(bottom=0.25)

# Initial solution at workspace center
init_x, init_y = FRAME_W / 2.0, FRAME_L / 2.0
z, roll, pitch, yaw, P_world, C = solve_equilibrium(
    init_x,
    init_y,
    np.array([FRAME_W, FRAME_L, FRAME_H]),
    np.array([PLAT_W, PLAT_L]),
    np.array([CABLE_L] * 4),
)


def update_plot(val):
    ax.clear()

    curr_x = s_x.val
    curr_y = s_y.val
    curr_L = s_L.val

    z, roll, pitch, yaw, P, C_anchors = solve_equilibrium(
        curr_x,
        curr_y,
        np.array([FRAME_W, FRAME_L, FRAME_H]),
        np.array([PLAT_W, PLAT_L]),
        np.array([curr_L] * 4),
    )

    # 1. Draw 2020 Frame Wireframe
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

    # 2. Draw Platform Box
    P_closed = np.vstack([P, P[0]])
    ax.plot(
        P_closed[:, 0],
        P_closed[:, 1],
        P_closed[:, 2],
        "r-",
        lw=2.5,
        label="Platform (50x50mm)",
    )
    ax.scatter(curr_x, curr_y, z, color="red", s=30)

    # 3. Draw Cable Lines
    for i in range(4):
        ax.plot(
            [C_anchors[i, 0], P[i, 0]],
            [C_anchors[i, 1], P[i, 1]],
            [C_anchors[i, 2], P[i, 2]],
            "b-",
            lw=1.5,
        )

    # Set Aspect Ratio & Axis Limits
    ax.set_xlim([0, FRAME_W])
    ax.set_ylim([0, FRAME_L])
    ax.set_zlim([0, FRAME_H])
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_zlabel("Z (mm)")
    ax.set_title(
        f"Platform Center: ({curr_x:.1f}, {curr_y:.1f}, {z:.1f} mm) | Tilt: R={np.degrees(roll):.1f}°, P={np.degrees(pitch):.1f}°"
    )


# Add UI Sliders
ax_x = plt.axes([0.15, 0.12, 0.65, 0.03])
ax_y = plt.axes([0.15, 0.07, 0.65, 0.03])
ax_L = plt.axes([0.15, 0.02, 0.65, 0.03])

s_x = Slider(ax_x, "Platform X", 50.0, FRAME_W - 50.0, valinit=init_x)
s_y = Slider(ax_y, "Platform Y", 50.0, FRAME_L - 50.0, valinit=init_y)
s_L = Slider(ax_L, "Cable Length", 250.0, 450.0, valinit=CABLE_L)

s_x.on_changed(update_plot)
s_y.on_changed(update_plot)
s_L.on_changed(update_plot)

# Initial render
update_plot(None)
plt.show()
