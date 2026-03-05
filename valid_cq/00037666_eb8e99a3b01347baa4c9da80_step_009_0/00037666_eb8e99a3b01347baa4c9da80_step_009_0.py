import cadquery as cq

# Parameter definitions based on the visual proportions of the image
num_holes = 5           # Total number of holes
hole_diameter = 8.0     # Diameter of the circular holes
hole_pitch = 16.0       # Distance between hole centers
bar_width = 16.0        # Width of the link (matches pitch for concentric rounded ends)
thickness = 3.0         # Thickness of the part

# Derived dimensions
# The distance between the centers of the first and last holes
center_to_center_length = (num_holes - 1) * hole_pitch

# The total length of the part (center-to-center + 2 * radius)
# Since the ends are semi-circles tangent to the width, the radius is bar_width / 2.
# Adding 2 * radius is adding bar_width.
total_length = center_to_center_length + bar_width

# Calculate hole coordinates centering the pattern on the origin
# The range starts from negative half of the center-to-center length
start_x = -center_to_center_length / 2.0
hole_points = [(start_x + i * hole_pitch, 0) for i in range(num_holes)]

# Generate the model
result = (
    cq.Workplane("XY")
    # Create the base 'stadium' or slot shape profile
    # slot2D takes (length, width) where length is the total extent
    .slot2D(total_length, bar_width)
    .extrude(thickness)
    # Select the top face to create the holes
    .faces(">Z")
    .workplane()
    # define the locations for the holes
    .pushPoints(hole_points)
    # Cut the holes through the solid
    .hole(hole_diameter)
)