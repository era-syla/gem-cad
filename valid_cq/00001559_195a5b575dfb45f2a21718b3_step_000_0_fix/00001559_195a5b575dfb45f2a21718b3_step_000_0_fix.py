import cadquery as cq

# Parameters
length = 80
width = 20
height_back = 20
height_front = 10
front_fillet = 10

# Sketch the side profile: a trapezoid sloping from full height at the back to lower height at the front
profile = [
    (0, 0),
    (length, 0),
    (length, height_front),
    (0, height_back),
]

# Build solid by extruding the profile, then fillet the top-front vertical edge
result = (
    cq.Workplane("XZ")
      .polyline(profile)
      .close()
      .extrude(width)
      .edges("<X and >Z")
      .fillet(front_fillet)
)