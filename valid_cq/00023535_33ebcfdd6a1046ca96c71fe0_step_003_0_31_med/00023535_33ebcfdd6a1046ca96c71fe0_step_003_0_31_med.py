import cadquery as cq

# Parametric dimensions
base_length = 220
base_width = 80
base_height = 30
channel_width = 36
channel_depth = 12

right_len = 45
left_len = 50
left_x = -35
jaw_height = 45
jaw_width = base_width - 10

# Create Base
base = cq.Workplane("XY").box(base_length, base_width, base_height)
# Center channel
base = base.faces(">Z").workplane().rect(base_length, channel_width).extrude(-channel_depth, combine="cut")
# Side cutouts to form flanges
base = base.faces("<Z").workplane().rect(base_length, base_width - 16).extrude(8, combine="cut")

# Right Block (Fixed Jaw Body)
right_x = base_length / 2 - right_len / 2
right_block = (cq.Workplane("XY")
               .transformed(offset=(right_x, 0, base_height / 2 + jaw_height / 2))
               .box(right_len, base_width, jaw_height))
# Chamfer the back of the fixed block
right_block = right_block.edges(">Z").edges(">X").chamfer(15)

# Right Jaw Plate
jaw_plate_right = (cq.Workplane("XY")
                   .transformed(offset=(right_x - right_len / 2 - 4, 0, base_height / 2 + jaw_height / 2 - 2))
                   .box(8, jaw_width, jaw_height - 4))

# Left Block (Movable Jaw Body)
left_block = (cq.Workplane("XY")
              .transformed(offset=(left_x, 0, base_height / 2 + jaw_height / 2))
              .box(left_len, base_width, jaw_height))
# Chamfer sides and back to mimic the arched casting
left_block = left_block.edges(">Z").edges("<X").chamfer(18)
left_block = left_block.edges(">Z").edges(">Y").chamfer(10)
left_block = left_block.edges(">Z").edges("<Y").chamfer(10)

# Left Jaw Plate
jaw_plate_left = (cq.Workplane("XY")
                  .transformed(offset=(left_x + left_len / 2 + 4, 0, base_height / 2 + jaw_height / 2 - 2))
                  .box(8, jaw_width, jaw_height - 4))

# Screw and Thread Representation
screw_dia = 15
screw_z = base_height / 2 + 10
screw_start = left_x - left_len / 2 - 10
screw_end = right_x - right_len / 2
screw_len = screw_end - screw_start

# Main screw shaft
screw = (cq.Workplane("YZ")
         .transformed(offset=(0, screw_z, 0))
         .workplane(offset=screw_start)
         .circle(screw_dia / 2)
         .extrude(screw_len))

# Fake threads via rings
thread_rings = cq.Workplane()
num_rings = int((screw_len - 25) / 2.5)
for i in range(num_rings):
    ring = (cq.Workplane("YZ")
            .transformed(offset=(0, screw_z, 0))
            .workplane(offset=screw_start + 15 + i * 2.5)
            .circle(screw_dia / 2 + 0.8)
            .extrude(1.2))
    thread_rings = thread_rings.union(ring)

screw = screw.union(thread_rings)

# Hub for handle
hub_len = 22
hub_start = screw_start
hub = (cq.Workplane("YZ")
       .transformed(offset=(0, screw_z, 0))
       .workplane(offset=hub_start)
       .circle(12)
       .extrude(-hub_len))

# Handle Shaft
handle_x = hub_start - 10
handle_len = 120
handle = (cq.Workplane("XZ")
          .transformed(offset=(handle_x, screw_z, 0))
          .workplane(offset=-handle_len / 2)
          .circle(3.5)
          .extrude(handle_len))

# Handle Knobs
knob1 = cq.Workplane("XY").transformed(offset=(handle_x, -handle_len / 2, screw_z)).sphere(6.5)
knob2 = cq.Workplane("XY").transformed(offset=(handle_x, handle_len / 2, screw_z)).sphere(6.5)

# Final Assembly
result = (base
          .union(right_block)
          .union(jaw_plate_right)
          .union(left_block)
          .union(jaw_plate_left)
          .union(screw)
          .union(hub)
          .union(handle)
          .union(knob1)
          .union(knob2))