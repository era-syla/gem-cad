import cadquery as cq

radius = 15
length = 50
fin_width = 3
fin_height = 10
fin_count = 12

# Create the main body
body = cq.Workplane("XY").sphere(radius).intersect(
    cq.Workplane("XY").cylinder(length, radius)
)

# Create a single fin
fin = (
    cq.Workplane("YZ")
    .moveTo(0, radius)
    .lineTo(fin_width / 2, radius + fin_height)
    .lineTo(-fin_width / 2, radius + fin_height)
    .close()
    .extrude(length)
)

# Create all fins using polarArray
fins = fin.rotate((0, 0, 0), (1, 0, 0), 90).faces("<Y").workplane(centerOption='CenterOfBoundBox').polarArray(radius, 0, 360, fin_count).each(lambda loc: fin.val().locate(loc))

# Combine body and fins
result = body.union(fins)