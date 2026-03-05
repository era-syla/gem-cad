import cadquery as cq

# Define parametric dimensions for the rectangular bar
length = 300.0  # Length of the bar
width = 15.0    # Width of the cross-section
thickness = 8.0 # Thickness of the cross-section

# Create the rectangular bar geometry
# The box method creates a rectangular prism centered at the origin by default
result = cq.Workplane("XY").box(length, width, thickness)