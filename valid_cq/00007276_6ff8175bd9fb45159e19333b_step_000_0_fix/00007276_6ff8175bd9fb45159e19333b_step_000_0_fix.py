import cadquery as cq

# Parameters
bar_length = 200.0
bar_width = 20.0
bar_thickness = 5.0
flange_width = 4.0
slot_length = 12.0

# Create main bar
result = (
    cq.Workplane("XY")
    .rect(bar_length, bar_width)
    .extrude(bar_thickness)
)

# Calculate inner slot dimensions
inner_slot_width = bar_width - 2 * flange_width
slot_depth = bar_thickness

# Cut slots from top face at both ends
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-bar_length/2 + slot_length/2, 0),
        ( bar_length/2 - slot_length/2, 0)
    ])
    .rect(slot_length, inner_slot_width)
    .cutBlind(-slot_depth)
)