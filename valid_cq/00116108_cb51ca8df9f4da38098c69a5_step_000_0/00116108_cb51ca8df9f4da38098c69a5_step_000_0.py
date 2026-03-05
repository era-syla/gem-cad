import cadquery as cq

# Parameters for dimensions
disk_diameter = 100.0
disk_thickness = 8.0

center_hole_dia = 20.0

# Large offset hole
large_hole_dia = 32.0
large_hole_offset = -31.0  # Offset along X axis

# Small offset hole
small_hole_dia = 6.0
small_hole_offset = 35.0   # Offset along X axis

# Create the main disk body
result = (
    cq.Workplane("XY")
    .circle(disk_diameter / 2.0)
    .extrude(disk_thickness)
)

# Cut the holes
result = (
    result.faces(">Z")
    .workplane()
    # Center hole
    .hole(center_hole_dia)
    # Large hole to the left
    .pushPoints([(large_hole_offset, 0)])
    .hole(large_hole_dia)
    # Small hole to the right
    .pushPoints([(small_hole_offset, 0)])
    .hole(small_hole_dia)
)