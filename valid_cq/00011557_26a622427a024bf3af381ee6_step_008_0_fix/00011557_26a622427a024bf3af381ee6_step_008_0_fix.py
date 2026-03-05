import cadquery as cq

# Define dimensions
diameter = 5
length1 = 50
length2 = 40
offset1 = 30
offset2 = 20

# Create the base tube
tube1 = cq.Workplane("XY").circle(diameter / 2).extrude(length1)

# Create the vertical tube
tube2 = cq.Workplane("XZ").workplane(offset1, length1).circle(diameter / 2).extrude(length2)

# Create the side tube
tube3 = cq.Workplane("XY").workplane(offset2).circle(diameter / 2).extrude(length2)

# Combine the tubes
result = tube1.union(tube2).union(tube3)