import cadquery as cq

# Parameters
thickness = 3

# Build main plate
base = cq.Workplane("XY").rect(200, 60).extrude(thickness)

# Build two mounting ears on top of the plate
ear1 = cq.Workplane("XY").transformed(offset=(-60, 30, 0)).rect(80, 30).extrude(thickness)
ear2 = cq.Workplane("XY").transformed(offset=(60, 30, 0)).rect(80, 30).extrude(thickness)

# Combine base and ears
plate = base.union(ear1).union(ear2)

# Add large mounting holes in ears
mount_hole_positions = [(-60, 30), (60, 30)]
plate = plate.faces(">Z").workplane().pushPoints(mount_hole_positions).hole(20)

# Add small countersunk holes at corners
corner_holes = [
    (-90, -30), (-90, 30),
    (90, -30),  (90, 30),
    (-110, 30), (110, 30)
]
plate = plate.faces(">Z").workplane().pushPoints(corner_holes).hole(5)

# Cut central slot
plate = plate.faces(">Z").workplane().rect(40, 10).cutThruAll()

# Engrave text on top face
plate = plate.faces(">Z").workplane().text("VORON 2.4", 8, -1)

result = plate