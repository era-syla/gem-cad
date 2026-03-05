import cadquery as cq
import math

# Base foot with filleted top edges
base = cq.Workplane("XY").box(60, 40, 10).edges(">Z").fillet(2)

# Seat plate on top of base
seat = (base.faces(">Z")
            .workplane()
            .transformed(offset=(0, -10, 5))
            .box(40, 10, 10))

# Fixed jaw mounted on the seat plate
fixed_jaw = (seat.faces(">Z")
                 .workplane()
                 .box(20, 10, 20))

# Movable jaw on the opposite side
movable_jaw = (base.faces(">Z")
                   .workplane()
                   .transformed(offset=(0, 10, 5))
                   .box(20, 10, 20))

# Screw rod passing through the movable jaw
screw = (cq.Workplane("XY")
           .transformed(offset=(0, 11, 25))
           .circle(1.5)
           .extrude(-42))

# Large hoop ring
path_wire = cq.Workplane("XY").circle(100).val()
ring = (cq.Workplane("YZ")
          .circle(1.5)
          .sweep(path_wire, isFrenet=True))

# Combine all parts
result = base.union(seat).union(fixed_jaw).union(movable_jaw).union(screw).union(ring)