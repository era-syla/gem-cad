import cadquery as cq

# Parametric dimensions
disk_diameter = 100.0
disk_thickness = 4.0
center_hole_diameter = 2.0

# Create the disk with a center hole
# We draw two concentric circles and extrude them.
# CadQuery automatically detects the inner circle as a hole.
result = (
    cq.Workplane("XY")
    .circle(disk_diameter / 2.0)
    .circle(center_hole_diameter / 2.0)
    .extrude(disk_thickness)
)