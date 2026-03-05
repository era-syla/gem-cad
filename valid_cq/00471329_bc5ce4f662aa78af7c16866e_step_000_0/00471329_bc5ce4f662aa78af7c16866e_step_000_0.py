import cadquery as cq

# Parameters for the geometry
height = 200.0   # Total length/height of the bar
width = 3.0      # Width of the cross-section
thickness = 3.0  # Thickness of the cross-section

# Create the 3D model
# A long, thin vertical rectangular prism (bar/rod) centered at the origin
result = cq.Workplane("XY").box(width, thickness, height)