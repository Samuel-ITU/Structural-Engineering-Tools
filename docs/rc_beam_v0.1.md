# RC beam v0.1 — ACI 318-19
Scope: rectangular, singly reinforced, one tension layer, no axial force; normalweight concrete, nonprestressed, fy <= 550 MPa. SI internal units: mm, MPa, kN-m.

- Effective depth: d = h - cover - stirrup diameter - bar diameter/2.
- As = n*pi*db^2/4.
- Equivalent block: a = As*fy/(0.85*fc*b), c = a/beta1.
- beta1 = 0.85 for fc <= 28 MPa, decreases 0.05 per 7 MPa, min 0.65 (ACI 318-19 22.2.2.4.3).
- epsilon_t = 0.003*(d-c)/c.
- phi per ACI 318-19 Table 21.2.2: 0.65 at epsilon_y, 0.90 at epsilon_y+0.003, linear interpolation between.
- Mn = As*fy*(d-a/2), phiMn >= Mu.
- As,min = max(0.25*sqrt(fc)/fy*b*d, 1.4/fy*b*d) (ACI 318-19 9.6.1.2, SI).
- ACI 318-19 9.3.3.1 tensile strain requirement, detailing, bar spacing, development, deflection, shear, torsion, seismic and load combinations are NOT checked. A pass flag is only for the checks implemented; NOT a complete code compliance verdict.
- Check published code text and an independent benchmark before professional use.
