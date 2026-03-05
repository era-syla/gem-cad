import cadquery as cq

# Main block
main_block = cq.Workplane("XY").rect(20, 20).extrude(4)

# Smaller block
small_block = cq.Workplane("XY").rect(10, 10).extrude(2)

# Quarter cylinder
quarter_cylinder = (cq.Workplane("XY")
                    .center(20, 0)
                    .threePointArc((30, 10), (20, 20))
                    .lineTo(20, 0)
                    .close()
                    .extrude(10))

result = main_block.union(small_block).union(quarter_cylinder)