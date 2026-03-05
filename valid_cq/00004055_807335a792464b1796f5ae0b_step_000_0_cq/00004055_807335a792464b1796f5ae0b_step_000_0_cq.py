import cadquery as cq

# Parametric dimensions
outer_width = 100.0   # Width of the outer square
outer_length = 100.0  # Length of the outer square
thickness = 10.0      # Thickness of the plate
wall_width = 15.0     # Width of the frame wall

# Calculated dimensions
inner_width = outer_width - 2 * wall_width
inner_length = outer_length - 2 * wall_width

# Generate the model
# Create a workplane, draw the outer rectangle, draw the inner rectangle, and extrude
result = (
    cq.Workplane("XY")
    .rect(outer_width, outer_length)
    .rect(inner_width, inner_length)
    .extrude(thickness)
)