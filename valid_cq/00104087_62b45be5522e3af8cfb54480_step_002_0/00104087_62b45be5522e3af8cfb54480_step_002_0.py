import cadquery as cq

# Parameters
thickness = 3.0          # Thickness of the part
hole_width = 14.0        # Width of the central slot (diameter of the arcs)
hole_length = 28.0       # Total length of the central slot (end-to-end)
wall_width = 7.0         # Uniform width of the material around the hole

# Derived dimensions for the outer shape to ensure concentricity and uniform wall thickness
# The center-to-center distance of the arcs must remain constant.
center_distance = hole_length - hole_width
outer_width = hole_width + (2 * wall_width)
outer_length = center_distance + outer_width

# Create the CAD model
result = (
    cq.Workplane("XY")
    # Draw the outer stadium profile
    .slot2D(length=outer_length, diameter=outer_width, angle=90)
    # Draw the inner stadium profile (this becomes the hole)
    .slot2D(length=hole_length, diameter=hole_width, angle=90)
    # Extrude the resulting face (CadQuery automatically handles the nested wire as a hole)
    .extrude(thickness)
)