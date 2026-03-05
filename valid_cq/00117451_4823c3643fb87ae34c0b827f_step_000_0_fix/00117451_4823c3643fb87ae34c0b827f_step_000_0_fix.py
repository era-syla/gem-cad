import cadquery as cq

# Parameters (all in mm)
length = 200
flange_width = 50
web_height = 10
lip_length = 3
thickness = 2

# Define the cross-section profile
profile = [
    (0, 0),
    (flange_width, 0),
    (flange_width, -thickness),
    (flange_width - lip_length, -thickness),
    (flange_width - lip_length, -web_height),
    (0, -web_height),
]

# Build the section and extrude
result = (
    cq.Workplane("XY")
      .polyline(profile)
      .close()
      .extrude(length)
)