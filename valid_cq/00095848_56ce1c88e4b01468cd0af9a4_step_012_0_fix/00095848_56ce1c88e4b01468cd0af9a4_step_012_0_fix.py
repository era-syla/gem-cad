import cadquery as cq

# Parameters
length = 100.0   # extrusion length
wall_thickness = 3.0
base_thickness = 3.0
wall_height = 20.0
outer_width = 50.0  # total width from outer face to outer face

# 2D profile of U‐channel on the XY plane
profile = [
    (0, 0),
    (outer_width, 0),
    (outer_width, base_thickness),
    (outer_width - wall_thickness, base_thickness),
    (outer_width - wall_thickness, wall_height),
    (wall_thickness, wall_height),
    (wall_thickness, base_thickness),
    (0, base_thickness),
]

# Build the solid by extruding the profile
result = (
    cq.Workplane("XY")
      .polyline(profile)
      .close()
      .extrude(length)
)