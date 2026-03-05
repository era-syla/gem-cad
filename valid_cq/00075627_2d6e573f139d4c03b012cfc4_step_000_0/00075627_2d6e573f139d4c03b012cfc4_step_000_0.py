import cadquery as cq

# -- Parametric Dimensions --
# Tall Plate Dimensions
tall_height = 200.0
tall_width = 35.0
tall_thickness = 4.0

# Short Plate Dimensions
short_height = 60.0
short_width = 40.0
short_thickness = 4.0
short_elevation = 20.0  # Height from ground to bottom of short plate

# Layout Dimensions
gap_width = 15.0       # Horizontal distance between the two plates

# Detail Dimensions (Louvers)
frame_margin = 5.0     # Width of the solid frame around louvers
num_louvers = 10       # Number of slots
louver_spacing = 1.5   # Solid material between slots

# Connector Dimensions
conn_height = 5.0
conn_depth = 4.0       # Thickness of the connecting bar

# -- Geometry Generation --

# 1. Create the Tall Plate
# Positioned on the right side.
# Centered on Y (thickness), Z=0 is the base.
tall_plate_x = (gap_width / 2.0) + (tall_width / 2.0)
tall_plate = (
    cq.Workplane("XY")
    .box(tall_width, tall_thickness, tall_height, centered=(True, True, False))
    .translate((tall_plate_x, 0, 0))
)

# 2. Create the Short Plate (Louvered)
# Positioned on the left side.
short_plate_x = -((gap_width / 2.0) + (short_width / 2.0))

# Create the base solid for the short plate
short_base = (
    cq.Workplane("XY")
    .box(short_width, short_thickness, short_height, centered=(True, True, False))
)

# Calculate Louver Geometry
cut_width = short_width - (2 * frame_margin)
cut_area_height = short_height - (2 * frame_margin)
# Calculate the height of a single slot
slot_height = (cut_area_height - (num_louvers - 1) * louver_spacing) / num_louvers

# Generate center points for the slots relative to the face center
slot_centers = []
start_y = (cut_area_height / 2.0) - (slot_height / 2.0)
for i in range(num_louvers):
    y_pos = start_y - i * (slot_height + louver_spacing)
    slot_centers.append((0, y_pos))

# Apply the cuts to the front face
short_plate_slotted = (
    short_base
    .faces(">Y")
    .workplane()
    .pushPoints(slot_centers)
    .rect(cut_width, slot_height)
    .cutThruAll()
)

# Move the short plate to its final position
short_plate = short_plate_slotted.translate((short_plate_x, 0, short_elevation))

# 3. Create the Connector
# A horizontal bar connecting the two plates near the bottom of the short plate.
# Spans the gap between them.
connector = (
    cq.Workplane("XY")
    .box(gap_width, conn_depth, conn_height, centered=(True, True, False))
    .translate((0, 0, short_elevation + 5.0)) # Positioned slightly above the bottom edge
)

# 4. Combine all parts into the final result
result = tall_plate.union(short_plate).union(connector)