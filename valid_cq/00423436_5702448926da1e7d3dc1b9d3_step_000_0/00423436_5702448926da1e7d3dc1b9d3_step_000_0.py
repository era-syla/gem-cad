import cadquery as cq

# Parametric dimensions
shaft_length = 100.0
shaft_diameter = 25.0
end_hole_diameter = 6.0
end_hole_offset = 12.0  # Distance from the end face to the hole center
center_hole_diameter = 3.0
chamfer_size = 1.0

# 1. Create the main cylindrical shaft
# Oriented along the X-axis, centered at the origin
result = (
    cq.Workplane("YZ")
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length, both=True)
)

# 2. Cut the through-holes at the ends
# These holes are perpendicular to the shaft axis (along Y-axis)
# We sketch on the XZ plane and cut along Y
x_pos = shaft_length / 2.0 - end_hole_offset

# Create a cutter for the end holes
end_holes_cutter = (
    cq.Workplane("XZ")
    .pushPoints([(-x_pos, 0), (x_pos, 0)])
    .circle(end_hole_diameter / 2.0)
    .extrude(shaft_diameter * 1.5, both=True)  # Extrude sufficient length to cut through
)

# Apply the cut
result = result.cut(end_holes_cutter)

# 3. Cut the center hole
# This hole is perpendicular to the shaft and the end holes (along Z-axis)
# We sketch on the XY plane and cut along Z
center_hole_cutter = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .circle(center_hole_diameter / 2.0)
    .extrude(shaft_diameter * 1.5, both=True)
)

# Apply the cut
result = result.cut(center_hole_cutter)

# 4. Add chamfers to the ends of the shaft for engineering detail
result = result.faces("<X or >X").edges().chamfer(chamfer_size)