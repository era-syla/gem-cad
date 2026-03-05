import cadquery as cq

# Parameters
R_base = 15
R_small = 7.5
H_base = 10
H_cone = 80
H_top = 5
groove_depth = 1
groove_height = 1
groove1_z = 1
groove2_z = 3
hole_r = 2.5

# Build 2D profile in X-Z plane with grooves
points = [
    (R_base, 0),
    (R_base, groove1_z),
    (R_base - groove_depth, groove1_z),
    (R_base - groove_depth, groove1_z + groove_height),
    (R_base, groove1_z + groove_height),
    (R_base, groove2_z),
    (R_base - groove_depth, groove2_z),
    (R_base - groove_depth, groove2_z + groove_height),
    (R_base, groove2_z + groove_height),
    (R_base, H_base),
    (R_small, H_base + H_cone),
    (R_small, H_base + H_cone + H_top)
]

# Revolve the profile around Z axis
result = (
    cq.Workplane("XZ")
      .polyline(points)
      .close()
      .revolve(angleDegrees=360, axisStart=(0, 0, 0), axisEnd=(0, 0, 1))
)

# Drill the central hole from the top face
result = result.faces(">Z").workplane().circle(hole_r).cutThruAll()