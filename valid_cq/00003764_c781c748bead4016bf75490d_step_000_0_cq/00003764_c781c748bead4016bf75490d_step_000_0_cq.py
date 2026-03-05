import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions of the square plate
plate_width = 100.0  # Total width of the square
plate_thickness = 3.0  # Thickness of the main plate
corner_radius = 5.0  # Fillet radius for the four corners

# Grille / Slots details
rim_width = 8.0  # Width of the outer frame
bar_width = 6.0  # Width of the internal horizontal bars
num_slots = 6  # Number of slots (implies number of bars)

# Central feature
center_disk_diameter = 25.0
center_disk_thickness = 5.0  # Total thickness including the base plate thickness

# Small connecting tabs/notches on the rim
tab_width = 4.0
tab_depth = 1.0  # How deep the tab cuts into the rim
tab_length = 3.0

# --- Geometry Construction ---

# 1. Base Plate (Outer Frame)
# Start with a simple rectangle
base = cq.Workplane("XY").box(plate_width, plate_width, plate_thickness)

# Apply fillets to the corners
base = base.edges("|Z").fillet(corner_radius)

# 2. Create the slots (Grille pattern)
# Calculate slot dimensions based on parameters to ensure symmetry
inner_area_width = plate_width - (2 * rim_width)
total_bar_width = (num_slots - 1) * bar_width
total_slot_width = inner_area_width - total_bar_width
slot_width = total_slot_width / num_slots
slot_length = inner_area_width

# Create a single slot profile to cut
slot_sketch = (
    cq.Sketch()
    .rect(slot_length, slot_width)
)

# Distribute the slots along the Y axis
# Calculate positions
y_positions = []
start_y = -inner_area_width / 2 + slot_width / 2
for i in range(num_slots):
    y_positions.append(start_y + i * (slot_width + bar_width))

# Cut the slots
grille = base.faces(">Z").workplane().pushPoints([(0, y) for y in y_positions]).rect(slot_length, slot_width).cutThruAll()

# 3. Add the Central Disk
# This sits on top of the bars in the center
center_disk = (
    cq.Workplane("XY")
    .workplane(offset=0) # Start from bottom to merge cleanly, or offset slightly
    .circle(center_disk_diameter / 2)
    .extrude(center_disk_thickness)
)

# Combine grille and center disk
result = grille.union(center_disk)

# 4. Add the small tabs/notches on the rim
# These look like small rectangular cutouts on the top face of the rim
# There are 2 per side
offset_dist = plate_width / 2 - rim_width / 2 
spacing = plate_width / 3  # Approximate spacing between tabs on a side

# Define notch locations relative to center
# Top and Bottom edges (varying X, fixed Y)
top_bottom_points = [
    (-spacing/2, plate_width/2 - tab_depth/2),
    (spacing/2, plate_width/2 - tab_depth/2),
    (-spacing/2, -(plate_width/2 - tab_depth/2)),
    (spacing/2, -(plate_width/2 - tab_depth/2)),
]

# Left and Right edges (varying Y, fixed X)
left_right_points = [
    (plate_width/2 - tab_depth/2, -spacing/2),
    (plate_width/2 - tab_depth/2, spacing/2),
    (-(plate_width/2 - tab_depth/2), -spacing/2),
    (-(plate_width/2 - tab_depth/2), spacing/2),
]

# Create Cutouts
# Vertical notches (on top/bottom edges) - long dimension is parallel to edge
result = (
    result.faces(">Z").workplane()
    .pushPoints(top_bottom_points)
    .rect(tab_width, tab_depth)
    .cutBlind(-plate_thickness/2) # Cut halfway through
)

# Horizontal notches (on left/right edges) - long dimension is parallel to edge
result = (
    result.faces(">Z").workplane()
    .pushPoints(left_right_points)
    .rect(tab_depth, tab_width)
    .cutBlind(-plate_thickness/2)
)

# Apply a very small chamfer to top edges for visual polish (optional but looks good)
result = result.edges(">Z").chamfer(0.2)