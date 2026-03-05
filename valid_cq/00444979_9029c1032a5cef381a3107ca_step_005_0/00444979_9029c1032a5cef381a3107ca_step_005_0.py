import cadquery as cq

# Parametric dimensions estimated from the image
thickness = 2.0
ring_outer_radius = 6.0
ring_inner_radius = 4.5
arm_length = 65.0
arm_height_start = 10.0  # Height at the wide end (tip)
arm_height_end = 4.0     # Height at the narrow end (near ring)

# 1. Create the Arm Geometry
# Define a trapezoidal profile on the XY plane.
# The arm extends along the negative X-axis.
# The narrow end goes to x=0 to ensure full overlap with the ring before cutting the hole.
arm_points = [
    (-arm_length, arm_height_start / 2.0),
    (-arm_length, -arm_height_start / 2.0),
    (0, -arm_height_end / 2.0),
    (0, arm_height_end / 2.0)
]

arm = cq.Workplane("XY").polyline(arm_points).close().extrude(thickness)

# 2. Create the Outer Ring Geometry
# A solid cylinder centered at (0,0)
ring_outer = cq.Workplane("XY").circle(ring_outer_radius).extrude(thickness)

# 3. Combine and Cut
# Union the arm and the ring, then cut the center hole
result = (
    arm.union(ring_outer)
    .faces(">Z")
    .workplane()
    .circle(ring_inner_radius)
    .cutThruAll()
)