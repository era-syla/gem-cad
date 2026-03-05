import cadquery as cq

# Create the two rail bars
rail1 = (
    cq.Workplane("YZ")
    .rect(4, 4)
    .extrude(200)
    .translate((0, -6, 2))
)
rail2 = rail1.translate((0, 12, 0))

# Create the slider body that rides on the rails
slider = (
    cq.Workplane("YZ")
    .rect(20, 8)
    .extrude(30)
    .translate((80, 0, 4))
)

# Add a small fin on top of the slider
fin = (
    cq.Workplane("YZ")
    .rect(2, 10)
    .extrude(30)
    .translate((80, -11, 8))
)

# Create the sliding rod
rod = (
    cq.Workplane("YZ")
    .circle(1)
    .extrude(150)
    .translate((80, 0, 4))
)

# Add a small tip at the end of the rod
tip = (
    cq.Workplane("YZ")
    .circle(0.6)
    .extrude(10)
    .translate((230, 0, 4))
)

# Combine all parts into the final result
result = rail1.union(rail2).union(slider).union(fin).union(rod).union(tip)