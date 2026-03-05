import cadquery as cq

# Parametric dimensions
length = 100.0   # Total length of the bar
width = 15.0     # Width (thickness) of the bar
height = 20.0    # Height of the bar
hole_diameter = 4.0      # Diameter of the through hole
csk_diameter = 8.0       # Diameter of the countersink
csk_angle = 90.0         # Angle of the countersink
hole_offset = 10.0       # Distance from the edge to the center of the hole

# Create the main rectangular block
# We center it on X and Y to make symmetric operations easier
result = cq.Workplane("XY").box(length, width, height)

# Define points for the holes
# We place them on the front face (XZ plane relative to the box orientation, or a face selector)
# Since the box is centered:
# x-coordinates are: -length/2 + hole_offset and length/2 - hole_offset
# z-coordinate is: 0 (centered vertically)
# y-coordinate is: width/2 (on the face)

# Select the front face (positive Y direction in default box orientation if viewed from top)
# Actually, let's just select the face by normal vector to be precise.
# Looking at the image, the holes are on one of the long side faces.
# Let's assume the face normal is along Y.

result = (
    result
    .faces(">Y")  # Select the face in the positive Y direction
    .workplane()  # Create a workplane on that face
    .pushPoints([
        (-(length / 2 - hole_offset), 0),  # Left hole
        ((length / 2 - hole_offset), 0)    # Right hole
    ])
    .cskHole(hole_diameter, csk_diameter, csk_angle) # Create countersunk holes
)

# If the holes were simple counterbores or just through holes, we would use cboreHole or hole.
# The image shows a conical depression, which indicates a countersink.