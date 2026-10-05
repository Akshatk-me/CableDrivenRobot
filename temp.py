import matplotlib.pyplot as plt
import numpy as np

# Data
anchor_height = [250, 300, 350, 400, 450, 500, 550]
g70 = [9.8, 5.01, 2.77, 1.52, 0.75, 0.27, 0]
g120 = [11.88, 7.02, 4.67, 3.34, 2.5, 1.9, 1.52]
g180 = [12.8, 7.95, 5.57, 4.19, 3.28, 2.7, 2.23]
g250 = [13.33, 8.48, 6.07, 4.66, 3.74, 3.1, 2.63]

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot each series with markers
ax.plot(
    anchor_height,
    g70,
    "o-",
    label="70 g effector (unballasted)",
    linewidth=2,
    markersize=8,
    color="#1f77b4",
)
ax.plot(
    anchor_height, g120, "s-", label="120 g", linewidth=2, markersize=8, color="#ff7f0e"
)
ax.plot(
    anchor_height, g180, "^-", label="180 g", linewidth=2, markersize=8, color="#2ca02c"
)
ax.plot(
    anchor_height, g250, "d-", label="250 g", linewidth=2, markersize=8, color="#d62728"
)

# Labels - matching your image
ax.set_xlabel("anchor height above table (mm)", fontsize=12)
ax.set_ylabel("max acceleration (m/s²)", fontsize=12)
ax.set_title(
    "Acceleration limit before cable slack (200×200 mm workspace, travel height)",
    fontsize=13,
    fontweight="bold",
    pad=15,
)

# Grid
ax.grid(True, alpha=0.3)
ax.set_axisbelow(True)  # Put grid behind data

# Set y-axis limits to match your image (0 to 14)
ax.set_ylim(0, 14)
ax.set_xlim(230, 570)

# Legend - positioned to match your image style
ax.legend(loc="upper right", fontsize=10, framealpha=0.95)

# Add minor ticks
ax.minorticks_on()
ax.grid(True, which="minor", alpha=0.1)

# Tight layout and save
plt.tight_layout()
plt.savefig("acceleration_limit_cable_slack.png", dpi=300, bbox_inches="tight")
print("Plot saved as 'acceleration_limit_cable_slack.png'")

plt.show()
