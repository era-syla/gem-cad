import cadquery as cq

# --- Parameters ---
# Dimensions based on standard LEGO brick specifications (in mm)
pitch = 8.0               # Distance between stud centers
stud_diameter = 4.8       # Diameter of the studs
stud_height = 1.7         # Height of the studs
brick_height = 9.6        # Height of the main brick body
num_studs_length = 4      # Number of studs along the length
num_studs_width = 1       # Number of studs along the width

# Calculate total dimensions
total_length = num_studs_length * pitch
total_width = num_studs_width * pitch

# --- Geometry Generation ---

# 1. Create the main rectangular block
# We center the box at the origin to simplify symmetric stud placement
base = cq.Workplane("XY").box(total_length, total_width, brick_height)

# 2. Create the studs on the top surface
result = (
    base
    .faces(">Z")                         # Select the top face
    .workplane()                         # Create a workplane on that face
    .rarray(                             # Create a rectangular array of points
        xSpacing=pitch, 
        ySpacing=pitch, 
        xCount=num_studs_length, 
        yCount=num_studs_width, 
        center=True                      # Center the array about the origin
    )
    .circle(stud_diameter / 2.0)         # Draw the stud circles
    .extrude(stud_height)                # Extrude them upwards
)