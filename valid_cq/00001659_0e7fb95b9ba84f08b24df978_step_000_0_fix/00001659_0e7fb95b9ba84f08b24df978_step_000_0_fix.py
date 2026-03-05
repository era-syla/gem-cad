import cadquery as cq

# Base plate
base = cq.Workplane("XY").circle(40).extrude(8)

# Two hollow pins
pin_positions = [(20, 0), (-20, 0)]
pins = (
    cq.Workplane("XY")
    .pushPoints(pin_positions)
    .circle(6)          # outer radius 6 mm
    .extrude(20)        # pin height 20 mm
    .faces(">Z")
    .workplane()
    .circle(3)          # hole radius 3 mm
    .cutBlind(20)       # cut down through the pin
)

result = base.union(pins)