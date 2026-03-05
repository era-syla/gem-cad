import cadquery as cq

# Define parametric dimensions
length = 100.0  # Length of the plate
width = 30.0    # Width of the plate
thickness = 5.0 # Thickness of the plate

# Create the rectangular prism (box)
# centered=True centers the box at the origin (0,0,0)
result = cq.Workplane("XY").box(length, width, thickness)

# Alternatively, if you want it sitting on the XY plane instead of centered on Z:
# result = cq.Workplane("XY").box(length, width, thickness, centered=(True, True, False))