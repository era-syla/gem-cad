import cadquery as cq

# Parameters
sphere_radius = 5.0
strut_width = 2.0
spacing = 15.0  # Center-to-center distance between spheres
grid_size = 3   # 3x3x3 grid

# Create a single sphere
sphere = cq.Workplane("XY").sphere(sphere_radius)

# Create the grid of spheres
spheres = (
    cq.Workplane("XY")
    .rarray(spacing, spacing, grid_size, grid_size, True)
    .eachpoint(lambda loc: sphere.val().located(loc))
)

# Extrude the spheres in Z to create the 3D grid of spheres
# Since rarray creates a 2D grid, we need to stack them or iterate in Z
# A cleaner approach in CadQuery for a 3D lattice is to create lists of points
points = []
for x in range(grid_size):
    for y in range(grid_size):
        for z in range(grid_size):
            # Centering the grid around the origin
            px = (x - (grid_size - 1) / 2) * spacing
            py = (y - (grid_size - 1) / 2) * spacing
            pz = (z - (grid_size - 1) / 2) * spacing
            points.append((px, py, pz))

# Create the full assembly of spheres at once
all_spheres = cq.Workplane("XY").pushPoints(points).sphere(sphere_radius)

# Create the struts
# We need struts in X, Y, and Z directions connecting the spheres

struts = cq.Workplane("XY")

# X-direction struts
# There are (grid_size-1) gaps in X, grid_size in Y, grid_size in Z
for x in range(grid_size - 1):
    for y in range(grid_size):
        for z in range(grid_size):
            # Calculate center position for the strut
            px = ((x + 0.5) - (grid_size - 1) / 2) * spacing
            py = (y - (grid_size - 1) / 2) * spacing
            pz = (z - (grid_size - 1) / 2) * spacing
            
            # Create a box for the strut
            # Length is spacing, width/height is strut_width
            strut = (
                cq.Workplane("XY")
                .center(px, py)
                .workplane(offset=pz - strut_width/2)
                .box(spacing, strut_width, strut_width)
            )
            struts = struts.union(strut)

# Y-direction struts
# There are grid_size in X, (grid_size-1) gaps in Y, grid_size in Z
for x in range(grid_size):
    for y in range(grid_size - 1):
        for z in range(grid_size):
            px = (x - (grid_size - 1) / 2) * spacing
            py = ((y + 0.5) - (grid_size - 1) / 2) * spacing
            pz = (z - (grid_size - 1) / 2) * spacing
            
            strut = (
                cq.Workplane("XY")
                .center(px, py)
                .workplane(offset=pz - strut_width/2)
                .box(strut_width, spacing, strut_width)
            )
            struts = struts.union(strut)

# Z-direction struts
# There are grid_size in X, grid_size in Y, (grid_size-1) gaps in Z
for x in range(grid_size):
    for y in range(grid_size):
        for z in range(grid_size - 1):
            px = (x - (grid_size - 1) / 2) * spacing
            py = (y - (grid_size - 1) / 2) * spacing
            pz = ((z + 0.5) - (grid_size - 1) / 2) * spacing
            
            strut = (
                cq.Workplane("XY")
                .center(px, py)
                .workplane(offset=pz - spacing/2)
                .box(strut_width, strut_width, spacing)
            )
            struts = struts.union(strut)

# Combine spheres and struts
result = all_spheres.union(struts)