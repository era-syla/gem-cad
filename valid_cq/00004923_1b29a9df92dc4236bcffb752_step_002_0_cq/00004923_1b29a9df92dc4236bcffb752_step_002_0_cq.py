import cadquery as cq

# Parametric dimensions
plate_width = 100.0  # Width of the square plate
plate_thickness = 5.0  # Thickness of the plate
num_bumps_x = 8  # Number of bumps along the X axis
num_bumps_y = 8  # Number of bumps along the Y axis
bump_diameter = 2.5  # Diameter of each bump
bump_height = 1.0  # Height of the spherical segment above the plate
padding = 10.0  # Distance from the edge to the center of the first/last bumps

# Calculations for grid spacing
# Effective area for bumps is width - 2 * padding
step_x = (plate_width - 2 * padding) / (num_bumps_x - 1)
step_y = (plate_width - 2 * padding) / (num_bumps_y - 1)

# Create the base plate
base_plate = cq.Workplane("XY").box(plate_width, plate_width, plate_thickness)

# Create the points for the bumps
# We need to generate a grid of points on the top surface
bump_points = []
start_x = -plate_width / 2 + padding
start_y = -plate_width / 2 + padding

for i in range(num_bumps_x):
    for j in range(num_bumps_y):
        x = start_x + i * step_x
        y = start_y + j * step_y
        bump_points.append((x, y))

# Create the bumps
# We select the top face, push the grid points, and create spheres
# To make them look like small bumps, we create a sphere and cut the bottom, or union a sphere
# A simpler approach in CQ for "bumps" on a surface is to cut spheres or add them.
# Given the image, they look like small spherical caps added to the surface.

# Let's create the bumps as a separate object and union them
# Or better, use Workplane features directly.

# Move to the top face
top_face = base_plate.faces(">Z").workplane()

# Place the points and create the bumps
# A sphere radius needs to be calculated based on the desired diameter and height
# if it's a spherical cap. However, usually these are just small hemispheres or partial spheres.
# Let's assume they are simple hemispheres or small spheres embedded slightly.
# For simplicity and visual match, we will create spheres centered on the face.
radius = bump_diameter / 2.0

# Using pushPoints and sphere to add material
result = (
    top_face
    .pushPoints(bump_points)
    .sphere(radius)
)

# Alternatively, if the bumps are meant to be separate small cylinders or cones, 
# sphere is the best approximation for the visual "rivet" or "nub" look in the image.
# The sphere command in the context of a workplane creates a sphere at each point 
# and combines it with the solid. By default, the center of the sphere is on the workplane.
# This creates a hemisphere sticking out (since the other half is inside the plate).