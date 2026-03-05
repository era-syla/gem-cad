import cadquery as cq

# Define parameters for the rectangular strip
length = 150.0  # Length of the strip
width = 10.0    # Width of the strip
thickness = 1.0 # Thickness of the strip

# Create the solid geometry
# We use the box operation on the XY plane. 
# By default, box centers the geometry at the origin.
result = cq.Workplane("XY").box(length, width, thickness)