import cadquery as cq

# --- Parameter Definitions ---
# Plate dimensions
plate_width = 40.0
plate_length = 40.0
plate_thickness = 5.0
plate_fillet_radius = 2.0

# Rod dimensions
rod_diameter = 4.0
rod_length = 200.0  # Much longer than the plate

# Position
# The rod passes through the middle of the plate's thickness or is attached to the bottom.
# Based on the view, it looks like it goes through the center of the side faces.
rod_offset_z = 0.0 # Centered vertically

# --- Geometry Construction ---

# 1. Create the central square plate
plate = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .edges("|Z")  # Select vertical edges
    .fillet(plate_fillet_radius)
)

# 2. Create the long rod
# The rod runs perpendicular to the "front" face, let's assume along the Y-axis or X-axis.
# In the image, the plate is roughly aligned with the ground plane, and the rod sticks out sideways.
# Let's align the rod along the Y-axis.
rod = (
    cq.Workplane("XZ")
    .circle(rod_diameter / 2.0)
    .extrude(rod_length)
    .translate((0, -rod_length / 2.0, 0)) # Center the rod along Y
)

# 3. Combine the parts
# In CadQuery, a boolean union is often implied or explicitly done.
# The image shows them as a single assembly.
# Let's union them.
result = plate.union(rod)

# Alternatively, if the rod is meant to be a hole, we would subtract.
# But the image clearly shows a solid rod extending outwards.

# If there is a detail underneath (like a mount), it's hard to see.
# The prompt asks for the model "based on the provided image".
# The most prominent features are the plate and the rod.
# Let's stick to that simple interpretation.

# Refinement: Looking closely, the rod seems to pass through the center of the plate's side faces.
# My current construction centers the plate at (0,0,0) and the rod at (0,0,0).
# This aligns them perfectly.

# If there is a small feature underneath, like a linear bearing block:
# Often these look like a block on a rail.
# If this is a linear rail carriage (block) on a rail (rod):
# The block usually has some detail underneath.
# However, the image is low res. A simple union of a box and cylinder is the most robust interpretation.

# Let's double check the "underneath" part. There is a slight shadow or protrusion on the bottom right side of the plate.
# It might suggest the plate sits *on top* of the rod, rather than the rod going through.
# Or it could be a linear bearing block where the rod goes through a lower section.
# Let's try to model it as a linear bearing block, which is a common mechanical part matching this look.
# A linear bearing block (like an SC8UU) usually has a main body and a base.
# Let's assume a simplified representation: A block with a hole, and the rod passing through.
# But visually, it is a single grey object. A union is appropriate.

# Let's refine the "Plate" to be slightly more block-like if it's a bearing block.
# But the top is very flat and wide. Let's stick to the "plate with rod through it" geometry.
# To make it look exactly like the image, the rod should be centered on the Z-axis of the plate.

# Final check of orientation:
# Image shows isometric view.
# Plate is flat on X-Y plane.
# Rod runs along one axis (let's say X).
# My code currently extrudes the rod along Y (from XZ plane). Let's change rod to X-axis to match typical "lengthwise" orientations,
# though visually in an isometric view X and Y are symmetric.
# Let's aligning the rod along the X-axis for clarity.

plate = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .edges("|Z")
    .fillet(plate_fillet_radius)
)

rod = (
    cq.Workplane("YZ")
    .circle(rod_diameter / 2.0)
    .extrude(rod_length)
    .translate((-rod_length / 2.0, 0, 0))
)

result = plate.union(rod)