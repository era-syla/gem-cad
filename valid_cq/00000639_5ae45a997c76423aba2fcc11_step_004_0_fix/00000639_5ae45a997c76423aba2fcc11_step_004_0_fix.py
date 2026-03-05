import cadquery as cq

# Main plate dimensions
plate_w = 120
plate_h = 100
plate_t = 5
corner_r = 12

# Create the main plate outline as a rounded rectangle
result = (
    cq.Workplane("XY")
    .rect(plate_w, plate_h)
    .extrude(plate_t)
)

# Apply fillets to top edges (rounded corners on the main body)
result = result.edges("|Z").fillet(corner_r)

# Now cut notches on the bottom edge (front side) - two notches
# Left notch
notch_w = 10
notch_d = 6

result = (
    result
    .faces(">Y")
    .workplane()
    .center(-25, 0)
    .rect(notch_w, notch_d * 2)
    .cutBlind(-notch_d)
)

# Right notch  
result = (
    result
    .faces(">Y")
    .workplane()
    .center(25, 0)
    .rect(notch_w, notch_d * 2)
    .cutBlind(-notch_d)
)

# Cut a slot/handle near the top of the plate
slot_w = 30
slot_h = 8
slot_r = 4

result = (
    result
    .faces(">Z")
    .workplane()
    .center(-15, 20)
    .slot2D(slot_w, slot_h, 0)
    .cutThruAll()
)

# Cut two small square holes (mounting holes)
sq_size = 5

# Upper right square hole
result = (
    result
    .faces(">Z")
    .workplane()
    .center(20, 10)
    .rect(sq_size, sq_size)
    .cutThruAll()
)

# Lower left square hole
result = (
    result
    .faces(">Z")
    .workplane()
    .center(-15, -15)
    .rect(sq_size, sq_size)
    .cutThruAll()
)

# Cut notches on right side
right_notch_w = 6
right_notch_d = 8

result = (
    result
    .faces(">X")
    .workplane()
    .center(0, 0)
    .rect(right_notch_d * 2, right_notch_w)
    .cutBlind(-right_notch_d)
)