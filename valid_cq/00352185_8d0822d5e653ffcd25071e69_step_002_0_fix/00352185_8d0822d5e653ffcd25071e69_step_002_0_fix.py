import cadquery as cq
import math

# Parameters
L = 60        # top plate length
W = 30        # top plate width
P_t = 5       # top plate thickness
slope_run = 20
drop = 15
slope_angle = math.degrees(math.atan(drop/slope_run))
cyl_D = 16
cyl_L = 20
r = cyl_D/2
slot_w = 4
slot_h = cyl_D + 2
slot_offset = 5
hole_d = 5

# Top plate with holes
plate = cq.Workplane("XY").box(L, W, P_t)
hole_positions = [(-15, -7.5), (15, -7.5), (-15, 7.5), (15, 7.5)]
plate = plate.faces(">Z").workplane().pushPoints(hole_positions).hole(hole_d)

# Sloped support block
slope = (
    cq.Workplane("XY")
      .transformed(offset=(L/2 + slope_run/2, 0, P_t - drop/2),
                   rotate=(0, slope_angle, 0))
      .box(slope_run, W, drop)
)

# Cylinder with two slots (created in its local frame)
cyl = cq.Workplane("XY").circle(r).extrude(cyl_L)
# Slot cutting box
slot_box = cq.Workplane("XY").box(cyl_L * 1.1, slot_w, slot_h)
slot1 = slot_box.translate((slot_offset, 0, cyl_L / 2))
slot2 = slot_box.translate((-slot_offset, 0, cyl_L / 2))
cyl = cyl.cut(slot1).cut(slot2)

# Rotate cylinder to align with slope face and place it
cx = L/2 + slope_run
cz = P_t - drop
slope_cyl = (
    cyl.rotate((0, 0, 0), (0, 1, 0), slope_angle)
       .translate((cx, 0, cz - cyl_L))
)

# Final result
result = plate.union(slope).union(slope_cyl)