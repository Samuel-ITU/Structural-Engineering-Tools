"""ACI 318-19 rectangular singly reinforced beam, SI units (mm, MPa, N-mm)."""
from dataclasses import dataclass
from math import sqrt, pi

@dataclass(frozen=True)
class BeamInput:
    b_mm: float
    h_mm: float
    cover_mm: float
    stirrup_diameter_mm: float
    bar_diameter_mm: float
    bar_count: int
    fc_mpa: float
    fy_mpa: float
    mu_knm: float
    Es_mpa: float = 200000.0

@dataclass(frozen=True)
class FlexureResult:
    As_mm2: float
    d_mm: float
    a_mm: float
    c_mm: float
    epsilon_t: float
    phi: float
    Mn_knm: float
    phi_Mn_knm: float
    utilization: float
    as_min_mm2: float
    passes: bool

def calculate_flexure(x: BeamInput) -> FlexureResult:
    """ACI 318-19: beta1 22.2.2.4.3; minimum As 9.6.1.2; phi Table 21.2.2.
    Scope: nonprestressed, normalweight, rectangular singly reinforced, fy<=550 MPa,
    fc 17-70 MPa; single tension layer; no axial load.
    """
    if not (17 <= x.fc_mpa <= 70 and 0 < x.fy_mpa <= 550 and x.Es_mpa > 0):
        raise ValueError("Unsupported material range")
    if not (x.b_mm > 0 and x.h_mm > 0 and x.cover_mm >= 0 and
            x.stirrup_diameter_mm >= 0 and x.bar_diameter_mm > 0 and
            isinstance(x.bar_count, int) and x.bar_count > 0 and x.mu_knm >= 0):
        raise ValueError("Invalid geometry, reinforcement or demand")
    d = x.h_mm - x.cover_mm - x.stirrup_diameter_mm - x.bar_diameter_mm / 2
    if d <= 0:
        raise ValueError("Nonpositive effective depth")
    As = x.bar_count * pi * x.bar_diameter_mm**2 / 4
    a = As * x.fy_mpa / (0.85 * x.fc_mpa * x.b_mm)
    beta1 = max(0.65, 0.85 - 0.05 * max(0.0, (x.fc_mpa - 28) / 7))
    c = a / beta1
    if c >= d:
        raise ValueError("Neutral axis beyond tension steel; outside model scope")
    eps_y = x.fy_mpa / x.Es_mpa
    eps_t = 0.003 * (d - c) / c
    if eps_t < eps_y:
        raise ValueError("Tension steel does not yield; this simplified model is inapplicable")
    # ACI 318-19 Table 21.2.2 for tied nonprestressed sections:
    # compression controlled at eps_t <= eps_y; tension controlled at eps_y+0.003.
    phi = 0.65 + 0.25 * min(1.0, max(0.0, (eps_t - eps_y) / 0.003))
    Mn = As * x.fy_mpa * (d - a / 2) / 1e6
    As_min = max(0.25 * sqrt(x.fc_mpa) / x.fy_mpa * x.b_mm * d,
                 1.4 / x.fy_mpa * x.b_mm * d)
    phi_Mn = phi * Mn
    util = x.mu_knm / phi_Mn if phi_Mn > 0 else float("inf")
    return FlexureResult(As, d, a, c, eps_t, phi, Mn, phi_Mn,
                         util, As_min, As >= As_min and util <= 1)
