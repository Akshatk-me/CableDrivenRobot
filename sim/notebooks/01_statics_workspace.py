# %% [markdown]
# # 01 — Statics: where can the platform be held? (Q-A1, Q-A2, first look at Q-E1)
#
# Model: L1 point-mass statics (sim/cdpr/statics.py). Moments are ignored; see ADR-0002.
#
# Metric: **slack margin** = the largest tension we can give the slackest cable at a point.
# A point is usable for a chosen minimum tension T_min exactly where slack margin ≥ T_min,
# so one map answers the question for every T_min.
#
# Run as a script (`uv run python sim/notebooks/01_statics_workspace.py`) or cell by cell in
# VS Code / Jupyter: the `# %%` markers make each block a cell.

# %%
import sys
from dataclasses import replace
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cdpr import statics  # noqa: E402
from cdpr.params import load  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
RESULTS.mkdir(exist_ok=True)

prm = load()
WORK_HALF = 0.175                       # R-01: 350 x 350 mm work area, centred
PULLEY_HEIGHTS = [0.30, 0.57]           # D-02 range from ADR-0008
PLATFORM_HEIGHTS = [0.10, 0.20]         # roughly: picking height, and carrying height (R-02 lift)
xs = ys = np.linspace(-0.27, 0.27, 109)

print(f"Moving mass {prm.moving_mass:.3f} kg  ->  weight {prm.moving_mass * prm.g:.2f} N")
print(f"Max tension within torque margin (standstill): {prm.max_tension:.1f} N")

# %% Compute slack margin and max tension over each grid
def maps(p, z):
    margin = np.full((len(ys), len(xs)), np.nan)
    tmax = np.full_like(margin, np.nan)
    for j, y in enumerate(ys):
        for i, x in enumerate(xs):
            pt = np.array([x, y, z])
            margin[j, i] = statics.best_slack_margin(pt, p)
            r = statics.solve_tensions(pt, replace(p, min_tension=0.0))
            if r.taut_possible:
                tmax[j, i] = r.tensions.max()
    return margin, tmax

results = {}
for H in PULLEY_HEIGHTS:
    for z in PLATFORM_HEIGHTS:
        results[H, z] = maps(prm.with_pulley_height(H), z)

# %% Summary over the R-01 work area
inside = (np.abs(xs)[None, :] <= WORK_HALF) & (np.abs(ys)[:, None] <= WORK_HALF)
print(f"\n{'pulley H':>9} {'platform z':>11} {'worst slack margin':>19} {'% area ≥0.2 N':>14} "
      f"{'% area ≥0.5 N':>14} {'worst max tension':>18}")
for (H, z), (margin, tmax) in results.items():
    m = margin[inside]
    print(f"{H:9.2f} {z:11.2f} {m.min():17.2f} N {100*np.mean(m >= 0.2):13.0f}% "
          f"{100*np.mean(m >= 0.5):13.0f}% {np.nanmax(tmax[inside]):16.1f} N")

# %% Plot: slack margin maps, one colour scale for all panels so they compare directly
fig, axes = plt.subplots(len(PULLEY_HEIGHTS), len(PLATFORM_HEIGHTS), figsize=(9, 8.6),
                         sharex=True, sharey=True, constrained_layout=True)
vmax = max(np.nanmax(m) for m, _ in results.values())
extent = [xs[0] * 1000, xs[-1] * 1000, ys[0] * 1000, ys[-1] * 1000]

for r, H in enumerate(PULLEY_HEIGHTS):
    for c, z in enumerate(PLATFORM_HEIGHTS):
        ax = axes[r, c]
        margin, _ = results[H, z]
        im = ax.imshow(np.clip(margin, 0, None), origin="lower", extent=extent,
                       cmap="Blues", vmin=0, vmax=vmax)
        cs = ax.contour(xs * 1000, ys * 1000, margin, levels=[0.2, 0.5],
                        colors=["#555555", "#111111"], linewidths=[1.0, 1.6], linestyles=["--", "-"])
        ax.clabel(cs, fmt={0.2: "0.2 N", 0.5: "0.5 N"}, fontsize=8)
        w = WORK_HALF * 1000
        ax.plot([-w, w, w, -w, -w], [-w, -w, w, w, -w], color="#c0392b", lw=1.2)
        ax.set_title(f"Pulleys at {H*1000:.0f} mm, platform at {z*1000:.0f} mm", fontsize=10)
        ax.grid(False)
        if r == len(PULLEY_HEIGHTS) - 1:
            ax.set_xlabel("x [mm]")
        if c == 0:
            ax.set_ylabel("y [mm]")

fig.colorbar(im, ax=axes, shrink=0.8, label="Slack margin: best tension in slackest cable [N]")
fig.suptitle("Where can all four cables stay taut?  Red square = R-01 work area (350 × 350 mm)\n"
             "Inside a contour, every cable can be kept above that tension", fontsize=11)
out = RESULTS / "01_slack_margin.png"
fig.savefig(out, dpi=150)
print(f"\nSaved {out}")
