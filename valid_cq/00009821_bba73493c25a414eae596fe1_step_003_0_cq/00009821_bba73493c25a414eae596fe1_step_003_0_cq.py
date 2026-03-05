import cadquery as cq

# Parametric dimensions
length = 200.0       # Total length of the plate
width = 40.0         # Total width of the plate
thickness = 2.0      # Thickness of the plate

num_slots_per_row = 13  # Number of slots in one row
slot_length = 6.0       # Length of each rectangular slot along the plate's long axis
slot_width = 3.0        # Width of each rectangular slot
row_spacing = 20.0      # Distance between the centerlines of the two rows

# Calculated dimensions for spacing
# Calculate the spacing between slot centers along the length
# The slots span most of the length. Let's assume some margin.
margin_x = 10.0 # Distance from edge to first slot center
# Calculate pitch based on margins
slot_pitch_x = (length - 2 * margin_x) / (num_slots_per_row - 1)

# Create the base plate
base_plate = cq.Workplane("XY").box(length, width, thickness)

# Create the positions for the slots
# We need two rows.
# Row 1 y-coordinate: -row_spacing / 2
# Row 2 y-coordinate: +row_spacing / 2
# X-coordinates range from -length/2 + margin to +length/2 - margin

slots = (
    base_plate.faces(">Z")
    .workplane()
    .rarray(
        xSpacing=slot_pitch_x, 
        ySpacing=row_spacing, 
        xCount=num_slots_per_row, 
        yCount=2, 
        center=True
    )
    .rect(slot_length, slot_width)
    .cutThruAll()
)

result = slots