import cadquery as cq

# Parameters
R = 10               # Radius of end circles
holeD = 6            # Diameter of holes
c2c = 50             # Center-to-center distance between end circles
thickness = 5        # Plate thickness

# Intermediate calculation
rect_len = c2c - 2 * R

# Create center rectangle
base = cq.Workplane("XY").rect(rect_len, 2 * R).extrude(thickness)

# Create end circles
circle1 = cq.Workplane("XY").center(c2c/2, 0).circle(R).extrude(thickness)
circle2 = cq.Workplane("XY").center(-c2c/2, 0).circle(R).extrude(thickness)

# Fuse all bodies
result = base.union(circle1).union(circle2)

# Drill holes through the plate
result = result.faces(">Z").workplane().pushPoints(
    [( c2c/2, 0), (-c2c/2, 0)]
).hole(holeD)