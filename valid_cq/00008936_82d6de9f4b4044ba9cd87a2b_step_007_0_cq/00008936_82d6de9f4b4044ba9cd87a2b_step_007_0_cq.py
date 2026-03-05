import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions
overall_length = 50.0  # Total length from top to bottom
width = 20.0           # Width of the straight section (and diameter of ends)
thickness = 5.0        # Thickness of the plate

# Hole dimensions
hole_diameter = 6.0    # Diameter of the mounting holes
hole_spacing = 30.0    # Distance between hole centers

# --- Construction ---

# 1. Create the base stadium/slot shape
# A slot shape can be made by creating a rectangle and filleting corners, 
# or by creating two circles and hulling them, or using a dedicated sketch tool.
# Here we will use a sketch based approach which is very robust.
# We center the part at the origin.

# Calculate the center-to-center distance for the main body
# If overall_length is 50 and width is 20, the radius is 10.
# The straight section length is 50 - 20 = 30.
# So the centers of the arcs are 30mm apart.
center_dist = overall_length - width

result = (
    cq.Workplane("XY")
    .sketch()
    # Create the outer stadium profile
    .slot(overall_length, width, angle=90, mode="a")
    # Create the two holes
    .push([ (0, hole_spacing/2), (0, -hole_spacing/2) ])
    .circle(hole_diameter / 2, mode="s")
    .finalize()
    .extrude(thickness)
)

# Alternatively, without sketch mode (classic API):
# result = (
#     cq.Workplane("XY")
#     .rect(width, overall_length - width) # Center rectangle
#     .extrude(thickness)
#     .edges("|Z").fillet(width / 2)      # Fillet vertical edges to make full round
#     .faces(">Z").workplane()
#     .pushPoints([(0, hole_spacing/2), (0, -hole_spacing/2)])
#     .hole(hole_diameter)
# )

# The sketch approach above is cleaner for this specific shape.