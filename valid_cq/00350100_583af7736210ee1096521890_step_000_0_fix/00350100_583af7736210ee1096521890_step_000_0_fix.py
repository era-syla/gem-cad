import cadquery as cq

# Main handle/body by revolving a profile around the X-axis
body = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (5, 2),
        (20, 5),
        (100, 5),
        (140, 4),
        (170, 3),
        (170, 0),
    ])
    .close()
    .revolve(angleDegrees=360, axisStart=(0, 0, 0), axisEnd=(1, 0, 0))
)

# Prong parameters
prong_length = 120.0
prong_height = 1.5
prong_width = 8.0
prong_root_x = 5.0
prong_root_z = 5.0

# Create a single prong sketch in the XZ plane and extrude in Y
base_prong = (
    cq.Workplane("XZ")
    .center(prong_root_x + prong_length / 2, prong_root_z + prong_height / 2)
    .rect(prong_length, prong_height)
    .extrude(prong_width)
)

# Position two prongs on either side of the handle
offset_y = prong_width / 2 + 0.1
prong1 = base_prong.translate((0,  offset_y, 0))
prong2 = base_prong.translate((0, -offset_y, 0))

# Combine everything into the final result
result = body.union(prong1).union(prong2)