import cadquery as cq

# --- Parameters ---
length = 300.0         # Length of the extrusion profile
width = 20.0           # Width/Height of the profile (20mm standard)
corner_radius = 1.0    # Fillet radius for external corners
center_hole_dia = 4.2  # Diameter of the central hole (typically for M5)

# T-Slot Dimensions
slot_opening = 6.2     # Width of the slot opening
slot_depth = 6.0       # Depth of the slot from surface
slot_inner_w = 10.5    # Width of the inner cavity
lip_thickness = 1.5    # Thickness of the retaining lip

# --- Geometry Construction ---

# 1. Base Geometry
# Create the main square profile and extrude it
# Using rect().extrude() puts the object in the Z range [0, length]
base = (
    cq.Workplane("XY")
    .rect(width, width)
    .extrude(length)
    .edges("|Z")  # Select vertical edges
    .fillet(corner_radius)
)

# 2. Define the T-Slot Cutter
# We create a 2D profile of the slot void and extrude it to create a cutting tool.
# Coordinates are relative to the center of the profile.

# Calculate Y coordinates for the top slot (centered on Y-axis)
y_surface = width / 2.0
y_lip_bottom = y_surface - lip_thickness
y_slot_bottom = y_surface - slot_depth

# Calculate X coordinates
x_opening = slot_opening / 2.0
x_inner = slot_inner_w / 2.0

# Define points for the T-shape polygon
# Clockwise winding starting from top-right of the opening
slot_points = [
    (x_opening, y_surface),
    (x_opening, y_lip_bottom),
    (x_inner, y_lip_bottom),
    (x_inner, y_slot_bottom),
    (-x_inner, y_slot_bottom),
    (-x_inner, y_lip_bottom),
    (-x_opening, y_lip_bottom),
    (-x_opening, y_surface)
]

# Create the solid cutter for one slot
slot_cutter = (
    cq.Workplane("XY")
    .polyline(slot_points)
    .close()
    .extrude(length)
)

# 3. Create Combined Cutters
# Union the cutter rotated 4 times (0, 90, 180, 270 degrees)
# Note: rotating around the Z-axis (0,0,1)
combined_cutters = slot_cutter
for angle in [90, 180, 270]:
    combined_cutters = combined_cutters.union(
        slot_cutter.rotate((0, 0, 0), (0, 0, 1), angle)
    )

# 4. Final Boolean Operations
# Cut the slots from the base and drill the center hole
result = (
    base
    .cut(combined_cutters)
    .faces(">Z")           # Select the top face
    .workplane()
    .hole(center_hole_dia) # Cut the center hole through all
)