import cadquery as cq

# Define parametric dimensions for the long rectangular beam
width = 10.0    # Cross-section width (X)
depth = 10.0    # Cross-section depth (Y)
height = 300.0  # Length of the beam (Z)

# Create the rectangular prism (box) centered at the origin
result = cq.Workplane("XY").box(width, depth, height)