import cadquery as cq

# Parametric dimensions
length = 100.0   # Total length of the part
height = 60.0    # Total height of the part
thickness = 15.0 # Thickness of the extrusion
corner_radius = 20.0 # Radius for the rounded corners at the bottom
hole_diameter = 4.0  # Diameter of the top hole

# Create the base sketch
# We will draw a rectangle and then fillet the bottom two corners
# to achieve the shape shown in the image.
result = (
    cq.Workplane("XY")
    .box(length, height, thickness)
    .edges("|Z")  # Select vertical edges
    .edges("<Y")  # Filter for the bottom edges
    .fillet(corner_radius) # Create the rounded bottom corners
    .faces(">Y")  # Select the top face
    .workplane()
    .center(0, 0) # Ensure we are at the center of the top face
    .hole(hole_diameter) # Create the hole in the top
)

# Alternatively, if drawing the profile explicitly is preferred for clarity:
# result = (
#     cq.Workplane("XY")
#     .moveTo(-length/2, height)
#     .lineTo(length/2, height)
#     .lineTo(length/2, corner_radius)
#     .radiusArc((length/2 - corner_radius, 0), -corner_radius)
#     .lineTo(-length/2 + corner_radius, 0)
#     .radiusArc((-length/2, corner_radius), -corner_radius)
#     .close()
#     .extrude(thickness)
#     .faces(">Y").workplane().hole(hole_diameter)
# )