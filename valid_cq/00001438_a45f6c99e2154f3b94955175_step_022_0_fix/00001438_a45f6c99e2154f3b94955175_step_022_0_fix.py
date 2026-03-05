import cadquery as cq

# Parameters
L = 80             # total length of the block (X direction)
W = 12             # block thickness (Y direction)
Rb = 8             # block half-height (for rounded ends, Z direction)
block_height = 2 * Rb
hole_d = 6         # diameter of side lug holes
cyl_d_outer = 16   # outer diameter of central cylinder
cyl_d_hole = 8     # inner diameter of central hole
cyl_h = 20         # height of central cylinder
collar_thick = 3
collar_outer = 20

# Create the lug block with rounded ends in XZ plane, then extrude in Y
block = (
    cq.Workplane("XZ")
      .moveTo(-L/2 + Rb, 0)
      .lineTo( L/2 - Rb, 0)
      .threePointArc(( L/2,   Rb), ( L/2 - Rb, 2*Rb))
      .lineTo(-L/2 + Rb, 2*Rb)
      .threePointArc((-L/2,   Rb), (-L/2 + Rb, 0))
      .close()
      .extrude(W)             # extrude along +Y
      .translate((0, -W/2, 0))  # center thickness about Y=0
)

# Cut the two side lug holes through the block (along Y)
block = (
    block.faces(">Y")
         .workplane()
         .pushPoints([(-L/2 + Rb, Rb), (L/2 - Rb, Rb)])
         .hole(hole_d)
)

# Create the central cylinder
cylinder = (
    cq.Workplane("XY")
      .circle(cyl_d_outer/2)
      .extrude(cyl_h)
      .translate((0, 0, block_height))
)

# Create the collar ring at the base of the cylinder
collar = (
    cq.Workplane("XY")
      .circle(collar_outer/2)
      .circle(cyl_d_outer/2)
      .extrude(collar_thick)
      .translate((0, 0, block_height))
)

# Combine block, cylinder, and collar
result = block.union(cylinder).union(collar)

# Cut out the central through-hole in the cylinder and block
cutter = (
    cq.Workplane("XY")
      .circle(cyl_d_hole/2)
      .extrude(block_height + cyl_h + 2)  # ensure it cuts completely
      .translate((0, 0, -1))
)

result = result.cut(cutter)