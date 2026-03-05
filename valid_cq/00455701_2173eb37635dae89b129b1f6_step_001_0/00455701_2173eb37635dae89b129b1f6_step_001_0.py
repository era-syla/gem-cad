import cadquery as cq

# -- Parametric Dimensions --
length = 180.0       # Total length of the plate
width = 60.0         # Total width of the plate
thickness = 10.0     # Thickness of the plate
seam_gap = 0.5       # Width of the central longitudinal cut
slot_length = 16.0   # Length of the oblong slots
slot_width = 4.0     # Width (diameter) of the slots
num_slots = 5        # Number of slots per row
end_margin = 25.0    # Distance from center of first/last slot to the part ends

# -- Modeling Logic --

# 1. Create the main base block
# Centered on the origin
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Cut the central seam
# We make the rectangle slightly longer than the part to ensure clean cuts on the end faces
result = (
    result.faces(">Z")
    .workplane()
    .rect(length + 5.0, seam_gap)
    .cutThruAll()
)

# 3. Create the slot pattern
# Calculate X positions for the slots based on margins and count
available_span = length - (2 * end_margin)
step_x = available_span / (num_slots - 1)
x_positions = [-available_span/2 + i * step_x for i in range(num_slots)]

# Y positions assume the slots are centered on each half of the split plate
y_offset = width / 4.0

# Collect all center points for the slots
slot_points = []
for x in x_positions:
    slot_points.append((x, y_offset))   # Top row
    slot_points.append((x, -y_offset))  # Bottom row

# 4. Cut the slots
# We use slot2D. The 'length' parameter is the total outer length.
# angle=90 aligns the slot length with the Y axis (transverse to the plate).
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(slot_points)
    .slot2D(length=slot_length, diameter=slot_width, angle=90)
    .cutThruAll()
)