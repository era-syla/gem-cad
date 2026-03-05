import cadquery as cq

# Parameters defining the dimensions of the object
body_width = 40.0
body_height = 40.0
thickness = 15.0
body_corner_fillet = 5.0

# The circular head dimensions
head_radius = 14.0
# Position the head so its center is aligned with the top edge of the body
head_center_y = body_height / 2.0
hole_radius = 6.5

# The bottom tab dimensions
tab_width = 20.0
tab_height = 8.0
# Position the tab below the body
tab_center_y = -(body_height / 2.0) - (tab_height / 2.0)

# Radius for the final edge finishing (rounded edges on faces)
face_edge_fillet = 1.0

# 1. Create the main rectangular body
# Using a box centered at the origin
main_body = cq.Workplane("XY").box(body_width, body_height, thickness)

# 2. Fillet the vertical corners of the main body
# Select edges parallel to the Z axis
main_body = main_body.edges("|Z").fillet(body_corner_fillet)

# 3. Create the circular head geometry
head = (
    cq.Workplane("XY")
    .moveTo(0, head_center_y)
    .circle(head_radius)
    .extrude(thickness / 2.0, both=True)  # Extrude symmetrically to match box
)

# 4. Create the bottom tab geometry
tab = (
    cq.Workplane("XY")
    .moveTo(0, tab_center_y)
    .rect(tab_width, tab_height)
    .extrude(thickness / 2.0, both=True)
)

# 5. Union the head and tab onto the main body
base_shape = main_body.union(head).union(tab)

# 6. Create and cut the through-hole in the head
hole = (
    cq.Workplane("XY")
    .moveTo(0, head_center_y)
    .circle(hole_radius)
    .extrude(thickness, both=True) # Ensure it cuts through entirely
)

shape_with_hole = base_shape.cut(hole)

# 7. Apply fillets to the edges of the front and back faces
# This creates the smooth, molded look shown in the image
# Select faces by normal direction (>Z is front, <Z is back) and get their edges
result = shape_with_hole.faces(">Z or <Z").edges().fillet(face_edge_fillet)