import cadquery as cq

# Main box body
box_w = 80
box_h = 80
box_d = 30

# Create the main box
box = cq.Workplane("XY").box(box_w, box_h, box_d)

# Fillet the vertical edges of the box
box = box.edges("|Z").fillet(4)

# Fillet the top and bottom edges
box = box.edges("#Z").fillet(2)

# Create the front face flange/lip - a raised border on the front face
# The front face is at z = box_d/2
flange_thickness = 3
flange_inset = 6

flange = (cq.Workplane("XY")
          .workplane(offset=box_d/2)
          .rect(box_w, box_h)
          .rect(box_w - flange_inset*2, box_h - flange_inset*2)
          .extrude(flange_thickness))

# Union the flange with the box
result = box.union(flange)

# Add the cylindrical boss/hub on the front face
boss_od = 28
boss_id = 20
boss_length = 12

boss = (cq.Workplane("XY")
        .workplane(offset=box_d/2)
        .circle(boss_od/2)
        .extrude(boss_length + flange_thickness))

result = result.union(boss)

# Hollow out the cylinder (bore through)
bore = (cq.Workplane("XY")
        .workplane(offset=-box_d/2 - 1)
        .circle(boss_id/2)
        .extrude(box_d + boss_length + flange_thickness + 2))

result = result.cut(bore)

# Add threaded appearance - helical grooves on the boss exterior
# Simulate threads with a series of cuts
import math

thread_pitch = 2.0
thread_depth = 0.8
num_threads = int(boss_length / thread_pitch)

for i in range(num_threads):
    z_pos = box_d/2 + flange_thickness + i * thread_pitch + thread_pitch/2
    thread_cut = (cq.Workplane("XY")
                  .workplane(offset=z_pos)
                  .circle((boss_od/2) + 0.1)
                  .circle((boss_od/2) - thread_depth)
                  .extrude(thread_pitch * 0.5))
    result = result.cut(thread_cut)

# Add mounting holes on the front face (4 corners)
hole_offset_x = 30
hole_offset_y = 30
hole_d = 4
hole_depth = box_d + boss_length + flange_thickness + 5

corner_positions = [
    (hole_offset_x, hole_offset_y),
    (-hole_offset_x, hole_offset_y),
    (hole_offset_x, -hole_offset_y),
    (-hole_offset_x, -hole_offset_y),
]

for (hx, hy) in corner_positions:
    hole = (cq.Workplane("XY")
            .workplane(offset=box_d/2 + flange_thickness + boss_length + 1)
            .center(hx, hy)
            .circle(hole_d/2)
            .extrude(box_d + flange_thickness + boss_length + 2))
    result = result.cut(hole)

# Add a small hole on the side (left face)
side_hole = (cq.Workplane("YZ")
             .workplane(offset=-box_w/2 - 1)
             .center(0, 5)
             .circle(2.5)
             .extrude(15))
result = result.cut(side_hole)

# Add a channel/groove on top front edge area
top_groove = (cq.Workplane("XY")
              .workplane(offset=box_d/2 + flange_thickness - 1)
              .rect(box_w - 2, 8)
              .extrude(4))

# Position the groove near the top
top_groove2 = (cq.Workplane("XY")
               .workplane(offset=box_d/2 + flange_thickness)
               .transformed(offset=cq.Vector(0, 32, 0))
               .rect(box_w - 14, 6)
               .extrude(3))

result = result.union(top_groove2)