import cadquery as cq

# Parameters based on the visual proportions of the image
length = 120.0     # Total length of the strip
width = 15.0       # Width of the strip (and diameter of the rounded ends)
thickness = 3.0    # Thickness of the strip

# Create the 3D model
# 1. Initialize a Workplane on the XY plane
# 2. Create a 2D slot (stadium shape) profile
# 3. Extrude the profile to the specified thickness
result = (
    cq.Workplane("XY")
    .slot2D(length, width)
    .extrude(thickness)
)