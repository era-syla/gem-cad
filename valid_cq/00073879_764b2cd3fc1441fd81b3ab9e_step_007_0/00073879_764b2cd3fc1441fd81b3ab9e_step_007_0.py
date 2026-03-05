import cadquery as cq

# Parametric dimensions for the model
cyl_radius = 12.0       # Radius of the large cylinder
cyl_height = 20.0       # Height of the large cylinder
tab_radius = 10.0       # Radius of the rounded end of the tab
tab_thickness = 8.0     # Thickness/height of the tab
center_dist = 30.0      # Distance between the center of the cylinder and the center of the tab
hole_dia = 8.0          # Diameter of the holes

# 1. Create the main large cylinder at the origin
main_cylinder = cq.Workplane("XY").circle(cyl_radius).extrude(cyl_height)

# 2. Create the tab structure
# The tab consists of a circular end and a rectangular section connecting to the main cylinder.
# We model the rectangular part to extend from the tab center (-center_dist) to the origin (0).

# Circular end of the tab
tab_end = (
    cq.Workplane("XY")
    .center(-center_dist, 0)
    .circle(tab_radius)
    .extrude(tab_thickness)
)

# Rectangular connecting body
# Width equals distance, Height equals diameter of the tab
# Centered at half the distance to span the gap correctly
tab_rect = (
    cq.Workplane("XY")
    .center(-center_dist / 2, 0)
    .rect(center_dist, tab_radius * 2)
    .extrude(tab_thickness)
)

# Combine the tab parts
tab_solid = tab_end.union(tab_rect)

# Union the tab with the main cylinder
body = main_cylinder.union(tab_solid)

# 3. Cut the holes
# Create cutter cylinders for the holes
# Hole for the main cylinder
hole_main = (
    cq.Workplane("XY")
    .circle(hole_dia / 2)
    .extrude(cyl_height)
)

# Hole for the tab
hole_tab = (
    cq.Workplane("XY")
    .center(-center_dist, 0)
    .circle(hole_dia / 2)
    .extrude(cyl_height)
)

# Subtract the holes from the main body
result = body.cut(hole_main).cut(hole_tab)