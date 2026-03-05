import cadquery as cq

# Base dimensions
base_len = 160
base_wid = 60
base_height = 20
slot_wid = 24
slot_depth = 10

# Base body with center slot
base_shape = cq.Workplane("XY").box(base_len, base_wid, base_height).translate((base_len/2, 0, base_height/2))
slot = cq.Workplane("XY").box(base_len, slot_wid, slot_depth).translate((base_len/2, 0, base_height - slot_depth/2))
base = base_shape.cut(slot)

# Generic jaw profile (used for both fixed and movable jaws)
jaw_length = 20
jaw_arch_wid = 34
jaw_arch_height = 25
jaw_base = cq.Workplane("XY").box(jaw_length, base_wid, 10).translate((0, 0, 5))
jaw_arch = (cq.Workplane("XY")
            .box(jaw_length, jaw_arch_wid, jaw_arch_height)
            .edges(">Z").edges("|X")
            .fillet(jaw_arch_wid/2 - 0.01)
            .translate((0, 0, jaw_arch_height/2)))
jaw_sym = jaw_base.union(jaw_arch)

# Fixed Jaw (Right side)
fixed_jaw = jaw_sym.translate((145, 0, base_height))
# Fill the back to make it a solid block
fixed_back = cq.Workplane("XY").box(15, base_wid, jaw_arch_height).translate((152.5, 0, base_height + jaw_arch_height/2))
fixed_jaw = fixed_jaw.union(fixed_back)

# Movable Jaw (Middle)
movable_jaw = jaw_sym.translate((70, 0, base_height))
# Add guide block underneath that fits into the slot
jaw_guide = cq.Workplane("XY").box(jaw_length, slot_wid - 0.5, slot_depth - 0.5).translate((70, 0, base_height - slot_depth/2))
movable_jaw = movable_jaw.union(jaw_guide)

# Front Bearing Block (Left side)
fb_base = cq.Workplane("XY").box(15, base_wid, 10).translate((0, 0, 5))
fb_arch = (cq.Workplane("XY")
           .box(15, 24, 20)
           .edges(">Z").edges("|X")
           .fillet(11.99)
           .translate((0, 0, 10)))
front_block = fb_base.union(fb_arch).translate((15, 0, base_height))

# Main Screw
screw_radius = 6
screw_z = base_height + 12
screw = cq.Workplane("YZ").workplane(offset=-5).center(0, screw_z).circle(screw_radius).extrude(150)
screw_head = cq.Workplane("YZ").workplane(offset=-20).center(0, screw_z).circle(9).extrude(15)

# Simulate threads with rings
ring = cq.Workplane("YZ").center(0, screw_z).circle(screw_radius + 0.5).extrude(1.5)
for i in range(25, 130, 3):
    screw = screw.union(ring.translate((i, 0, 0)))

# Handle
handle_rod = cq.Workplane("XZ").workplane(offset=-45).center(-12.5, screw_z).circle(3).extrude(90)
ball1 = cq.Workplane("XY").center(-12.5, -45).workplane(offset=screw_z).sphere(5)
ball2 = cq.Workplane("XY").center(-12.5, 45).workplane(offset=screw_z).sphere(5)

# Jaw Plates (Gripping faces)
plate1 = cq.Workplane("XY").box(4, 50, 20).translate((133, 0, base_height + 10))
plate2 = cq.Workplane("XY").box(4, 50, 20).translate((82, 0, base_height + 10))

# Assemble all components
result = (base
          .union(fixed_jaw)
          .union(movable_jaw)
          .union(front_block)
          .union(screw)
          .union(screw_head)
          .union(handle_rod)
          .union(ball1)
          .union(ball2)
          .union(plate1)
          .union(plate2))