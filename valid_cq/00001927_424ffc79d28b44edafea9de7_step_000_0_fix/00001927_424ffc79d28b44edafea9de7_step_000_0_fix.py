import cadquery as cq

# Parameters
Rbase = 15
Rtop = 3
cyl_h = 5
cone_h = 100
nose_r = Rtop
fin_t = 2
fin_h = 30
fin_l = 20

# Main body: cylinder + conical section
body = (
    cq.Workplane("XY")
      .circle(Rbase)
      .extrude(cyl_h)
      .workplane(offset=cyl_h)
      .circle(Rbase)
      .workplane(offset=cyl_h + cone_h)
      .circle(Rtop)
      .loft()
)

# Nose hemisphere
sphere = cq.Workplane("XY").workplane(offset=cyl_h + cone_h).sphere(nose_r)
cut_box = (
    cq.Workplane("XY")
      .workplane(offset=cyl_h + cone_h - nose_r/2)
      .box(2*Rbase, 2*Rbase, nose_r)
)
nose = sphere.cut(cut_box)

# Combine body and nose
result = body.union(nose)

# Single fin profile on XZ plane
fin0 = (
    cq.Workplane("XZ")
      .transformed(offset=(Rbase + fin_l/2, 0, fin_h/2))
      .rect(fin_l, fin_h)
      .extrude(fin_t)
)

# Create four fins by rotating fin0 around Z
for angle in [0, 90, 180, 270]:
    result = result.union(fin0.rotate((0, 0, 0), (0, 0, 1), angle))