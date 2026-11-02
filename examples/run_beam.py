from rc_beam import BeamInput, calculate_flexure

beam = BeamInput(b_mm=300, h_mm=550, cover_mm=40,
                 stirrup_diameter_mm=10, bar_diameter_mm=20,
                 bar_count=3, fc_mpa=28, fy_mpa=420, mu_knm=150)
result = calculate_flexure(beam)
for name, value in vars(result).items():
    print(f"{name}: {value}")
