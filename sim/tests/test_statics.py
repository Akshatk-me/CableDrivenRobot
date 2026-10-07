"""Sanity checks with answers we know independently of the code.

Good practice: every model layer gets tests like these before its results are trusted.
Run with:  uv run pytest
"""

import numpy as np
import pytest

from cdpr import kinematics, statics
from cdpr.params import load

PRM = load()


def test_cable_length_by_hand():
    # Platform level at the centre, 0.2 m up. Cable 1 runs from attachment (-0.05, -0.05, 0.2)
    # to pulley (-0.29, -0.29, H): a 0.24 x 0.24 x (H - 0.2) box diagonal.
    H = PRM.pulley_points[0, 2]
    expected = np.sqrt(0.24**2 + 0.24**2 + (H - 0.2) ** 2)
    L = kinematics.cable_lengths(np.array([0.0, 0.0, 0.2]), PRM)
    assert L == pytest.approx(np.full(4, expected))


def test_centre_tensions_equal_and_match_hand_calc():
    # By symmetry all four tensions are equal, and their vertical parts carry the weight:
    #   4 * T * cos(angle from vertical) = m g
    z = 0.2
    r = statics.solve_tensions(np.array([0.0, 0.0, z]), PRM)
    L = kinematics.cable_lengths(np.array([0.0, 0.0, z]), PRM)[0]
    cos_theta = (PRM.pulley_points[0, 2] - z) / L
    expected = PRM.moving_mass * PRM.g / (4 * cos_theta)
    assert r.feasible
    assert r.tensions == pytest.approx(np.full(4, expected))


@pytest.mark.parametrize("p", [[0.1, -0.05, 0.15], [-0.05, 0.04, 0.2], [0.0, 0.06, 0.15]])
def test_forces_balance_anywhere(p):
    # Whatever tensions we choose, they must exactly cancel gravity.
    p = np.array(p)
    r = statics.solve_tensions(p, PRM)
    U = kinematics.cable_directions(p, PRM).T
    assert r.taut_possible
    assert U @ r.tensions == pytest.approx([0.0, 0.0, PRM.moving_mass * PRM.g], abs=1e-9)
    assert np.all(r.tensions >= PRM.min_tension - 1e-9)


def test_outside_the_frame_is_not_holdable():
    # Beyond the pulleys, every cable pulls back toward the frame; nothing can hold the platform there.
    r = statics.solve_tensions(np.array([0.5, 0.0, 0.2]), PRM)
    assert not r.taut_possible


def test_lower_pulleys_mean_higher_tension():
    # Shallower cables need more tension to hold the same weight (hypothesis for Q-E1).
    p = np.array([0.0, 0.0, 0.15])
    t_high = statics.solve_tensions(p, PRM.with_pulley_height(0.57)).tensions[0]
    t_low = statics.solve_tensions(p, PRM.with_pulley_height(0.30)).tensions[0]
    assert t_low > t_high


@pytest.mark.parametrize("p", [[0.0, 0.0, 0.2], [0.12, 0.1, 0.1], [-0.15, 0.12, 0.25], [0.0, 0.17, 0.1]])
def test_margin_agrees_with_solver(p):
    # The point is holdable at min_tension exactly when the best slack margin reaches min_tension.
    p = np.array(p)
    margin = statics.best_slack_margin(p, PRM)
    assert statics.solve_tensions(p, PRM).taut_possible == (margin >= PRM.min_tension - 1e-9)


def test_margin_at_centre_is_equal_sharing():
    # At the centre the best you can do is share the load equally, so the margin equals that tension.
    p = np.array([0.0, 0.0, 0.2])
    assert statics.best_slack_margin(p, PRM) == pytest.approx(statics.solve_tensions(p, PRM).tensions[0])


def test_margin_scales_linearly_with_mass():
    # Every tension is proportional to the weight, so doubling mass doubles the slack margin.
    # This is what lets notebook 02 answer "how much mass?" without sweeping mass.
    from dataclasses import replace
    p = np.array([0.15, 0.12, 0.1])
    m1 = statics.best_slack_margin(p, PRM)
    m2 = statics.best_slack_margin(p, replace(PRM, moving_mass=2 * PRM.moving_mass))
    assert m2 == pytest.approx(2 * m1)
