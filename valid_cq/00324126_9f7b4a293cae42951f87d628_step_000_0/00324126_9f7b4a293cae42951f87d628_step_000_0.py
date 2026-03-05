import cadquery as cq

# --- Parametric Dimensions ---
table_length = 160.0
table_width = 70.0
table_height = 90.0
top_thickness = 4.0
leg_size = 4.0   # Square cross-section side length
leg_inset = 2.0  # Offset from the table edge

# --- Modeling ---

# 1. Create the table top
# Create a box centered on the XY plane. 
# The thickness is centered on Z=0, so the bottom face is at Z = -top_thickness/2
table_top = cq.Workplane("XY").box(table_length, table_width, top_thickness)

# 2. Create the legs
# Calculate the center coordinates for the legs based on dimensions and inset
x_pos = (table_length / 2) - leg_inset - (leg_size / 2)
y_pos = (table_width / 2) - leg_inset - (leg_size / 2)

leg_locations = [
    (x_pos, y_pos),
    (x_pos, -y_pos),
    (-x_pos, y_pos),
    (-x_pos, -y_pos)
]

# Calculate the length of the legs
leg_length = table_height - top_thickness

# Select the bottom face of the table top, sketch the legs, and extrude
result = (
    table_top
    .faces("<Z")                # Select the bottom face (lowest Z face)
    .workplane()                # Create a new workplane on the selected face
    .pushPoints(leg_locations)  # Move to the four leg positions
    .rect(leg_size, leg_size)   # Sketch the leg profiles
    .extrude(leg_length)        # Extrude downwards to create the legs
)