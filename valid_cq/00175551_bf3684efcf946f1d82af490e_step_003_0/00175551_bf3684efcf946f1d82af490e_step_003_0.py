import cadquery as cq

# Parameter definitions
length = 120.0       # Total length of the link
width = 20.0         # Width of the link
thickness = 3.0      # Thickness of the material
hole_diameter = 4.0  # Diameter of the holes

# Calculate the distance from center to the outer hole centers
# Assuming outer holes are concentric with the rounded ends of the slot
# The center-to-center distance of the slot arcs is (length - width)
# Distance from origin to one side is (length - width) / 2
outer_hole_offset = (length - width) / 2

# Create the 3D model
result = (
    cq.Workplane("XY")
    # Create the base slot shape (lozenge)
    .slot2D(length, width)
    .extrude(thickness)
    # Select the top face to cut holes
    .faces(">Z")
    .workplane()
    # Define points for the three holes: center, left, and right
    .pushPoints([
        (0, 0),
        (-outer_hole_offset, 0),
        (outer_hole_offset, 0)
    ])
    # Cut the holes
    .hole(hole_diameter)
)