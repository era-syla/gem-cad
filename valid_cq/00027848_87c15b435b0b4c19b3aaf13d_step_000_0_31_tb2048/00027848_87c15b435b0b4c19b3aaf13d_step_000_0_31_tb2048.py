import cadquery as cq

# Handle
handle = cq.Workplane("XY").box(80, 15, 3).translate((-40, 0, 0))
handle = handle.edges("|Z and <X").fillet(3)

# Bottom tab with hole
tab1 = cq.Workplane("XY").box(15, 3, 10).translate((-20, -9, -5))
tab1 = tab1.faces("<Y").workplane(centerOption="CenterOfMass").hole(3)

# Side triangular tab with hole
tab2 = (cq.Workplane("XY")
        .moveTo(0, 0)
        .lineTo(15, 0)
        .lineTo(7.5, -10)
        .close()
        .extrude(3)
        .translate((-10, -7.5, 0)))
tab2 = tab2.faces(">Z").workplane(centerOption="CenterOfMass").hole(4)

# Mid section with 2 holes
mid = cq.Workplane("XY").box(25, 15, 5).translate((12.5, 0, 1))
mid = mid.faces(">Z").workplane().pushPoints([(5, 0), (15, 0)]).hole(5)

# Pivot section
pivot = cq.Workplane("XY").cylinder(3, 12).translate((30, 0, 1.5))
pin = cq.Workplane("XY").cylinder(15, 3).translate((30, 0, 9))
block_near_pin = cq.Workplane("XY").box(8, 8, 8).translate((36, 4, 5.5))

# Base body and vertical plate
base = cq.Workplane("XY").box(30, 20, 5).translate((45, 0, 0))
base_vertical = cq.Workplane("XY").box(30, 3, 20).translate((45, 8.5, -7.5))

# Cut slot in vertical plate
base_slot = cq.Workplane("XY").box(25, 5, 2).translate((45, 8.5, -5))
base_vertical = base_vertical.cut(base_slot)

# Hex bolt and pin below pivot
hex_bolt = cq.Workplane("XY").polygon(6, 8).extrude(3).translate((30, -10, -2))
bolt_pin = cq.Workplane("XY").cylinder(8, 2.5).translate((30, -10, -5))

# End block with hole
end_block = cq.Workplane("XY").box(8, 8, 8).translate((56, 6, 5.5))
end_block = end_block.faces(">X").workplane(centerOption="CenterOfMass").hole(2)

# Combine all parts
result = (handle
          .union(tab1)
          .union(tab2)
          .union(mid)
          .union(pivot)
          .union(pin)
          .union(block_near_pin)
          .union(base)
          .union(base_vertical)
          .union(hex_bolt)
          .union(bolt_pin)
          .union(end_block))