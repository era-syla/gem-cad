import cadquery as cq

# Main trailer body dimensions
body_length = 8.0
body_width = 2.2
body_height = 2.2
roof_chamfer_depth = 0.4  # front top chamfer

# Build the main trailer box body with chamfered front top edge
# Using a 2D profile on the side (XZ plane) then extrude in Y
# Side profile: rectangle with top-front corner cut

# Points for side profile (in XZ plane)
# Front is at x=0, rear at x=body_length
# Bottom at z=0, top at z=body_height
# Top-front corner is chamfered

side_pts = [
    (0, 0),
    (body_length, 0),
    (body_length, body_height),
    (chamfer_x := roof_chamfer_depth, body_height),
    (0, body_height - roof_chamfer_depth),
]

side_profile = [
    (0, 0),
    (body_length, 0),
    (body_length, body_height),
    (roof_chamfer_depth, body_height),
    (0, body_height - roof_chamfer_depth),
]

# Create the body by extruding the side profile
body = (
    cq.Workplane("XZ")
    .polyline(side_profile)
    .close()
    .extrude(body_width)
)

# Translate body so it's centered in Y and starts at z=0
body = body.translate((0, -body_width / 2, 0))

# Undercarriage/chassis - a flat plate under the body
chassis_thickness = 0.15
chassis = (
    cq.Workplane("XY")
    .box(body_length + 1.5, body_width - 0.2, chassis_thickness)
    .translate((body_length / 2 - 0.75, 0, -chassis_thickness / 2))
)

# Tongue/hitch extending from front
tongue_length = 1.5
tongue_width = 0.15
tongue_height = 0.1

tongue = (
    cq.Workplane("XY")
    .box(tongue_length, tongue_width, tongue_height)
    .translate((-tongue_length / 2, 0, chassis_thickness / 2))
)

# Tongue support triangle - two angled bars
support1 = (
    cq.Workplane("XY")
    .box(tongue_length, tongue_width * 0.8, tongue_height * 0.8)
    .rotate((0, 0, 0), (0, 0, 1), 15)
    .translate((-tongue_length / 2, body_width * 0.2, chassis_thickness / 2))
)

support2 = (
    cq.Workplane("XY")
    .box(tongue_length, tongue_width * 0.8, tongue_height * 0.8)
    .rotate((0, 0, 0), (0, 0, 1), -15)
    .translate((-tongue_length / 2, -body_width * 0.2, chassis_thickness / 2))
)

# Wheels - dual axle at rear
wheel_radius = 0.35
wheel_width = 0.2
axle_y_offset = body_width / 2 + wheel_width / 2 + 0.05

# Axle positions (two axles near rear)
axle1_x = body_length * 0.72
axle2_x = body_length * 0.85
wheel_z = wheel_radius - chassis_thickness / 2 - 0.05

def make_wheel(x, y):
    return (
        cq.Workplane("YZ")
        .circle(wheel_radius)
        .extrude(wheel_width)
        .translate((x, y - wheel_width / 2, wheel_z))
    )

wheel1L = make_wheel(axle1_x, axle_y_offset)
wheel1R = make_wheel(axle1_x, -axle_y_offset - wheel_width)
wheel2L = make_wheel(axle2_x, axle_y_offset)
wheel2R = make_wheel(axle2_x, -axle_y_offset - wheel_width)

# Wheel hubs (inner cylinder)
hub_radius = wheel_radius * 0.4
hub_width = wheel_width * 1.1

def make_hub(x, y):
    return (
        cq.Workplane("YZ")
        .circle(hub_radius)
        .extrude(hub_width)
        .translate((x, y - hub_width / 2, wheel_z))
    )

hub1L = make_hub(axle1_x, axle_y_offset)
hub1R = make_hub(axle1_x, -axle_y_offset - hub_width)
hub2L = make_hub(axle2_x, axle_y_offset)
hub2R = make_hub(axle2_x, -axle_y_offset - hub_width)

# Combine everything
result = (
    body
    .union(chassis)
    .union(tongue)
    .union(support1)
    .union(support2)
    .union(wheel1L)
    .union(wheel1R)
    .union(wheel2L)
    .union(wheel2R)
    .union(hub1L)
    .union(hub1R)
    .union(hub2L)
    .union(hub2R)
)