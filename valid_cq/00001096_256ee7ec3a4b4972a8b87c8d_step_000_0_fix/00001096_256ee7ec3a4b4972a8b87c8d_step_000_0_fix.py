import cadquery as cq

# Base plate
result = cq.Workplane("XY").box(120, 100, 5)

# Cylindrical cup
cup = (
    cq.Workplane("XY")
    .workplane(offset=5)
    .circle(20)
    .extrude(50)
    .faces(">Z")
    .workplane()
    .circle(15)
    .cutBlind(-40)
)
result = result.union(cup)

# Side walls for U-bracket
wall1 = cq.Workplane("XY").transformed(offset=(-25, 0, 5)).box(10, 50, 60)
wall2 = cq.Workplane("XY").transformed(offset=( 25, 0, 5)).box(10, 50, 60)
result = result.union(wall1).union(wall2)

# Top U-bracket plate
bracket_top = cq.Workplane("XY").transformed(offset=(0, 0, 65)).box(50, 50, 5)
result = result.union(bracket_top)

# Vertical legs of the U-bracket
leg1 = cq.Workplane("XY").transformed(offset=(-25, 0, 65)).box(5, 50, 50)
leg2 = cq.Workplane("XY").transformed(offset=( 25, 0, 65)).box(5, 50, 50)
result = result.union(leg1).union(leg2)

# Hole through the top plate
result = result.faces(">Z").workplane().circle(10).cutThruAll()

# Four support rods and lower beam
rod_positions = [(-40, -40), (40, -40), (40, 40), (-40, 40)]
for x, y in rod_positions:
    rod = cq.Workplane("XY").transformed(offset=(x, y, 5)).circle(3).extrude(40)
    result = result.union(rod)

beam = cq.Workplane("XY").transformed(offset=(0, 0, 40)).box(80, 80, 10)
result = result.union(beam)

# Gearbox block and shaft
gearbox = cq.Workplane("XY").transformed(offset=(50, 0, 5)).box(20, 20, 20)
shaft   = cq.Workplane("YZ").transformed(offset=(60, 0, 15)).circle(3).extrude(10)
gear    = cq.Workplane("YZ").transformed(offset=(60, 0, 25)).circle(8).extrude(3)
result = result.union(gearbox).union(shaft).union(gear)