import cadquery as cq

# Parameters for the model dimensions
radius = 10.0
length = 50.0
offset_val = 15.0

# Create the top cylinder
# The cylinder is extruded along the X-axis (from the YZ plane)
# It is shifted in the +Y and +Z direction to match the upper position in the image
top_cylinder = (
    cq.Workplane("YZ")
    .circle(radius)
    .extrude(length)
    .translate((0, offset_val, offset_val))
)

# Create the bottom quarter-cylinder (quadrant extrusion)
# The profile is created in the YZ plane.
# Based on the image lighting and orientation, the curved face points "outwards" (Top-Left).
# This corresponds to the profile occupying the 2nd quadrant (-Y, +Z) relative to its corner.
bottom_quarter = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(0, radius)  # Vertical edge
    .threePointArc(
        (-radius * 0.707107, radius * 0.707107),  # Arc midpoint (135 degrees)
        (-radius, 0)                              # Arc endpoint (-90 degrees relative to start)
    )
    .close()  # Horizontal edge back to origin
    .extrude(length)
    .translate((0, -offset_val, -offset_val))
)

# Combine the two separate solids into the final result
result = top_cylinder.union(bottom_quarter)