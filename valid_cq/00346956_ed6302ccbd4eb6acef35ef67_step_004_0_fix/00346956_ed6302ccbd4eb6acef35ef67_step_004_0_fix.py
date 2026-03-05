import cadquery as cq

# Parameters for the top piece
radius1 = 10
length1 = 20

# Create a full sphere for the top piece
sphere1 = cq.Workplane("YZ").sphere(radius1)
# Create a box that covers the positive X half‐space for top piece
box1 = cq.Workplane("YZ").box(length1 + 2*radius1, 2*radius1, 2*radius1).translate(((length1 + 2*radius1)/2, 0, 0))
# Cut away the positive‐X half of the sphere to get a hemisphere
hemisphere1 = sphere1.cut(box1)
# Create the matching cylinder
cyl1 = cq.Workplane("YZ").circle(radius1).extrude(length1)
# Union hemisphere and cylinder
top = hemisphere1.union(cyl1)

# Parameters for the bottom piece
radius2 = 15
length2 = 30
gap = 5  # vertical spacing between the two pieces

# Create a full sphere for the bottom piece
sphere2 = cq.Workplane("YZ").sphere(radius2)
# Create a box that covers the positive X half‐space for bottom piece
box2 = cq.Workplane("YZ").box(length2 + 2*radius2, 2*radius2, 2*radius2).translate(((length2 + 2*radius2)/2, 0, 0))
# Cut away the positive‐X half of the sphere to get a hemisphere
hemisphere2 = sphere2.cut(box2)
# Create the matching cylinder
cyl2 = cq.Workplane("YZ").circle(radius2).extrude(length2)
# Union hemisphere and cylinder, then translate downwards
bottom = hemisphere2.union(cyl2).translate((0, -(radius1 + radius2 + gap), 0))

# Combine both pieces into the final result
result = top.union(bottom)