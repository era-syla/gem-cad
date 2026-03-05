import cadquery as cq

# Parametric dimensions
width = 10.0    # Cross-section width
depth = 10.0    # Cross-section depth
height = 120.0  # Length of the bar

# Create the rectangular prism geometry
# Start on XY plane, draw a rectangle, and extrude vertically
result = cq.Workplane("XY").rect(width, depth).extrude(height)