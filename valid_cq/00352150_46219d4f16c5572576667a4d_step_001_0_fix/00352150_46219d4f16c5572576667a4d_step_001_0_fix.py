import cadquery as cq

# Base plate
result = cq.Workplane("XY").box(60, 30, 5)

# Four holes
result = result.faces(">Z").workplane().hole(5, 2).rect(40, 20, forConstruction=True).vertices().hole(5)

# Slanted wall
result = result.faces("<Y").workplane(offset=-25).transformed(rotate=(45, 0, 0)).rect(30, 5).extrude(20)

# Slot on slanted face
result = result.faces(">Y").workplane(centerOption="CenterOfMass", offset=-5).slot2D(15, 5).cutBlind(-2)