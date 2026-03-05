import cadquery as cq

# Base plate (larger, thinner)
base_plate = (
    cq.Workplane("XY")
    .rect(120, 100)
    .extrude(4)
)

# Top plate (smaller, thicker, centered on base)
top_plate = (
    cq.Workplane("XY")
    .workplane(offset=4)
    .rect(96, 80)
    .extrude(6)
)

# Combine base and top plate
result = base_plate.union(top_plate)

# Add mounting screw holes (countersunk holes on top plate corners)
screw_positions = [
    (35, 28), (-35, 28), (35, -28), (-35, -28)
]

for x, y in screw_positions:
    result = (
        result
        .faces(">Z")
        .workplane()
        .pushPoints([(x, y)])
        .hole(4, 10)
    )

# Add rectangular slots/cutouts on the top face
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(15, 10)])
    .rect(12, 8)
    .cutBlind(-4)
)

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(-15, -10)])
    .rect(12, 8)
    .cutBlind(-4)
)

# Add small tabs/connectors on the sides of the base plate
# Right side tab
right_tab = (
    cq.Workplane("XY")
    .workplane(offset=4)
    .center(60, 0)
    .rect(8, 12)
    .extrude(3)
)

# Left side tab
left_tab = (
    cq.Workplane("XY")
    .workplane(offset=4)
    .center(-60, 0)
    .rect(8, 12)
    .extrude(3)
)

result = result.union(right_tab).union(left_tab)

# Add small connector bump on right side of top plate
right_connector = (
    cq.Workplane("XY")
    .workplane(offset=4)
    .center(48, 0)
    .rect(6, 8)
    .extrude(6)
)

result = result.union(right_connector)

# Small notch cutout in right connector
result = (
    result
    .faces(">X")
    .workplane()
    .center(0, 7)
    .rect(4, 4)
    .cutBlind(-4)
)

# Chamfer the top edges of the top plate slightly
result = (
    result
    .faces(">Z")
    .edges()
    .chamfer(0.5)
)