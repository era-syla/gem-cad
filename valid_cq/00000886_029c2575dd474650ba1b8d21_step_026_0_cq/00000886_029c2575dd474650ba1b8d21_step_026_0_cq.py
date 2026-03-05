import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions
total_height = 100.0  # Total height of the vertical plate
total_width = 40.0    # Width of the base plate
base_length = 50.0    # Length of the horizontal base plate protruding from the vertical
thickness = 5.0       # Thickness of the vertical and horizontal plates
gusset_thickness = 5.0 # Thickness of the triangular rib

# Hole dimensions
hole_diameter = 8.0
hole_center_offset = 15.0 # Distance from the front edge of the base

# --- Geometry Construction ---

# 1. Vertical Plate (The "Back")
# Create a box centered on XY, then move it so its back face is on XZ plane
vertical_plate = cq.Workplane("XY").box(thickness, total_height, total_width) \
    .translate((-thickness/2, total_height/2, 0))

# 2. Horizontal Base Plate (The "Foot")
# Create a box, position it at the bottom
horizontal_plate = cq.Workplane("XY").box(base_length, thickness, total_width) \
    .translate((base_length/2, thickness/2, 0))

# 3. Triangular Gusset (The "Rib")
# We'll sketch this on the XZ plane (side view) and extrude it symmetrically.
# Points for the triangle:
# P1: Top corner where gusset meets vertical plate (slightly below top edge typically, or flush)
# P2: Bottom corner where gusset meets vertical plate
# P3: Front corner where gusset meets horizontal plate
pts = [
    (0, thickness),                               # Bottom-left (at junction)
    (base_length, thickness),                     # Bottom-right (on base)
    (0, total_height)                             # Top-left (on vertical)
]

gusset = cq.Workplane("XY") \
    .transformed(rotate=(90, 0, 0)) \
    .polyline(pts).close() \
    .extrude(gusset_thickness/2.0, both=True) # Extrude symmetrically to center it

# --- Combine Parts ---
# Union vertical and horizontal plates first
structure = vertical_plate.union(horizontal_plate)

# Union the gusset
result = structure.union(gusset)

# --- Add Hole ---
# Add the hole to the horizontal base plate
# The hole is centered on width (Y=0) and offset from the front edge (X direction)
hole_x_pos = base_length - hole_center_offset

result = result.faces("<Z").workplane().moveTo(hole_x_pos, 0).hole(hole_diameter)

# Use the standard variable name for the final object
# result is already set above