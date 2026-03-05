import cadquery as cq

# Parametric dimensions
top_cube_size = 10.0      # Size of the top cube
stem_width = 4.0          # Width of the connecting stem
stem_thickness = 4.0      # Thickness of the connecting stem (depth)
stem_length = 15.0        # Length of the connecting stem
sphere_radius = 5.0       # Radius of the bottom sphere

# 1. Create the Top Cube
# Positioned so its bottom face is at Z=stem_length + sphere_radius
# and centered on X and Y axes.
top_cube = (
    cq.Workplane("XY")
    .workplane(offset=stem_length + sphere_radius)
    .box(top_cube_size, top_cube_size, top_cube_size, centered=(True, True, False))
)

# 2. Create the Bottom Sphere
# Positioned at the origin (0,0,0) or slightly offset.
# Based on the image, the stem connects to the top of the sphere.
# Let's place the center of the sphere at (0,0,sphere_radius) relative to a base,
# or simply at (0,0,0) and build up.
# Let's assume the center of the sphere is at (0,0,0).
sphere = cq.Workplane("XY").sphere(sphere_radius)

# 3. Create the Connecting Stem
# This connects the top of the sphere to the bottom of the cube.
# The sphere top is at Z = sphere_radius.
# The cube bottom is at Z = sphere_radius + stem_length.
stem = (
    cq.Workplane("XY")
    .workplane(offset=0) # Start from the center of the sphere
    .rect(stem_width, stem_thickness)
    .extrude(stem_length + sphere_radius + top_cube_size/2) # Extrude up into the cube
    # Note: intersecting geometry is fine, we will union them.
    # To make it clean: starts at sphere center, goes up.
)

# However, looking closely at the image:
# The stem seems to be flush with one side of the cube or centered?
# It looks centered relative to the cube and the sphere.
# Let's reconstruct systematically from bottom up to ensure connectivity.

# Center of sphere at Z=0
sphere_center = cq.Vector(0, 0, 0)
bottom_sphere = cq.Workplane("XY").sphere(sphere_radius)

# Stem
# Starts inside the sphere and goes up to the cube.
# Let's make the stem start at Z=0 and go up to the bottom of the cube.
# Cube bottom Z = sphere_radius + stem_length (visible gap length)
# Actually, the stem length in the image is the distance between sphere and cube.
# Let's define `stem_gap` as the visible part.
stem_gap = 12.0
cube_z_bottom = sphere_radius * 0.8 + stem_gap # slight overlap with sphere

stem_height = cube_z_bottom  # From origin to bottom of cube
connecting_stem = (
    cq.Workplane("XY")
    .rect(stem_width, stem_width) # Assuming square cross-section for the stem
    .extrude(cube_z_bottom)
)

# Top Cube
# Sits on top of the stem.
top_block = (
    cq.Workplane("XY")
    .workplane(offset=cube_z_bottom)
    .box(top_cube_size, top_cube_size, top_cube_size, centered=(True, True, False))
)

# Combine everything
result = bottom_sphere.union(connecting_stem).union(top_block)

# Export the result for visualization (optional in script, but good for testing)
# cq.exporters.export(result, "model.step")