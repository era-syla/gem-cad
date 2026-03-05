import cadquery as cq

# Create the main sphere
sphere = cq.Workplane("XY").sphere(10)

# Create cutouts on the sphere
cutout = cq.Workplane("XY").cylinder(10, 15).rotate((0, 0, 0), (0, 1, 0), 90).translate((10, 0, 0))
sphere = sphere.cut(cutout)

# Create fins
fin = cq.Workplane("XY").box(5, 20, 0.5).translate((7.5, 0, 0))
fin1 = fin.rotate((0, 0, 0), (0, 0, 1), 30)
fin2 = fin.rotate((0, 0, 0), (0, 0, 1), -30)

# Assemble all parts
result = sphere.union(fin1).union(fin2)