import cadquery as cq

# Parameters
beam_length = 200.0
half_length = beam_length / 2.0
web_height = 40.0
flange_length = 20.0
thickness = 3.0
hole_diameter = 3.0
hole_pitch = 15.0
edge_margin = 10.0

# Create U-channel cross-section and extrude
result = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),
        (flange_length, 0),
        (flange_length, thickness),
        (thickness, thickness),
        (thickness, web_height + thickness),
        (flange_length, web_height + thickness),
        (flange_length, web_height + 2 * thickness),
        (0, web_height + 2 * thickness),
    ])
    .close()
    .extrude(beam_length, both=True)
)

# Compute hole positions
n_holes = int((beam_length - 2 * edge_margin) / hole_pitch) + 1
x_positions = [ -half_length + edge_margin + i * hole_pitch for i in range(n_holes) ]
z_positions = [ edge_margin, flange_length - edge_margin ]
points = [(x, z) for x in x_positions for z in z_positions]

# Drill holes through top flange
result = (
    result
    .faces(">Y")
    .workplane()
    .pushPoints(points)
    .hole(hole_diameter)
)

# Drill holes through bottom flange
result = (
    result
    .faces("<Y")
    .workplane()
    .pushPoints(points)
    .hole(hole_diameter)
)