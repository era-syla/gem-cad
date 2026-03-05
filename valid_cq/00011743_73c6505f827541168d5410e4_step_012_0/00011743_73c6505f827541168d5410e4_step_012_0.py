import cadquery as cq

# Parameters for the plate dimensions and features
num_cols = 5
num_rows = 2
spacing = 20.0       # Distance between hole centers (pitch)
margin = 10.0        # Distance from hole center to the edge of the plate
thickness = 5.0      # Plate thickness
hole_diameter = 8.0  # Diameter of the through holes
corner_radius = 6.0  # Radius of the plate corners

# Calculate total width and height based on parameters
# Width is along the X-axis (long side), Height is along the Y-axis (short side)
total_length = (num_cols - 1) * spacing + 2 * margin
total_width = (num_rows - 1) * spacing + 2 * margin

# Generate the geometry
result = (
    cq.Workplane("XY")
    # 1. Create the base rectangular plate
    .box(total_length, total_width, thickness)
    
    # 2. Round the vertical corners
    .edges("|Z")
    .fillet(corner_radius)
    
    # 3. Select the top face to start drilling holes
    .faces(">Z")
    .workplane()
    
    # 4. Create a rectangular array of points for the holes
    #    rarray(xSpacing, ySpacing, xCount, yCount, center=True)
    .rarray(spacing, spacing, num_cols, num_rows)
    
    # 5. Cut the holes through the plate
    .hole(hole_diameter)
)