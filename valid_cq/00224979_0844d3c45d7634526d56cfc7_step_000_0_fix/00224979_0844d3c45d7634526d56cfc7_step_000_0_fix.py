import cadquery as cq

# Base cylinder
base = cq.Workplane("XY").circle(10).extrude(5)

# Vertical posts
post = (
    cq.Workplane("XY")
    .workplane(offset=5)
    .rect(2, 20)
    .extrude(40)
    .translate((8, 0, 0))
)

posts = (
    post
    .union(post.mirror("YZ"))
)

# Upper cylinder/linkage
upper_cylinder = (
    cq.Workplane("XY")
    .workplane(offset=45)
    .circle(5)
    .extrude(10)
)

# Linkage holes
linkage = (
    upper_cylinder.faces(">Z")
    .workplane()
    .rarray(8, 1, 2, 1, center=True)
    .circle(1)
    .cutThruAll()
)

result = base.union(posts).union(linkage)