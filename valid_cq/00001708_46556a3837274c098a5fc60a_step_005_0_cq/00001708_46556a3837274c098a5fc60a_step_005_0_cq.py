import cadquery as cq

# Parameters for the cylinders
cylinder_radius = 20.0
cylinder_height = 100.0

# Distance between the centers of the cylinders
# To make them touch or overlap slightly, the offset needs to be <= 2 * radius
# Here we'll create a slight overlap to fuse them into a single object
offset_x = 30.0
offset_y = 15.0  # Creating a slight diagonal offset as seen in the perspective

# Create the first cylinder
c1 = cq.Workplane("XY").circle(cylinder_radius).extrude(cylinder_height)

# Create the second cylinder, offset from the first
c2 = cq.Workplane("XY").center(offset_x, offset_y).circle(cylinder_radius).extrude(cylinder_height)

# Union the two cylinders to create a single solid object
result = c1.union(c2)