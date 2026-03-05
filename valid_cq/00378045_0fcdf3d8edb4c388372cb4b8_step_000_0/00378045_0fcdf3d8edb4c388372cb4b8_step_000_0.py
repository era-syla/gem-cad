import cadquery as cq

# Define parametric dimensions based on the visual aspect ratio
length = 100.0   # Horizontal length
height = 60.0    # Vertical height
thickness = 12.0 # Depth/Width

# Create the rectangular prism (box)
# box(length, width, height) creates a box centered at the origin
result = cq.Workplane("XY").box(length, thickness, height)