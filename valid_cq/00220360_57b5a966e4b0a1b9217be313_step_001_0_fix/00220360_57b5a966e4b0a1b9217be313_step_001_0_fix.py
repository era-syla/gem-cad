import cadquery as cq

# parameters
cyl_d = 10
cyl_r = cyl_d/2
cyl_h = 6
base_t = 3
wall_h = 10
wall_x = 5
spacing = 20
hole_d = 4

length = 2*spacing + 2*cyl_r
width = cyl_d

centers = [-spacing, 0, spacing]

# PartA: U-shaped half with walls and cylinders
partA = cq.Workplane("XY").rect(length, width).extrude(base_t)
for x in (centers[0], centers[-1]):
    partA = partA.faces(">Z").workplane(origin=(x, 0)).rect(wall_x, width).extrude(wall_h)
for x in (centers[0], centers[-1]):
    partA = partA.faces(">Z").workplane(origin=(x, 0)).hole(hole_d, wall_h)
partA = partA.faces(">Z").workplane().pushPoints([(x, 0) for x in centers]).circle(cyl_r).extrude(cyl_h)

# PartB: flat half with cylinders only
partB = cq.Workplane("XY").rect(length, width).extrude(base_t)
partB = partB.faces(">Z").workplane().pushPoints([(x, 0) for x in centers]).circle(cyl_r).extrude(cyl_h)

# offset PartB in Y so they don't overlap
partB = partB.translate((0, width + 10, 0))

# combine into a single result
result = partA.union(partB)