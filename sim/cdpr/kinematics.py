"""L0 — Kinematics: geometry only, no forces.

Question it answers: for a platform at position p (and orientation R), how long is each cable,
and which way does each cable pull?

Picture one cable:
    A_i  = the point where cable i leaves its top pulley   (fixed, world frame)
    b_i  = where cable i is tied on the platform           (fixed, platform frame)
    p + R @ b_i = that tie point in the world frame        (moves with the platform)

The cable is a straight line between those two points, so
    cable vector  v_i = A_i - (p + R @ b_i)      points from platform up to the pulley
    length        L_i = |v_i|
    direction     u_i = v_i / L_i                unit vector: the direction cable i pulls the platform
"""

from __future__ import annotations

import numpy as np

from .params import Params


def cable_vectors(p: np.ndarray, prm: Params, R: np.ndarray | None = None) -> np.ndarray:
    """Vectors from each attachment point to its pulley, shape (4, 3). R defaults to a level platform."""
    R = np.eye(3) if R is None else R
    attach_world = p + prm.attach_points @ R.T     # (4, 3): each row is p + R @ b_i
    return prm.pulley_points - attach_world


def cable_lengths(p: np.ndarray, prm: Params, R: np.ndarray | None = None) -> np.ndarray:
    """Cable lengths L_i [m], shape (4,). This is the inverse kinematics the controller runs."""
    return np.linalg.norm(cable_vectors(p, prm, R), axis=1)


def cable_directions(p: np.ndarray, prm: Params, R: np.ndarray | None = None) -> np.ndarray:
    """Unit vectors u_i along each cable, pointing from the platform toward the pulley, shape (4, 3)."""
    v = cable_vectors(p, prm, R)
    return v / np.linalg.norm(v, axis=1, keepdims=True)
