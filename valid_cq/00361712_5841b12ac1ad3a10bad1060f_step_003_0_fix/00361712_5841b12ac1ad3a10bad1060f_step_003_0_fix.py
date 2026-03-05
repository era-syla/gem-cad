import cadquery as cq

# Parameters
shaft_radius = 5
shaft_length = 40
flange_radius = 12
flange_thickness = 3
fillet_radius = 1

# Build the shaft
result = (
    cq.Workplane("XY")
    .circle(shaft_radius)
    .extrude(shaft_length)
    # Build the flange on top of the shaft
    .faces(">Z")
    .workplane()
    .circle(flange_radius)
    .extrude(flange_thickness)
    # Round all external sharp edges
    .edges()
    .fillet(fillet_radius)
)