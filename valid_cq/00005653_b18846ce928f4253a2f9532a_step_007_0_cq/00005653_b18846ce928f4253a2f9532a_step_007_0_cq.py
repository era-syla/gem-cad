import cadquery as cq

# Parametric dimensions for the rectangular bar
length = 200.0  # Length of the bar
width = 10.0    # Width of the bar
thickness = 2.0 # Thickness of the bar

# Create the rectangular bar using a simple box operation
# Centered on the XY plane for convenience
result = cq.Workplane("XY").box(length, width, thickness)

# Alternatively, using sketch and extrude for more explicit control:
# result = (cq.Workplane("XY")
#           .rect(length, width)
#           .extrude(thickness))