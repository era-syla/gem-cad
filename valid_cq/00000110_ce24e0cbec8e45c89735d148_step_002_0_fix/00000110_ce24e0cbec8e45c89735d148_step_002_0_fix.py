import cadquery as cq

# Build each component separately, then combine as an assembly

# 1. Crankshaft / main shaft assembly (center piece)
shaft = (
    cq.Workplane("XY")
    .cylinder(80, 4)
)

# Threaded end (simplified as cylinder)
threaded_end = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, -50))
    .cylinder(20, 3)
)

# Flange/collar on left side
flange = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, 35))
    .cylinder(8, 10)
)

# Large disk/flywheel on left
flywheel = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, 44))
    .cylinder(6, 18)
)

# Grooved ring around flywheel
groove_outer = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, 44))
    .cylinder(6, 20)
)

# Combine shaft components
shaft_assy = (
    shaft
    .union(threaded_end)
    .union(flange)
    .union(flywheel)
)

# 2. Piston (cylinder with slot cut)
piston = (
    cq.Workplane("XY")
    .cylinder(30, 20)
)

# Cut a slot in the piston
piston = (
    piston
    .faces(">Z")
    .workplane()
    .rect(5, 25)
    .cutBlind(-15)
)

# Cut a cross hole in piston
piston = (
    piston
    .faces(">X")
    .workplane()
    .center(0, 5)
    .circle(3)
    .cutThruAll()
)

# 3. Connecting rod
rod_body = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, 0))
    .box(5, 35, 8)
)

# Add circles at ends of connecting rod
rod_end1 = (
    cq.Workplane("XY")
    .transformed(offset=(0, 17, 0))
    .cylinder(8, 8)
)

rod_end2 = (
    cq.Workplane("XY")
    .transformed(offset=(0, -17, 0))
    .cylinder(6, 8)
)

# Cut holes in rod ends
rod_end1_hole = (
    cq.Workplane("XY")
    .transformed(offset=(0, 17, 0))
    .cylinder(8, 4)
)

connecting_rod = rod_body.union(rod_end1).union(rod_end2)

# Cut holes through rod ends
connecting_rod = (
    connecting_rod
    .faces(">Z")
    .workplane()
    .center(0, 17)
    .circle(3)
    .cutThruAll()
)

connecting_rod = (
    connecting_rod
    .faces(">Z")
    .workplane()
    .center(0, -17)
    .circle(2)
    .cutThruAll()
)

# 4. Knurled nut/wheel on right side
knurled_wheel = (
    cq.Workplane("XY")
    .cylinder(8, 18)
)

# Add a hub in center
wheel_hub = (
    cq.Workplane("XY")
    .cylinder(12, 8)
)

knurled_wheel = knurled_wheel.union(wheel_hub)

# Cut center hole
knurled_wheel = (
    knurled_wheel
    .faces(">Z")
    .workplane()
    .circle(3)
    .cutThruAll()
)

# Position all parts in exploded view
# Shaft assembly at origin
shaft_final = shaft_assy

# Piston upper left
piston_final = piston.translate((-60, 40, 50))

# Connecting rod upper middle
rod_final = connecting_rod.translate((-10, 30, 20))

# Knurled wheel right side
wheel_final = knurled_wheel.translate((70, -20, -10))

# Combine all into one result
result = (
    shaft_final
    .union(piston_final)
    .union(rod_final)
    .union(wheel_final)
)