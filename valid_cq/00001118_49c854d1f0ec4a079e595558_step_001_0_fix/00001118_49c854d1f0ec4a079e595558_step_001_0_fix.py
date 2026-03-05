import cadquery as cq

# Parameters
shaft_d = 16
shaft_h = 30
flange_d = 40
flange_h = 6
fillet1 = 3
block_w = 25
block_d = 12
block_h = 5
fillet2 = 2
arch_r = 10
hole_r = 4

# Build shaft
result = cq.Workplane("XY").cylinder(shaft_h, shaft_d/2)

# Add flange
result = result.union(
    cq.Workplane("XY")
      .workplane(offset=shaft_h)
      .cylinder(flange_h, flange_d/2)
)

# Fillet the top edge of the flange
result = result.edges(">Z").fillet(fillet1)

# Add rectangular block on top of flange
result = result.faces(">Z").workplane().box(block_w, block_d, block_h)

# Fillet the vertical edges of the block
result = result.edges("|Z").fillet(fillet2)

# Add semicircular arch (as a half-cylinder extruded along Y)
offset1 = shaft_h + flange_h + block_h
arch = (
    cq.Workplane("XZ")
      .workplane(offset=offset1)
      .cylinder(block_d, arch_r, centered=True)
)
result = result.union(arch)

# Drill a hole through the arch
hole = (
    cq.Workplane("XZ")
      .workplane(offset=offset1 + arch_r)
      .cylinder(block_d + 2, hole_r, centered=True)
)
result = result.cut(hole)