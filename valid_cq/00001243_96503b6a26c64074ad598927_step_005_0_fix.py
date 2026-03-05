import cadquery as cq

# Create a letter opener / paper knife shape
# Main body: flat blade that tapers to a point

total_length = 180
blade_length = 120
handle_length = 60
blade_width = 12
handle_width = 14
thickness = 3
tip_length = 40

# Build the profile in 2D then extrude
# The shape: handle (rectangular) + blade (tapers to point)

# Points for the top profile (XY plane, length along X)
# Handle portion then blade portion tapering to point

import cadquery as cq
from cadquery import Vector

# Create the flat body as a lofted/extruded 2D shape
# Use a 2D wire and extrude

# Profile points (viewed from top):
# Start at origin (left end of handle), go clockwise
# Handle: from x=0 to x=handle_length, width=handle_width
# Blade: from x=handle_length to x=total_length, tapers from blade_width to 0

pts_top = [
    (0, handle_width/2),
    (handle_length, blade_width/2),
    (total_length, 0),
    (handle_length, -blade_width/2),
    (0, -handle_width/2),
    (0, handle_width/2),
]

# Create the 2D profile
profile = (
    cq.Workplane("XY")
    .polyline([
        (0, handle_width/2),
        (handle_length, blade_width/2),
        (total_length, 0),
        (handle_length, -blade_width/2),
        (0, -handle_width/2),
    ])
    .close()
)

# Extrude to get flat blade body
flat_body = profile.extrude(thickness)

# Add a slight raised ridge along the center of the handle for grip
# Ridge on top of handle
ridge = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0, thickness))
    .rect(handle_length * 0.9, handle_width * 0.3)
    .extrude(thickness * 0.3)
    .translate((handle_length * 0.45, 0, 0))
)

# Combine
result = flat_body

# Fillet the edges slightly
result = (
    result
    .edges("|Z")
    .fillet(1.0)
)

# Rotate to match image orientation (diagonal)
result = result.rotate((0,0,0), (0,0,1), 35)