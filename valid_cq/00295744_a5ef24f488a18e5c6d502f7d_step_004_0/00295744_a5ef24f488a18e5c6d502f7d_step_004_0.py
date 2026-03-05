import cadquery as cq

# Parametric dimensions for the plate
width = 80.0    # X-axis dimension
height = 100.0  # Z-axis dimension
thickness = 5.0 # Y-axis dimension

# Create the solid rectangular plate
# Using box creates a centered rectangular prism
result = cq.Workplane("XY").box(width, thickness, height)