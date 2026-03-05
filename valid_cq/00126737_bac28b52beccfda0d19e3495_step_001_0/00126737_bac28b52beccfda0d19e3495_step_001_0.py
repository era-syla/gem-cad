import cadquery as cq

# Parametric dimensions for the model
# Bottom-left block dimensions (longer block)
length1 = 60.0
width1 = 15.0
height1 = 15.0

# Top-right block dimensions (shorter block)
length2 = 30.0
width2 = 15.0
height2 = 15.0

# Offset position for the second block relative to the first
# These values determine the gap between the two floating objects
offset_x = 50.0
offset_y = 30.0
offset_z = 40.0

# Create the first block centered at the origin
# box() generates a box centered on the workplane center
block1 = cq.Workplane("XY").box(length1, width1, height1)

# Create the second block and translate it to the offset position
block2 = cq.Workplane("XY").box(length2, width2, height2).translate((offset_x, offset_y, offset_z))

# Combine the two disjoint solids into the final result
result = block1.union(block2)