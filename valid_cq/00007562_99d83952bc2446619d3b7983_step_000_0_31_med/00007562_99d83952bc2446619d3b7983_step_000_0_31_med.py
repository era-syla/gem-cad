import cadquery as cq

# Parameters for the geometric features
thickness = 10.0

# Body parameters
body_width = 40.0
body_height = 25.0
body_fillet = 4.0

# Head parameters
head_radius = 14.0
head_hole_diameter = 10.0
head_y_offset = 14.0  # Centers the head relative to the body

# Base/Legs parameters
base_width = 20.0
base_height = 12.0
base_y_offset = -16.0  # Centers the base relative to the body

# 1. Create the central body (rounded rectangle)
body = (
    cq.Workplane("XY")
    .box(body_width, body_height, thickness)
    .edges("|Z")
    .fillet(body_fillet)
)

# 2. Create the lower base part
base = (
    cq.Workplane("XY")
    .center(0, base_y_offset)
    .box(base_width, base_height, thickness)
)

# 3. Create the circular head
head = (
    cq.Workplane("XY")
    .center(0, head_y_offset)
    .circle(head_radius)
    .extrude(thickness / 2.0, both=True)
)

# 4. Combine all solid parts
result = body.union(base).union(head)

# 5. Add the through-hole in the head
result = (
    result.faces(">Z")
    .workplane()
    .center(0, head_y_offset)
    .hole(head_hole_diameter)
)

# 6. Apply a slight chamfer/fillet to outer edges for realism (optional based on image highlights)
try:
    result = result.faces(">Z or <Z").edges().fillet(0.5)
except:
    pass