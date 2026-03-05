import cadquery as cq

# -- Parametric Dimensions --
length = 100.0       # Total length of the plate (X-axis)
width = 65.0         # Total width of the plate (Y-axis)
thickness = 5.0      # Thickness of the plate (Z-axis)
fillet_radius = 8.0  # Radius for the rounded front corners

# Slot (Notch) Dimensions
slot_width = 5.0     # Width of the slot along the length of the plate
slot_depth = 10.0    # Depth of the cut into the side of the plate
back_margin = 6.0    # Distance from the back edge to the start of the slot

# -- Modeling --

# 1. Create the base rectangular plate
# Oriented on the XY plane, centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Fillet the front corners
# We define the "front" as the +X direction.
# Select edges parallel to Z (|Z) that are at the maximum X boundary (>X).
result = result.edges("|Z and >X").fillet(fillet_radius)

# 3. Create the side slots near the back edge
# Calculate the X-coordinate for the center of the slots
# Back edge is at x = -length/2
slot_center_x = (-length / 2) + back_margin + (slot_width / 2)

# Create a cutter object
# Dimensions:
# - X: slot_width
# - Y: slot_depth * 2 (to ensure the cutter overlaps the edge fully, effectively cutting 'slot_depth' deep)
# - Z: thickness * 2 (to ensure it cuts through the entire thickness)
cutter = cq.Workplane("XY").box(slot_width, slot_depth * 2, thickness * 2)

# Position cutter on the +Y side edge
cutter_top = cutter.translate((slot_center_x, width / 2, 0))

# Position cutter on the -Y side edge
cutter_bottom = cutter.translate((slot_center_x, -width / 2, 0))

# 4. Subtract the cutters from the main body
result = result.cut(cutter_top).cut(cutter_bottom)