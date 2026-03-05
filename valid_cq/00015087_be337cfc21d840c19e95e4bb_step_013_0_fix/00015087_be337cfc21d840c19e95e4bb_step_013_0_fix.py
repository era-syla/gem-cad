import cadquery as cq

# Create the bolt
bolt = (
    cq.Workplane("XY")
    .circle(5)  # Cylinder diameter
    .extrude(30)  # Cylinder height
    .faces(">Z")
    .workplane()
    .circle(7)
    .extrude(2)
    .faces(">Z")
    .workplane()
    .hole(3)  # Thread hole diameter
)

# Create the washer
washer = (
    cq.Workplane("XY")
    .circle(7)
    .circle(4)
    .extrude(2)
)

# Create the nut
nut = (
    cq.Workplane("XY")
    .polygon(6, 10)  # Hexagon shape
    .extrude(4)  # Nut thickness
    .faces(">Z")
    .workplane()
    .hole(3)  # Thread hole diameter
)

# Assemble the components
result = bolt.union(washer.translate((0, 0, 32))).union(nut.translate((0, 0, 34)))
