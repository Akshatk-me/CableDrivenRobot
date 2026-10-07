"""Load physical parameters from sim/params.yaml.

Every model function takes a `Params` object instead of reading numbers itself.
That keeps all numbers in one place (params.yaml) and makes design sweeps easy:
copy the Params, change one field, re-run.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
import yaml

DEFAULT_PATH = Path(__file__).resolve().parents[1] / "params.yaml"


@dataclass(frozen=True)
class Params:
    pulley_points: np.ndarray      # (4, 3) cable exit points A_i, world frame [m]
    attach_points: np.ndarray      # (4, 3) attachment points b_i, platform frame [m]
    moving_mass: float             # platform + gripper + payload [kg]
    min_tension: float             # below this a cable counts as slack [N]
    spool_radius: float            # [m]
    holding_torque: float          # motor torque at standstill [N·m]
    torque_margin: float           # usable fraction of available torque [-]
    g: float                       # [m/s²]

    @property
    def max_tension(self) -> float:
        """Largest cable tension the motor can hold within the torque margin, at standstill [N]."""
        return self.holding_torque * self.torque_margin / self.spool_radius

    def with_pulley_height(self, z: float) -> "Params":
        """Copy with all pulley exit points moved to height z [m] (ADR-0008: pulleys slide on the uprights)."""
        pts = self.pulley_points.copy()
        pts[:, 2] = z
        return replace(self, pulley_points=pts)


def load(path: str | Path = DEFAULT_PATH, payload: str | None = "mass") -> Params:
    """Read params.yaml.

    payload: "mass" (target payload, default), "mass_stretch" (stretch payload),
             or None (empty platform, e.g. the return trip after placing an object).
    """
    with open(path) as f:
        y = yaml.safe_load(f)
    v = lambda section, key: y[section][key]["value"]  # noqa: E731
    return Params(
        pulley_points=np.array(v("frame", "pulley_exit_points"), dtype=float),
        attach_points=np.array(v("platform", "attachment_points"), dtype=float),
        moving_mass=v("platform", "mass") + v("gripper", "mass") + (v("payload", payload) if payload else 0.0),
        min_tension=v("cable", "min_tension"),
        spool_radius=v("spool", "radius"),
        holding_torque=v("motor", "holding_torque"),
        torque_margin=v("motor", "torque_margin"),
        g=v("environment", "g"),
    )
