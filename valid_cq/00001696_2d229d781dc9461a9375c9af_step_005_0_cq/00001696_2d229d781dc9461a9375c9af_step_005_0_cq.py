import cadquery as cq

# Parametric dimensions for the flat rectangular bar
length = 100.0  # Total length of the bar
width = 10.0    # Width of the bar
thickness = 1.0 # Thickness of the bar

# Create the box geometry
# centered=(True, True, True) ensures the object is centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)

# Alternatively, if centering is not desired on Z:
# result = cq.Workplane("XY").box(length, width, thickness, centered=(True, True, False))