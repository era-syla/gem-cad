import cadquery as cq

# Parametric dimensions
plate_height = 100.0
plate_width = 80.0
thickness = 5.0

# Chamfer/Corner details
chamfer_start_y = 60.0  # Height where the angled cut begins on the left
chamfer_end_x = 30.0    # Distance from left edge where the top flat part begins

# Hole parameters
large_hole_diameter = 12.0
small_hole_diameter = 3.0
hole_center_x = 15.0    # Distance from left edge
hole_center_y = 50.0    # Distance from bottom
small_hole_offset = 10.0 # Distance from center of large hole to centers of small holes

# Create the base shape
# We will draw the profile on the XY plane and extrude it
# The shape is defined by points: (0,0) -> (width, 0) -> (width, height) -> (chamfer_end_x, height) -> (0, chamfer_start_y) -> close
result = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (plate_width, 0),
        (plate_width, plate_height),
        (chamfer_end_x, plate_height),
        (0, chamfer_start_y),
        (0, 0)
    ])
    .close()
    .extrude(thickness)
)

# Add the holes
# We locate the workplane on the front face
result = (
    result.faces(">Z")
    .workplane()
    # Create the large center hole
    .pushPoints([(hole_center_x, hole_center_y)])
    .hole(large_hole_diameter)
    # Create the two smaller mounting holes
    .pushPoints([
        (hole_center_x - small_hole_offset/2, hole_center_y), # Left small hole
        (hole_center_x + small_hole_offset/2, hole_center_y)  # Right small hole
    ])
    .hole(small_hole_diameter)
)