import cadquery as cq

# Parameters
base_l = 150
base_w = 64
base_h = 25
anvil_x = 45
ram_x = 45
pinion_x = 26
pinion_z = 125

# Base Plate
base = (cq.Workplane("XY")
        .workplane(offset=base_h/2)
        .box(base_l, base_w, base_h)
        .edges("|Z").fillet(15)
        .edges(">Z").fillet(3))

# Base relief cut
base = base.cut(cq.Workplane("XY")
                .workplane(offset=3)
                .box(base_l-40, base_w-25, 6))

# Base mounting holes and anvil clearance hole
base = base.faces(">Z").workplane().pushPoints([(-55, 20), (-55, -20)]).hole(10)
base = base.faces(">Z").workplane().center(anvil_x, 0).hole(12)

# Anvil Pad
pad_h = 6
pad = (cq.Workplane("XY")
       .workplane(offset=base_h + pad_h/2 - 1)
       .center(anvil_x, 0)
       .cylinder(pad_h + 2, 24)
       .edges(">Z").fillet(1))

# Anvil Plate
anvil_h = 14
anvil_r = 30
anvil = (cq.Workplane("XY")
         .workplane(offset=base_h + pad_h + anvil_h/2 - 0.5)
         .center(anvil_x, 0)
         .cylinder(anvil_h + 1, anvil_r)
         .edges(">Z").chamfer(1))

anvil = anvil.faces(">Z").workplane().hole(8)

# Anvil Slots
for angle, width in [(0, 6), (90, 10), (180, 16), (270, 8)]:
    slot = (cq.Workplane("XY")
            .workplane(offset=base_h + pad_h + anvil_h + 1)
            .center(anvil_x, 0)
            .transformed(rotate=cq.Vector(0, 0, angle))
            .center(anvil_r, 0)
            .rect(20, width)
            .extrude(-anvil_h - 4))
    anvil = anvil.cut(slot)

# Frame Core
sk = (cq.Workplane("XZ")
      .moveTo(-65, base_h - 5)
      .lineTo(-5, base_h - 5)
      .threePointArc((15, 80), (pinion_x, pinion_z))
      .lineTo(-10, 150)
      .threePointArc((-40, 80), (-65, base_h - 5))
      .close())
frame = sk.extrude(16, both=True)

# Pinion Boss
pboss = cq.Workplane("XZ").center(pinion_x, pinion_z).cylinder(44, 20)
frame = frame.union(pboss)

# Ram Boss
rboss = cq.Workplane("XY").workplane(offset=pinion_z).center(ram_x, 0).box(28, 28, 60)
frame = frame.union(rboss)

# Frame Side Pockets (Cast Relief)
psk = (cq.Workplane("XZ")
       .moveTo(-55, base_h + 8)
       .lineTo(-10, base_h + 8)
       .threePointArc((10, 80), (14, 110))
       .lineTo(-5, 135)
       .threePointArc((-30, 80), (-55, base_h + 8))
       .close())

pocket = psk.extrude(20)
frame = frame.cut(pocket.translate((0, 4, 0)))
frame = frame.cut(pocket.mirror("XZ").translate((0, -4, 0)))

# Frame Ram and Pinion Holes
frame = frame.cut(cq.Workplane("XY")
                  .workplane(offset=160)
                  .center(ram_x, 0)
                  .rect(16.5, 16.5)
                  .extrude(-70))

frame = frame.cut(cq.Workplane("XZ")
                  .center(pinion_x, pinion_z)
                  .cylinder(50, 8.5))

# Vertical Ram
ram_len = 120
ram = (cq.Workplane("XY")
       .workplane(offset=pinion_z)
       .center(ram_x, 0)
       .box(16, 16, ram_len)
       .faces(">Z").chamfer(1.5)
       .faces("<Z").chamfer(1.5))

# Rack Teeth cut into Ram
for z in range(95, 145, 4):
    cutter = (cq.Workplane("XZ")
              .workplane(offset=0)
              .moveTo(38, z)
              .lineTo(34, z - 2)
              .lineTo(34, z + 2)
              .close()
              .extrude(20, both=True))
    ram = ram.cut(cutter)

# Pinion Shaft
shaft = cq.Workplane("XZ").center(pinion_x, pinion_z).cylinder(42, 8)

# Left Hub
hub_l = cq.Workplane("XZ").workplane(offset=-27).center(pinion_x, pinion_z).cylinder(10, 14)
shaft = shaft.union(hub_l)

# Right Cap
hub_r = cq.Workplane("XZ").workplane(offset=24).center(pinion_x, pinion_z).cylinder(4, 12)
hub_r = hub_r.cut(cq.Workplane("XZ").workplane(offset=26).center(pinion_x, pinion_z).cylinder(3, 6))
shaft = shaft.union(hub_r)

# Handle Lever
hp1_x, hp1_z = pinion_x + 15, pinion_z - 6
hp2_x, hp2_z = pinion_x - 110, pinion_z + 44

handle_path = (cq.Workplane("XZ")
        .workplane(offset=-27)
        .moveTo(hp1_x, hp1_z)
        .lineTo(hp2_x, hp2_z))
handle = (cq.Workplane("YZ")
        .workplane(offset=hp1_x)
        .center(-27, hp1_z)
        .circle(4)
        .sweep(handle_path))

knob_1 = cq.Workplane("XZ").workplane(offset=-27).center(hp1_x, hp1_z).sphere(6)
knob_2 = cq.Workplane("XZ").workplane(offset=-27).center(hp2_x, hp2_z).sphere(7)

# Final Assembly Union
result = (base
          .union(pad)
          .union(anvil)
          .union(frame)
          .union(ram)
          .union(shaft)
          .union(handle)
          .union(knob_1)
          .union(knob_2))