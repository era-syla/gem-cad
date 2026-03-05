import cadquery as cq

# Parameters
length = 200.0     # total length of the rail
width = 10.0       # rail width
thickness = 5.0    # rail thickness
hole_dia = 3.0     # diameter of the holes
hole_spacing = 10.0  # center-to-center spacing between holes

# Compute number of holes along the length
num_holes = int(length / hole_spacing) + 1

# Create the base rail
result = cq.Workplane("XY").box(length, width, thickness, centered=(True, True, False))

# Generate hole positions along the top face
x_coords = [(-length/2 + i * hole_spacing) for i in range(num_holes)]
points = [(x, 0) for x in x_coords]

# Drill the holes through the thickness
result = result.faces(">Z").workplane().pushPoints(points).hole(hole_dia)

# 'result' now contains the final solid
result