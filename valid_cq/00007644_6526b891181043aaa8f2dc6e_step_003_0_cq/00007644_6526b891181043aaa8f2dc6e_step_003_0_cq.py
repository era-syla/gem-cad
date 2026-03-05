import cadquery as cq

# Parametric dimensions
length = 40.0   # Overall length of the slot shape
width = 25.0    # Width of the slot (diameter of the rounded ends)
thickness = 5.0 # Thickness of the plate
hole_diam = 8.0 # Diameter of the central hole

# Calculate center-to-center distance for the slot
# The overall length is the distance between centers plus the radius at each end (2 * radius = width)
# So, center_dist = length - width
center_dist = length - width

# Create the model
# Using a sketch to create the "racetrack" or slot profile
result = (
    cq.Workplane("XY")
    .slot2D(length, width)  # Creates the outer stadium/slot shape
    .circle(hole_diam / 2)  # Creates the inner hole circle
    .extrude(thickness)     # Extrudes both profiles to create the solid with a hole
)

# Alternative construction method using rect and fillet if explicit radius control is preferred:
# result = (
#     cq.Workplane("XY")
#     .rect(center_dist, width)
#     .extrude(thickness)
#     .edges("|Z")
#     .fillet(width / 2)
#     .faces(">Z")
#     .workplane()
#     .hole(hole_diam)
# )