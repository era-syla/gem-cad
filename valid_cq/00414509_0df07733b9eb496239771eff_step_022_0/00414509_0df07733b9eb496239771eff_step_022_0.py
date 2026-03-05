import cadquery as cq

# Parameters for the plate dimensions
plate_length = 200.0
plate_width = 150.0
plate_thickness = 5.0

# Parameters for the holes
hole_diameter = 6.0
hole_margin = 20.0  # Distance from the edge to the center of the hole

# Calculate spacing between hole centers based on margins
hole_spacing_x = plate_length - (2 * hole_margin)
hole_spacing_y = plate_width - (2 * hole_margin)

# Create the CAD model
result = (
    cq.Workplane("XY")
    # Create the base rectangular plate centered at origin
    .box(plate_length, plate_width, plate_thickness)
    # Select the top face to place holes
    .faces(">Z")
    .workplane()
    # Create a rectangle for construction (not solid) to define hole locations at vertices
    .rect(hole_spacing_x, hole_spacing_y, forConstruction=True)
    # Select the vertices of that construction rectangle
    .vertices()
    # Cut holes through the plate at selected vertices
    .hole(hole_diameter)
)