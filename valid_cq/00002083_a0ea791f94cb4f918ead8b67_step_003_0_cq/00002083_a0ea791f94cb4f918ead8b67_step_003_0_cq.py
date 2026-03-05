import cadquery as cq

# Parametric dimensions
height = 100.0  # Height of the plate
width = 100.0   # Width of the plate
thickness = 10.0 # Thickness of the plate

# Create the rectangular plate
# We center it on the X and Y axes for convenience, but Z starts at 0
result = cq.Workplane("XY").box(width, thickness, height)

# Alternatively, if you wanted it to look exactly like the "standing up" orientation:
# result = cq.Workplane("XY").box(width, height, thickness)
# But standard box creates centered geometry. Let's make it more explicit.

# Create a box centered on X and Y, with Z starting from 0 (if extruded) or centered.
# The `box` method creates a box centered at the origin by default.
result = cq.Workplane("XY").box(width, thickness, height)