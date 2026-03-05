import cadquery as cq

# Parametric dimensions for the square column
width = 10.0   # Width of the square cross-section
depth = 10.0   # Depth of the square cross-section
height = 100.0 # Height of the column

# Create the solid rectangular prism
result = cq.Workplane("XY").box(width, depth, height)

# Alternatively, using extrusion:
# result = cq.Workplane("XY").rect(width, depth).extrude(height)