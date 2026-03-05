import cadquery as cq

# Define the main block dimensions
main_block = cq.Workplane("XY").rect(50, 5).extrude(100)

# Add a rounded top feature
rounded_top = (
    cq.Workplane("XY")
    .center(0, 100)
    .threePointArc((25, 120), (-25, 120))
    .close()
    .extrude(5)
)

# Union the main block and the rounded top
result = main_block.union(rounded_top)

# Create a pivot hole at the bottom
result = result.faces(">Z").workplane().center(-25, -50).hole(3)

# Add a side support
support = cq.Workplane("YZ").move(0, -2.5).rect(5, 20).extrude(20)
result = result.union(support)