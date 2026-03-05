import cadquery as cq

# Parameters
length = 100.0
height = 10.0
thickness = 1.0
flange_length = 3.0
flange_depth = 2.0

# Create the main profile
pts = [
    (0, 0),
    (0, height),
    (flange_length, height),
    (flange_length, height - thickness),
    (thickness, height - thickness),
    (thickness, thickness),
    (length - thickness, thickness),
    (length - thickness, height - thickness),
    (length - flange_length, height - thickness),
    (length - flange_length, height),
    (length, height),
    (length, 0)
]

# We need a top-down view profile to extrude
# Let's draw it in the XY plane and extrude along Z

pts_xy = [
    (0, flange_depth),
    (flange_length, flange_depth),
    (flange_length, thickness),
    (length - flange_length, thickness),
    (length - flange_length, flange_depth),
    (length, flange_depth),
    (length, 0),
    (0, 0)
]

result = (
    cq.Workplane("XY")
    .polyline(pts_xy)
    .close()
    .extrude(height)
)
