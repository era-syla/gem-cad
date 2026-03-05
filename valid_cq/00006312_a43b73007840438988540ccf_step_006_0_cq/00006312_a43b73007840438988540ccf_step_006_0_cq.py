import cadquery as cq

# Parameters
length = 100.0       # Total length of the rail
width = 20.0         # Width of the rail
base_height = 5.0    # Thickness of the base plate
tooth_height = 5.0   # Height of the teeth above the base
tooth_width = 10.0   # Width of each tooth (along the length axis)
gap_width = 10.0     # Gap between teeth
num_teeth = 4        # Number of raised teeth
hole_diameter = 4.0  # Diameter of the mounting holes
hole_offset = 5.0    # Distance from the end edge to the hole center

# Derived dimensions
total_height = base_height + tooth_height

# Calculate positions
# The rail consists of a base and a series of teeth.
# Let's center the object at the origin.

# Create the base plate
result = cq.Workplane("XY").box(length, width, base_height)

# Create the teeth
# We need to calculate the starting position for the first tooth to center the pattern
# Pattern length = num_teeth * tooth_width + (num_teeth - 1) * gap_width
pattern_length = num_teeth * tooth_width + (num_teeth - 1) * gap_width
start_x = -pattern_length / 2.0 + tooth_width / 2.0

# Define a single tooth
def create_tooth(loc):
    return cq.Solid.makeBox(tooth_width, width, tooth_height).translate(
        (loc.x, -width / 2.0, base_height / 2.0)
    )

# Use points to place the teeth
# Generate a list of x-coordinates for the teeth centers
tooth_centers = [
    (start_x + i * (tooth_width + gap_width), 0) for i in range(num_teeth)
]

# Add teeth to the base
result = result.pushPoints(tooth_centers).rect(tooth_width, width).extrude(tooth_height)

# Create mounting holes
# Holes are typically centered on the flat sections at the ends
hole_x_pos = length / 2.0 - hole_offset

result = (
    result.faces(">Z[1]")  # Select the top face of the base (not the teeth)
    .workplane()
    .pushPoints([(hole_x_pos, 0), (-hole_x_pos, 0)])
    .hole(hole_diameter)
)