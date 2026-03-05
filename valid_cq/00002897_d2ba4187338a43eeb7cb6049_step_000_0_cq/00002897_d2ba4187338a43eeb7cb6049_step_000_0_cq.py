import cadquery as cq

# Parametric dimensions
cylinder_radius = 10.0
cylinder_height = 40.0
block_size = 10.0  # Size of the rectangular protrusion
block_height = 10.0 # Height of the rectangular protrusion
spacing = 40.0     # Distance between the two main assemblies

# 1. Create the left object: A simple cylinder
left_cylinder = cq.Workplane("XY").circle(cylinder_radius).extrude(cylinder_height)

# 2. Create the right object: A cylinder with a rectangular block protrusion
# First, the main cylinder body (same as left)
right_cylinder_body = cq.Workplane("XY").circle(cylinder_radius).extrude(cylinder_height)

# Next, the rectangular block.
# We create it on the side. We need to position it correctly.
# It seems to stick out radially.
block = (
    cq.Workplane("XY")
    .center(cylinder_radius, 0) # Move center to the edge of the cylinder
    .rect(block_size, block_size, centered=False) # Create rectangle, uncentered to grow outwards
    .extrude(block_height)
    # Adjust position: center the Y of the block on the X-axis
    .translate((0, -block_size/2, 0))
)

# Combine the right cylinder and the block
right_assembly = right_cylinder_body.union(block)

# 3. Position the objects
# Move the left object to the left (negative X) and the right object to the right (positive X)
# or keep left at origin and move right. Let's move them apart symmetrically.
final_left = left_cylinder.translate((-spacing/2, 0, 0))
final_right = right_assembly.translate((spacing/2, 0, 0))

# 4. Combine into final result
result = final_left.union(final_right)