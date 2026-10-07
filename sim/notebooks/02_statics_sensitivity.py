# %% [markdown]
# # 02 — How much moving mass keeps every cable taut? (Q-E1, Q-E5, D-11)
#
# Model: L1 point-mass statics. Moments ignored (ADR-0002).
#
# Key idea: every tension is proportional to the weight (tested in test_margin_scales_linearly_with_mass).
# So for each pulley height we compute ONE number — the worst slack margin per kg over the whole
# operating box — and the mass needed for any minimum tension follows directly:
#
#     m_needed = T_min / worst_margin_per_kg
#
# The robot must stay taut on the EMPTY return trip too, so the condition that matters is
#     empty mass (platform + gripper + any ballast)  ≥  m_needed
# and the ballast to add is  max(0, m_needed − current empty mass).

# %%
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cdpr import statics  # noqa: E402
from cdpr.params import load  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
RESULTS.mkdir(exist_ok=True)

empty = load(payload=None)
loaded = load()

# Operating box: the R-01 work area, from picking height to carrying height (R-02 lift).
WORK_HALF = 0.175
xs = ys = np.linspace(-WORK_HALF, WORK_HALF, 15)
zs = [0.10, 0.15, 0.20]
pulley_heights = np.round(np.arange(0.30, 0.571, 0.01), 3)
T_MINS = [0.2, 0.3, 0.5]                 # candidate minimum tensions (D-11 is still undecided)

# %% Worst margin per kg at each pulley height (the slow part, a few seconds)
k = np.array([statics.worst_margin_per_kg(empty.with_pulley_height(H), xs, ys, zs) for H in pulley_heights])

# %% Table: mass needed and ballast to add
print(f"Empty moving mass now: {empty.moving_mass:.3f} kg   Loaded: {loaded.moving_mass:.3f} kg\n")
print(f"{'pulley H':>9} {'margin':>10}" + "".join(f"   ballast @ {t} N" for t in T_MINS))
for H, kk in zip(pulley_heights, k):
    if round(H * 100) % 5:               # print every 50 mm; the plot has the rest
        continue
    row = "".join(f"{max(0.0, t / kk - empty.moving_mass):13.2f} kg  " for t in T_MINS)
    print(f"{H*1000:7.0f} mm {kk:7.2f} N/kg  {row}")

# %% Plot: mass needed vs pulley height, one line per T_min
BLUES = {0.2: "#86b6ef", 0.3: "#3987e5", 0.5: "#1c5cab"}   # one hue, light→dark = lenient→strict
fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
H_mm = pulley_heights * 1000

for t in T_MINS:
    m = t / k
    ax.plot(H_mm, m, color=BLUES[t], lw=2, label=f"T_min = {t} N")
    ax.annotate(f"{t} N", (H_mm[-1], m[-1]), xytext=(6, 0), textcoords="offset points",
                va="center", fontsize=9, color="#333333")

for mass, name in [(empty.moving_mass, "empty now"), (loaded.moving_mass, "loaded")]:
    ax.axhline(mass, color="#888888", lw=1, ls="--")
    ax.annotate(f"{name}\n{mass:.2f} kg", (H_mm[-1], mass), xytext=(6, -4), textcoords="offset points",
                va="top", fontsize=8.5, color="#555555")

ax.set_xlabel("Pulley height above work surface [mm]  (D-02)")
ax.set_ylabel("Moving mass needed to keep every cable taut [kg]")
ax.set_title("Mass needed so the slackest cable stays above T_min, anywhere in the\n"
             "350 × 350 mm work area at platform heights 100–200 mm (point-mass statics).\n"
             "Where a line is above 'empty now', the platform needs ballast.", fontsize=10)
ax.set_xlim(H_mm[0], H_mm[-1] + 60)
ax.set_ylim(0, None)
ax.grid(True, color="#e5e5e5", lw=0.6)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(0.0, 1.0))

out = RESULTS / "02_mass_needed.png"
fig.savefig(out, dpi=150)
print(f"\nSaved {out}")
