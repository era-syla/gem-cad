import cadquery as cq

R_blob = 20
dist = 50
thickness = 6
hole_r = 12
pocket_r = 8
pocket_d = 2
fillet_out = 2
fillet_in = 1

c1 = cq.Workplane("XY").transformed(offset=(-dist/2, 0, 0)).circle(R_blob).extrude(thickness)
c2 = cq.Workplane("XY").transformed(offset=( dist/2, 0, 0)).circle(R_blob).extrude(thickness)
result = c1.union(c2)

# central through hole
result = result.cut(
    cq.Workplane("XY")
      .circle(hole_r)
      .extrude(thickness + 1)
)

# shallow pocket on right lobe top
result = result.cut(
    cq.Workplane("XY")
      .transformed(offset=(dist/2, 0, thickness))
      .circle(pocket_r)
      .extrude(-pocket_d)
)

# outer vertical edge fillets
result = result.edges("|Z").fillet(fillet_out)
# top horizontal edge fillets
result = result.edges(">Z").fillet(fillet_in)