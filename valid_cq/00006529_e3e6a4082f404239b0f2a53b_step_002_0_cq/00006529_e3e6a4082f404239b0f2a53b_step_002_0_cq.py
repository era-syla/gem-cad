import cadquery as cq

# --- Parameters ---
cube_size = 50.0        # Length of the cube sides
sphere_radius = 24.0    # Radius of the hemispherical cutout (slightly less than half the cube size)
hole_diameter = 4.0     # Diameter of the small holes at the bottom
num_holes = 5           # Number of small holes in the pattern
hole_circle_radius = 10.0 # Radius of the circle on which the holes are placed
hole_depth = 15.0       # How deep the small holes go

# --- Geometry Construction ---

# 1. Create the base cube
base = cq.Workplane("XY").box(cube_size, cube_size, cube_size)

# 2. Create the spherical cutout
# We create a sphere and cut it from the top face.
# The sphere's center needs to be positioned correctly.
# If the cube is centered at (0,0,0) and height is cube_size, the top face is at Z = cube_size/2.
# We want the equator of the hemisphere to be exactly on the top face.
sphere_cutout = (
    cq.Workplane("XY")
    .workplane(offset=cube_size/2)  # Move to the top face
    .sphere(sphere_radius)
)

# Cut the sphere from the base
# Note: sphere() creates a solid centered at the current workplane origin.
# By default, it's a full sphere. When we cut, we remove the volume intersection.
result = base.cut(sphere_cutout)

# 3. Create the small holes inside the bowl
# We want these holes to be vertical (along Z).
# They are arranged in a circular pattern around the center.
# We need to start drilling from a plane that ensures we cut through the bottom of the bowl.
# A safe place to start is the top face of the cube, drilling downwards.

# Create a list of points for the hole locations
# We'll put one hole in the center, and others in a circle
hole_locations = [(0, 0)]  # Center hole
angle_step = 360.0 / (num_holes - 1)
import math

for i in range(num_holes - 1):
    angle = math.radians(i * angle_step)
    x = hole_circle_radius * math.cos(angle)
    y = hole_circle_radius * math.sin(angle)
    hole_locations.append((x, y))

# Drill the holes
result = (
    result.faces(">Z")      # Select top face
    .workplane()
    .pushPoints(hole_locations)
    .hole(hole_diameter) # hole() cuts through everything by default, or we can specify depth
)
# Note: simple hole() goes through the entire part. Looking at the image, 
# the holes seem to go down into the block. If they need to be blind, 
# we would use .blindHole(hole_depth). Assuming through-holes or deep blind holes 
# based on typical drainage or fixture designs. Let's make them deep enough to be visible but not necessarily through.
# Let's refine the hole creation to be blind holes starting from the top face, 
# ensuring they go deep enough relative to the bowl bottom.
# The bowl bottom is at z = (cube_size/2) - sphere_radius = 25 - 24 = 1mm from center.
# So drilling from the top (z=25) down 40mm ensures they are visible.

result = (
    base.cut(sphere_cutout) # Re-apply cut to fresh base variable logic
    .faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .hole(hole_diameter, depth=sphere_radius + 10.0) # Depth relative to the top face
)

# Let's do a pure clean parametric version
# Re-initializing result to ensure the script is self-contained and clean
result = (
    cq.Workplane("XY")
    .box(cube_size, cube_size, cube_size)
    # Cut the hemisphere
    .faces(">Z").workplane()
    .sphere(sphere_radius, combine='cut')
    # Cut the holes
    .faces(">Z").workplane()
    .pushPoints(hole_locations)
    .hole(hole_diameter, depth=sphere_radius + 15.0) 
)

# Export or visualization would happen here in a typical workflow
# show_object(result)