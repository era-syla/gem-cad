import cadquery as cq

# Parametric dimensions
length = 100.0  # Center-to-center distance
width = 15.0    # Width of the link
thickness = 5.0 # Thickness of the link
hole_diam = 6.0 # Diameter of the holes at the ends

# Create the basic shape
# We start with a box and fillet the ends, or sketch the profile directly.
# A sketch approach is often cleaner for this "slot" or "stadium" shape.

result = (
    cq.Workplane("XY")
    # Draw a slot shape using center-to-center distance and diameter (width)
    .slot2D(length, width)
    # Extrude it to create the solid body
    .extrude(thickness)
    # Select the top face for drilling holes
    .faces(">Z")
    .workplane()
    # Create two points at the centers of the rounded ends
    # Since the slot is centered at (0,0), the ends are at (-length/2, 0) and (length/2, 0)
    .pushPoints([(-length / 2.0, 0), (length / 2.0, 0)])
    # Cut the holes
    .hole(hole_diam)
)