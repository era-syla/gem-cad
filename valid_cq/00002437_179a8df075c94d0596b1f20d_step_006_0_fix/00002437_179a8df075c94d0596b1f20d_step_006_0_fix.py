import cadquery as cq

# Parameters
r_outer = 50.0      # outer radius
rim_height = 2.0    # height of the outer vertical rim
dome_height = 5.0   # total height at center

# Construct half‐section profile and revolve
profile = [
    (r_outer, 0),
    (r_outer, rim_height),
    (r_outer - 2.0, rim_height + 1.0),
    (0, dome_height),
    (0, 0)
]

result = (
    cq.Workplane("XZ")
      .polyline(profile)
      .close()
      .revolve(360)
)