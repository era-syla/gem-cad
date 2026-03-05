import cadquery as cq

# Create T-shaped base plate
points = [(-60, 0), (60, 0), (60, -15), (30, -15), (30, -60),
          (-30, -60), (-30, -15), (-60, -15)]
base = cq.Workplane("XY").polyline(points).close().extrude(5)

# Add holes in the crossbar
base = (base.faces(">Z").workplane()
        .pushPoints([(0, -7.5)]).hole(8)
        .pushPoints([(-30, -7.5), (30, -7.5)]).hole(4))

# Add mounting holes in the lower plate
plate_holes = [(-20, -25), (20, -25), (-20, -55), (20, -55)]
base = base.faces(">Z").workplane().pushPoints(plate_holes).hole(4)

# Create square bosses on top of the crossbar
boss_positions = [(-55, -7.5), (-20, -7.5), (20, -7.5), (55, -7.5)]
bosses = (cq.Workplane("XY")
          .workplane(offset=5)
          .pushPoints(boss_positions)
          .rect(10, 10)
          .extrude(5))

# Create cylinders to cut holes through the bosses
boss_cutters = (cq.Workplane("XY")
                .workplane(offset=5)
                .pushPoints(boss_positions)
                .circle(2)
                .extrude(5))

# Combine all and subtract boss holes
result = base.union(bosses).cut(boss_cutters)