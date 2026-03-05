import cadquery as cq

# --- Parameters ---
# Main Screw / Rod Dimensions
head_diameter = 18.0
head_length = 24.0
head_hole_diameter = 6.0
rod_diameter = 8.0
rod_length = 150.0

# Small Stud / Pin Dimensions
stud_diameter = 5.0
stud_length = 45.0
stud_position_offset = (-40.0, 0.0, 10.0)  # Position relative to the main part

# --- Modeling Main Screw ---

# 1. Create the cylindrical head base
# Aligned along the Z-axis
main_body = cq.Workplane("XY").circle(head_diameter / 2.0).extrude(head_length)

# 2. Add the long threaded rod shaft
# Extrudes from the top face of the head
main_body = (
    main_body.faces(">Z")
    .workplane()
    .circle(rod_diameter / 2.0)
    .extrude(rod_length)
)

# 3. Cut the cross-hole in the head
# The hole is centered vertically on the head and runs perpendicular to the Z-axis (along Y)
# We define a cutter object on the XZ plane and extrude it along Y to cut through the head
hole_cutter = (
    cq.Workplane("XZ")
    .center(0, head_length / 2.0)  # Center on X=0, Z=Middle of head
    .circle(head_hole_diameter / 2.0)
    .extrude(head_diameter * 2.0, both=True)  # Extrude both ways along Y to ensure full cut
)

# Apply the cut to the main body
main_screw = main_body.cut(hole_cutter)

# --- Modeling Small Stud ---

# Create a simple cylinder for the secondary object
stud = (
    cq.Workplane("XY")
    .circle(stud_diameter / 2.0)
    .extrude(stud_length)
    .translate(stud_position_offset)
)

# --- Final Assembly ---

# Combine both objects into the final result
result = main_screw.union(stud)