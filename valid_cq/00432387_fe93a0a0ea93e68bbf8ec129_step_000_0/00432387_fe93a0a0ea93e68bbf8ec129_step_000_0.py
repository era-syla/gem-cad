import cadquery as cq

# Parametric dimensions based on the visual proportions
plate_width = 30.0
straight_length = 60.0
thickness = 10.0

# Generate the 3D model
# We create a sketch on the XY plane starting with the straight section,
# add the semi-circular end using a 3-point arc, and extrude.
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(straight_length, 0)
    .threePointArc(
        (straight_length + plate_width / 2.0, plate_width / 2.0),  # Midpoint of the arc
        (straight_length, plate_width)                             # End point of the arc
    )
    .lineTo(0, plate_width)
    .close()
    .extrude(thickness)
)