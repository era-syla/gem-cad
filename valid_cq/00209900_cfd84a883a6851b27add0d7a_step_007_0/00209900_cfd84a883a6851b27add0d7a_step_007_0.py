import cadquery as cq

# Geometric parameters
plate_width = 100.0     # Width of the plate (X-axis)
plate_height = 75.0     # Height of the plate (Z-axis)
plate_thickness = 2.0   # Thickness of the plate (Y-axis)

# Create the rectangular plate geometry
# Using box primitive centered at the origin
# Oriented vertically to match the isometric view in the image
result = cq.Workplane("XY").box(plate_width, plate_thickness, plate_height)