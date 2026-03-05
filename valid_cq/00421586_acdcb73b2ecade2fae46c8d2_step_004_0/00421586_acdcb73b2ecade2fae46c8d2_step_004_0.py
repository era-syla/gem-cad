import cadquery as cq

# --- Parameters ---
# Dimensions estimated from the image aspect ratio
plate_length = 160.0
plate_width = 70.0
plate_thickness = 2.0
hole_diameter = 3.2  # Standard M3 clearance

# Text settings
text_size = 10.0
text_depth = 0.5
text_spacing_y = 16.0  # Distance between text centers

# Define offsets for parametric hole placement
end_margin = 6.0
inner_margin = 14.0
side_margin = 6.0

# --- Hole Pattern Calculation ---
# The pattern is asymmetrical: double holes on left corners, single on right corners
hole_positions = [
    # Left End Corners (Double holes)
    (-plate_length/2 + end_margin, -plate_width/2 + side_margin),
    (-plate_length/2 + inner_margin, -plate_width/2 + side_margin),
    (-plate_length/2 + end_margin, plate_width/2 - side_margin),
    (-plate_length/2 + inner_margin, plate_width/2 - side_margin),
    
    # Mid-Left Section
    (-35, -20), 
    (-35, 20),
    
    # Mid-Right Section
    (30, -15), 
    (30, 15),
    
    # Far-Right Inner Section
    (50, -24), 
    (50, 24),
    
    # Right End Corners (Single holes)
    (plate_length/2 - end_margin, -plate_width/2 + side_margin),
    (plate_length/2 - end_margin, plate_width/2 - side_margin),
]

# --- Geometry Construction ---

# 1. Create the base rectangular plate
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Cut the mounting holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

# 3. Engrave "Circuit" text
# Positioned slightly above center
result = (
    result.faces(">Z")
    .workplane()
    .center(0, text_spacing_y / 2)
    .text("Circuit", text_size, -text_depth)
)

# 4. Engrave "Board" text
# Positioned slightly below center
result = (
    result.faces(">Z")
    .workplane()
    .center(0, -text_spacing_y / 2)
    .text("Board", text_size, -text_depth)
)