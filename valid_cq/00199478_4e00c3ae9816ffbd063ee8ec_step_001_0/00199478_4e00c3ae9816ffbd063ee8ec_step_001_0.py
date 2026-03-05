import cadquery as cq

# Define parametric dimensions based on the visual proportions of the image
length = 200.0    # Total length of the bar
height = 12.0     # Vertical height of the cross-section
thickness = 3.0   # Thickness/width of the cross-section

# Create the 3D model: a long rectangular prism (bar)
# We align the length along the X-axis
result = cq.Workplane("XY").box(length, thickness, height)