import cadquery as cq

# Define parametric dimensions based on the visual aspect ratio
# The object appears to be a thin rectangular plate standing vertically
plate_width = 60.0    # X dimension
plate_height = 100.0  # Z dimension
plate_thickness = 2.0 # Y dimension

# Create the 3D solid geometry
# We create a box centered at the origin.
# The dimensions are mapped to create a vertical plate orientation.
result = cq.Workplane("XY").box(plate_width, plate_thickness, plate_height)