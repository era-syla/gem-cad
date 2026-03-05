import cadquery as cq

# Define the bracket
bracket = (
    cq.Workplane("XY")
    .box(40, 10, 10)
    .faces(">Z").workplane(centerOption="CenterOfMass")
    .circle(5).cutThruAll()
)

# Define the peg
peg = (
    cq.Workplane("XY")
    .circle(2.5)
    .extrude(10)
)

# Place the peg
bracket_with_peg = bracket.union(peg.translate((25, 0, -5)))

# Define the pin
pin = cq.Workplane("XY").circle(2).extrude(10)

# Create array of pins
pins = [
    pin.translate((15, 0, 5)),
    pin.translate((20, 0, 5)),
    pin.translate((25, 0, 5))
]

# Combine all parts
result = bracket_with_peg
for pin_item in pins:
    result = result.union(pin_item)