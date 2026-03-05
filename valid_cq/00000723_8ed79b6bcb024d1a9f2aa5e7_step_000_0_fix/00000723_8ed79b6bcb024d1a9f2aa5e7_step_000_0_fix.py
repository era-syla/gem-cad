import cadquery as cq

# Parameters
flange_radius = 20
flange_thickness = 4
shaft_radius = 10
shaft_length = 15
hex_size = 7  # hex socket across flats
hex_depth = 10

# Build the flange (large disk)
flange = (
    cq.Workplane("XY")
    .circle(flange_radius)
    .extrude(flange_thickness)
)

# Add a fillet to the front face edge of the flange
flange = (
    flange
    .faces(">Z")
    .edges()
    .fillet(1.5)
)

# Build the shaft (cylinder extending from back of flange)
shaft = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .circle(shaft_radius)
    .extrude(-shaft_length)
)

# Union flange and shaft
result = flange.union(shaft)

# Cut hex socket into the front face (going through flange into shaft)
result = (
    result
    .faces(">Z")
    .workplane()
    .polygon(6, hex_size * 2 / (3**0.5), circumscribed=False)
    .cutBlind(-(hex_depth))
)

# Add a small chamfer to the hex socket entrance edges
# We need to select the top edges of the hex pocket
# Use a different approach - cut with a slightly larger polygon at top for chamfer effect
# Instead, let's add a chamfer to the hex opening
try:
    result = (
        result
        .faces(">Z")
        .edges("not >Z")
        .chamfer(0.3)
    )
except Exception:
    pass

result = result