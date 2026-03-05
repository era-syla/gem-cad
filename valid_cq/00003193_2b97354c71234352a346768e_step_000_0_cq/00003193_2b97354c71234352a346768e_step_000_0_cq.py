import cadquery as cq

# Parametric dimensions
length = 100.0  # Length of the plate
height = 50.0   # Height of the plate
thickness = 2.0 # Thickness of the plate (making it thin like a sheet)

# Create the simple rectangular plate
# We center it on X and Y, but keep Z starting from 0 (or centered, choice is arbitrary but centered is usually cleaner)
result = cq.Workplane("XY").box(length, thickness, height)

# Alternatively, if the orientation in the image is strictly side-on:
# result = cq.Workplane("XY").box(length, height, thickness)
# But looking at the perspective, it looks like a vertical wall.
# Let's stick with the first interpretation which creates a standing wall.