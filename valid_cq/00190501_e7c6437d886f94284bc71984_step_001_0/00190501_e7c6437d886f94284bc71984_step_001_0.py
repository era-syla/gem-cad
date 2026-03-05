import cadquery as cq

# Dimensions based on the visual proportions of the image
length = 100.0      # Total length of the plate
width = 70.0        # Total width of the plate
thickness = 3.0     # Thickness of the plate
slot_depth = 25.0   # How deep the slots go into the plate
slot_width = 2.0    # Width of the slot cuts

# Generate the base rectangular plate
# Centered at the origin for simpler symmetry operations
result = cq.Workplane("XY").box(length, width, thickness)

# Calculate slot positions
# The image shows two slots that divide the length into three roughly equal segments.
# This implies a pitch of length/3.
# Positions relative to the center (X=0) would be -length/6 and +length/6.
x_offset = length / 6.0
slot_positions = [(-x_offset), (x_offset)]

# Calculate cut rectangle parameters
# To ensure the slot is open at the edge, the cut shape should extend slightly 
# beyond the plate's edge. We define a small extension buffer.
extension = 5.0
cut_length = slot_depth + extension

# We assume the slots are cut into the +Y edge (at y = width/2).
# The cut rectangle ranges from y = (width/2 - slot_depth) to y = (width/2 + extension).
# We need to find the center Y coordinate for the rectangle command.
cut_center_y = (width / 2.0) - (slot_depth / 2.0) + (extension / 2.0)

# Create the points for the cut operations
cut_points = [(x, cut_center_y) for x in slot_positions]

# Perform the cuts
result = (
    result
    .faces(">Z")  # Select the top face
    .workplane()
    .pushPoints(cut_points)
    .rect(slot_width, cut_length)
    .cutThruAll() # Cut through the entire thickness
)