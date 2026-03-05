import cadquery as cq

# -- Parametric Dimensions --
# Ring Dimensions
ring_id = 45.0          # Inner Diameter
ring_od = 65.0          # Outer Diameter
ring_height = 15.0      # Thickness of the ring

# Lug Dimensions
lug_neck_width = 12.0
lug_head_width = 24.0
lug_neck_length = 8.0
lug_head_length = 10.0
lug_total_reach = lug_neck_length + lug_head_length

# Detail Dimensions
chamfer_size = 3.0
hole_diameter = 4.0
hole_depth = 12.0

# -- Geometry Construction --

# 1. Create the central ring
# Centered at the origin (X=0, Y=0), extruded along Z
ring = (
    cq.Workplane("XY")
    .circle(ring_od / 2.0)
    .circle(ring_id / 2.0)
    .extrude(ring_height)
)

# 2. Design a single Lug
# We calculate coordinates to create a T-shaped profile.
# We ensure the lug starts slightly inside the ring (overlap) for a clean union.
overlap = 2.0
start_x = (ring_od / 2.0) - overlap
neck_end_x = start_x + lug_neck_length
end_x = neck_end_x + lug_head_length

# Define points for the T-shape profile (Counter-Clockwise)
lug_pts = [
    (start_x, -lug_neck_width / 2.0),
    (neck_end_x, -lug_neck_width / 2.0),
    (neck_end_x, -lug_head_width / 2.0),
    (end_x, -lug_head_width / 2.0),
    (end_x, lug_head_width / 2.0),
    (neck_end_x, lug_head_width / 2.0),
    (neck_end_x, lug_neck_width / 2.0),
    (start_x, lug_neck_width / 2.0)
]

# Create the base solid for the lug
lug_solid = (
    cq.Workplane("XY")
    .polyline(lug_pts)
    .close()
    .extrude(ring_height)
)

# Apply Chamfers to the outer face
# We select the face with the maximum X coordinate (the end of the lug)
# and chamfer its edges to create the faceted look.
lug_solid = (
    lug_solid
    .faces(">X")
    .edges()
    .chamfer(chamfer_size)
)

# Drill the mounting hole
# Create a hole on the outer face, going inwards (-X direction)
lug_solid = (
    lug_solid
    .faces(">X")
    .workplane()
    .hole(hole_diameter, hole_depth)
)

# 3. Pattern and Assembly
# Initialize the result with the ring
result = ring

# Rotate the lug 4 times (0, 90, 180, 270 degrees) and union with the ring
for i in range(4):
    angle = i * 90.0
    # Rotate about the Z-axis centered at origin
    rotated_lug = lug_solid.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.union(rotated_lug)
