import cadquery as cq

# Parameters
body_length = 60
body_width = 30
body_height = 20
pin_length = 10
pin_thickness = 2
pin_height = 2
pin_positions = [-20, -10, 0, 10, 20]
panel_thickness = 2

result = (
    cq.Workplane("XY")
    .box(body_length, body_width, body_height)
    # Add pins on the long face
    .faces(">Y")
    .workplane()
    .pushPoints([(x, 0) for x in pin_positions])
    .rect(pin_thickness, pin_height)
    .extrude(pin_length)
    # Add end panels on +X face
    .add(
        cq.Workplane("YZ", origin=(body_length/2, 0, 0))
        .rect(body_width, body_height)
        .extrude(panel_thickness)
    )
    # Add end panels on -X face
    .add(
        cq.Workplane("YZ", origin=(-body_length/2, 0, 0))
        .rect(body_width, body_height)
        .extrude(-panel_thickness)
    )
)