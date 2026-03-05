import cadquery as cq

# Parametric dimensions based on visual estimation
plate_length = 300.0
plate_width = 200.0
plate_thickness = 15.0
hole_diameter = 8.0
hole_margin_x = 30.0  # Distance from short edges
hole_margin_y = 30.0  # Distance from long edges

# Define hole positions (3 columns x 2 rows)
# X coordinates for 3 columns (Left, Center, Right)
x_coords = [-plate_length/2 + hole_margin_x, 0, plate_length/2 - hole_margin_x]
# Y coordinates for 2 rows (Top, Bottom)
y_coords = [-plate_width/2 + hole_margin_y, plate_width/2 - hole_margin_y]

# Generate list of (x, y) points
hole_points = [(x, y) for x in x_coords for y in y_coords]

# Create the solid geometry
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .hole(hole_diameter)
)