import cadquery as cq

# --- Parametric Dimensions ---
length = 60.0        # Total length of the main body
width = 15.0         # Width of the main body
thickness = 10.0     # Height/thickness of the main body
fillet_radius = 2.0  # Radius for the corners (vertical edges)

hole_diameter = 5.0  # Diameter of the mounting holes
hole_spacing = 45.0  # Center-to-center distance between holes

rib_width = 2.0      # Width of each rib on top
rib_height = 2.0     # Height of the ribs above the top surface
rib_length = 15.0    # Length of the ribs (along the width direction)
rib_count = 3        # Number of ribs
rib_gap = 2.0        # Gap between ribs

# --- Modeling Strategy ---
# 1. Create the main rectangular block.
# 2. Fillet the vertical edges to create the rounded ends.
# 3. Create the two mounting holes.
# 4. Create the ribbed pattern on top.

# --- 1. Main Body ---
# Start with a centered rectangle extrude
body = (
    cq.Workplane("XY")
    .box(length, width, thickness)
)

# --- 2. Fillet Edges ---
# Select vertical edges
body = body.edges("|Z").fillet(fillet_radius)

# --- 3. Mounting Holes ---
# Create points for holes and cut them
body = (
    body.faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing / 2, 0), (hole_spacing / 2, 0)])
    .hole(hole_diameter)
)

# --- 4. Ribs on Top ---
# Calculate the total width of the rib array to center it
total_rib_array_width = (rib_count * rib_width) + ((rib_count - 1) * rib_gap)
start_y = -total_rib_array_width / 2 + (rib_width / 2)

# Create the ribs
# We will create a sketch for the ribs and extrude them
ribs = (
    body.faces(">Z")
    .workplane()
    .rarray(1, rib_width + rib_gap, 1, rib_count) # 1 column, repeated along Y
    .rect(rib_length, rib_width)
    .extrude(rib_height)
)

# Combine body and ribs (CadQuery's extrude on a face usually joins automatically,
# but 'result' holds the current state)
result = ribs

# Export logic (optional, for verification)
# cq.exporters.export(result, "model.step")