import cadquery as cq

# Parametric dimensions
box_size = 10.0  # Size of the cube sides
dimple_radius = 2.5  # Radius of the sphere cut
dimple_depth = 1.0   # How deep the sphere cuts into the cube (implicitly controlled by sphere position)

# Alternatively, we can define the sphere radius and offset it.
# Looking at the image, the dimple diameter is roughly 1/3 to 1/4 of the box width.
# Let's assume box is 10x10x10.
# The hole diameter looks like roughly 3-4 units. So radius 1.5-2.0.
# The cut looks spherical.

# Revised Parameters
cube_width = 10.0
cube_height = 10.0
cube_depth = 10.0
sphere_radius = 2.5 # Radius of the cutting sphere

# Create the base cube
# Centered on X and Y, sitting on Z=0 or centered on Z. Let's center everything for simplicity.
base = cq.Workplane("XY").box(cube_width, cube_depth, cube_height)

# Create the spherical cutter
# We need to position a sphere such that it intersects the top face.
# If the box is centered at (0,0,0) with height 10, the top face is at Z=5.
# We want the cut to be centered on the top face.
# Let's say we want a specific diameter for the opening on top.
# Or we can just subtract a sphere located slightly above the top face.

# Strategy:
# 1. Create a box.
# 2. Select the top face.
# 3. Create a sphere object.
# 4. Cut the sphere from the box.

# Let's position the sphere center.
# Top face is at Z = cube_height / 2.
# We want the bottom of the sphere to penetrate the box.
# Center of sphere needs to be at (0, 0, Z_pos).
# If Z_pos = (cube_height/2), the sphere is exactly half-submerged (hemisphere cut).
# The image shows a shallow cut, less than a hemisphere.
# So the center of the sphere must be higher than the top face.
# Let's define the cut depth.
cut_depth = 1.5
# Sphere center Z = (cube_height / 2) + sphere_radius - cut_depth
sphere_center_z = (cube_height / 2.0) + sphere_radius - cut_depth

# Create the solid sphere for the cut
sphere_cutter = cq.Solid.makeSphere(sphere_radius, cq.Vector(0, 0, sphere_center_z))

# Perform the cut
result = base.cut(sphere_cutter)

# Alternatively, using Workplane methods purely:
# result = (
#     cq.Workplane("XY")
#     .box(cube_width, cube_depth, cube_height)
#     .faces(">Z")
#     .workplane()
#     .sphere(sphere_radius) # This creates a sphere and usually unions or cuts depending on context, but .sphere() adds material in standard CQ API usually or replaces.
# )

# The explicit cut operation with a Solid object is often more reliable for specific placement like this.
# Let's re-verify the dimensions.
# If box is 10, radius 2.5, depth 1.5.
# Center at 5 + 2.5 - 1.5 = 6.0.
# Lowest point of sphere at 6.0 - 2.5 = 3.5. Top of box at 5.0. 
# Wait, lowest point is CenterZ - Radius. 6.0 - 2.5 = 3.5.
# This means the sphere penetrates 1.5 units into the box (from 5.0 down to 3.5).
# This matches the "shallow bowl" look.

# Final Code Construction
result = (
    cq.Workplane("XY")
    .box(cube_width, cube_depth, cube_height)
    .cut(
        cq.Solid.makeSphere(sphere_radius, cq.Vector(0, 0, sphere_center_z))
    )
)