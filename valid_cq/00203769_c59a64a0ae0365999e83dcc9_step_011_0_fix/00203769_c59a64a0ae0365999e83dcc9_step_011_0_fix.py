import cadquery as cq

# Base plate parameters
base_thickness = 5
base_profile = [(0, 0), (120, 0), (120, 20), (50, 20), (50, 60), (0, 60)]

# Create the L-shaped base plate
base = cq.Workplane("XY").polyline(base_profile).close().extrude(base_thickness)

# Create the vertical block on the left part of the base
block_height = 25
block = (
    base.faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .rect(40, 40)
    .extrude(block_height)
)

# Cut a rectangular through-cavity in the front face of the block
cavity_width = 20
cavity_height = 20
block = (
    block.faces("<X")
    .workplane(centerOption="CenterOfBoundBox")
    .rect(cavity_width, cavity_height)
    .cutThruAll()
)

# Create the boss on the right part of the base
boss_height = 10
boss = (
    base.faces(">Z")
    .workplane()
    .center(60, 30)
    .rect(30, 15)
    .extrude(boss_height)
)

# Drill two holes through the top of the boss
hole_dia = 6
hole_offsets = [(-8, 0), (8, 0)]
boss = boss.faces(">Z").workplane().pushPoints(hole_offsets).hole(hole_dia)

# Cut a slot through the top of the boss
slot_length = 20
slot_radius = 3
boss = boss.faces(">Z").workplane().slot2D(slot_length, slot_radius, 0).cutThruAll()

# Create a triangular support under the boss
support_depth = 40
support = (
    base.faces(">Z")
    .workplane()
    .center(60, 30)
    .polyline([(-15, -10), (15, -10), (15, 0)])
    .close()
    .extrude(support_depth)
)

# Combine all parts into the final result
result = base.union(block).union(boss).union(support)