import cadquery as cq

# Parametric Dimensions
length = 80.0          # Total length of the plate
width = 40.0           # Total width of the plate
thickness = 10.0       # Total height/thickness of the plate
land_length = 15.0     # Length of the raised sections at both ends
recess_depth = 3.0     # Depth of the transverse channel cut
hole_diameter = 22.0   # Diameter of the central hole
pin_diameter = 6.0     # Diameter of the protruding pin
pin_length = 20.0      # Length of the protruding pin

# Calculated Dimensions
recess_length = length - (2 * land_length)

# 1. Base Geometry
# Create the main rectangular block centered on the XY plane
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Top Recess
# Cut the wide transverse channel on the top surface.
# We select the top face, sketch a rectangle centered on the part (spanning the recess length),
# and cut downwards. The width is exaggerated to ensure it cuts through the side edges cleanly.
result = (
    result.faces(">Z")
    .workplane()
    .rect(recess_length, width + 5.0)
    .cutBlind(-recess_depth)
)

# 3. Central Hole
# Create the through-hole in the center.
# We select the bottom face ("<Z") to establish a workplane, as it remains a single,
# centered planar face, ensuring the hole is perfectly centered relative to the overall geometry.
result = (
    result.faces("<Z")
    .workplane()
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)

# 4. Guide Pin
# Add the cylindrical pin to one of the end faces.
# We select the face with the minimum X coordinate.
result = (
    result.faces("<X")
    .workplane()
    .circle(pin_diameter / 2.0)
    .extrude(pin_length)
)