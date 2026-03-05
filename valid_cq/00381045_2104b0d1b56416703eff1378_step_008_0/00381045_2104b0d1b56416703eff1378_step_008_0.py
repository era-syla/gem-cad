import cadquery as cq

# Parameters for the spheres
# Radii of the four spheres in increasing order
radii = [2.0, 3.5, 5.0, 6.5]
# Distance between the centers of the spheres along the axis
spacing = 20.0

# Create the first sphere (smallest) at the origin
result = cq.Workplane("XY").sphere(radii[0])

# Iterate through the remaining radii to create and union the other spheres
for i in range(1, len(radii)):
    # Calculate the position along the X-axis
    x_pos = i * spacing
    
    # Create the next sphere at the calculated offset
    # We use a new Workplane for each to define absolute position easily
    next_sphere = cq.Workplane("XY").center(x_pos, 0).sphere(radii[i])
    
    # Union the new sphere with the existing geometry
    result = result.union(next_sphere)

# The 'result' variable now contains the four disjoint spheres as a single compound object