import cadquery as cq

# -- Dimensions and Parameters --
plate_length = 200.0
plate_width = 100.0
plate_thickness = 5.0
corner_radius = 20.0

hole_diameter = 3.0
num_cols = 11  # Number of holes along the length
num_rows = 5   # Number of holes along the width

# Margin from the plate edge to the center of the outer holes
margin_x = 15.0
margin_y = 15.0

# -- Calculations --
# Calculate spacing (pitch) between hole centers based on plate size and margins
x_spacing = (plate_length - (2 * margin_x)) / (num_cols - 1)
y_spacing = (plate_width - (2 * margin_y)) / (num_rows - 1)

# -- Geometry Generation --
result = (
    cq.Workplane("XY")
    # Create the main rectangular body
    .box(plate_length, plate_width, plate_thickness)
    
    # Fillet the four vertical edges to create rounded corners
    .edges("|Z")
    .fillet(corner_radius)
    
    # Select the top face to start the hole pattern
    .faces(">Z")
    .workplane()
    
    # Create a rectangular array of points for the grid
    .rarray(x_spacing, y_spacing, num_cols, num_rows)
    
    # Cut holes through the plate at the array points
    .hole(hole_diameter)
)