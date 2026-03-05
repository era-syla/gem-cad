import cadquery as cq

# Parametric dimensions
main_cube_size = 50.0  # Size of the large upper cube
cutout_radius = 25.0   # Radius of the cylindrical cutout
cutout_depth = 50.0    # Depth of the cutout (should be >= main_cube_size)
lower_block_width = 25.0 # Width of the lower block
lower_block_depth = 25.0 # Depth of the lower block
lower_block_height = 30.0 # Height of the lower block extending downwards

# 1. Create the main upper cube
# Centered on XY plane, sitting on Z=0 initially
main_body = cq.Workplane("XY").box(main_cube_size, main_cube_size, main_cube_size)

# 2. Create the negative shape (cylinder) to cut the corner
# We need a cylinder that intersects one corner.
# Let's target the corner at (-x, -y) relative to the center.
# The cylinder axis needs to be along the Y-axis (based on the curved profile on the front face).
# Actually, looking at the image, the curve is on the bottom edge.
# It looks like a "fillet" but huge, or simply a subtractive cylinder.
# Let's align it such that a cylindrical void is removed from the bottom-left corner.

# Create a cylinder for the cutout
# The cylinder is oriented along the Y axis.
cutout = (
    cq.Workplane("XZ")
    .cylinder(cutout_radius, main_cube_size * 2) # Extra length for clean cut
    .translate((-main_cube_size/2, -main_cube_size/2, 0)) # Position at bottom-left corner
)

# However, looking closer at the image, it's not just a cut.
# There is a lower block that seems to share the curvature.
# It looks like the operation is:
# 1. Start with a large cube.
# 2. Add a smaller block underneath one corner.
# 3. Apply a large fillet to the internal corner where they meet?
# OR
# 1. Start with the large cube.
# 2. Subtract a cylinder from the bottom corner.
# 3. Create a mating part that fits into that cylindrical cut but is a block with a rounded top.

# Let's try a boolean approach which is often robust for this shape.
# Shape analysis:
# Part A: Large Cube.
# Part B: Smaller rectangular prism attached to the bottom of Part A.
# The connection interface is curved. The bottom of Part A has a concave cylindrical cut. The top of Part B has a convex cylindrical surface.

# Let's refine the strategy:
# 1. Create the large cube.
# 2. Cut a cylindrical chunk out of the bottom-left corner (viewed from front).
# 3. Create a smaller block.
# 4. Intersect the smaller block with a cylinder to give it a rounded top.
# 5. Position the smaller block under the large cube.

# Alternative (easier) strategy:
# The shape looks like two blocks.
# Block 1 (Main): Cube with a cylindrical void at the bottom corner.
# Block 2 (Leg): A rectangular block that has a matching cylindrical top surface.

# Let's build the Main Cube with the cut:
main_cube = cq.Workplane("XY").box(main_cube_size, main_cube_size, main_cube_size)

# We want the cut on the bottom (-Z) face, on the corner.
# Let's create a cutter cylinder along the Y axis.
cutter = (
    cq.Workplane("XZ")
    .workplane(offset=0) # Center of the cube in Y
    .circle(cutout_radius)
    .extrude(main_cube_size + 10, both=True) # Extrude along Y
    .translate((-main_cube_size/2, -main_cube_size/2, 0)) # Move to bottom-left corner
)

# Apply the cut to the main cube
upper_part = main_cube.cut(cutter)

# Now create the lower leg part.
# It is a rectangular block, but its top face is cylindrical to match the cut.
# We can make a cylinder and intersect it with a box.

# Create the cylinder that forms the top of the leg (same size/pos as cutter)
leg_base_cylinder = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .circle(cutout_radius)
    .extrude(lower_block_depth, both=True) # Extrude along Y
    .translate((-main_cube_size/2, -main_cube_size/2, 0))
)

# Create the rectangular prism for the leg body
# It sits below the center of the cylinder axis.
# Width = cutout_radius (radius wide), Depth = lower_block_depth
# Height needs to extend downwards.
leg_box = (
    cq.Workplane("XY")
    .box(cutout_radius, lower_block_depth, lower_block_height + cutout_radius)
    .translate((-main_cube_size/2 - cutout_radius/2 + cutout_radius/2, 
                0, 
                -main_cube_size/2 - (lower_block_height + cutout_radius)/2))
    # Adjust X: The cylinder is centered at -main_cube_size/2. The leg box should align with the vertical edge.
    # The image shows the leg is flush with the left face of the cube.
    # Cube left face is at x = -main_cube_size/2.
    # Leg center x should be -main_cube_size/2 + width/2 if it is flush.
    # But the cylinder center is exactly at the corner (-main_cube_size/2, -main_cube_size/2).
    # This implies the leg is the quarter-cylinder quadrant under the main block, extended down.
)

# Let's simplify the construction logic based on the visual "Mate".
# The visual shows a "corner" fillet style interaction.

# Revised Construction Plan:
# 1. Create Main Cube.
# 2. Create the "Leg" block roughly in position.
# 3. Create a cylinder solid representing the interface curve.
# 4. Subtract the cylinder from the Main Cube.
# 5. Intersect the Leg block with the cylinder (or simply model the leg as a box + fillet, but the curve matches the subtraction).

# Let's execute the "Cut and Keep" method.

# 1. Main Cube
cube = cq.Workplane("XY").box(main_cube_size, main_cube_size, main_cube_size)

# 2. Define the axis of the cylinder. 
# It runs along Y.
# Center is at the bottom-left edge of the cube (X=-25, Z=-25).
cyl_x = -main_cube_size / 2
cyl_z = -main_cube_size / 2

# 3. Create the subtraction tool (The cylinder)
tool = (
    cq.Workplane("XZ")
    .center(cyl_x, cyl_z)
    .circle(cutout_radius)
    .extrude(main_cube_size * 2, both=True) # Make it long enough
)

# 4. Create the solid for the lower leg
# It needs to look like a block with a rounded top.
# We can model this by making a box and intersecting it with the same cylinder geometry, 
# then moving it down or extruding it down.
# Or simpler: Create a box, fillet top edge? No, the radius is huge.
# Better: Create the shape in 2D profile and extrude.

# Profile of the leg on XZ plane:
# A rectangle from (Bottom) to (Cylinder Center), intersected by the circle.
# Let's make the leg purely by extruding a specific sketch.
leg_sketch = (
    cq.Workplane("XZ")
    .hLine(cutout_radius)     # Top horizontal (from center) - actually we need the arc
    .vLine(-lower_block_height) # Down
    .hLine(-cutout_radius)    # Back left
    .close()                  # Up to close
)
# Wait, that's a rectangle. We need the top to be the arc.

leg = (
    cq.Workplane("XZ")
    .workplane(offset= -lower_block_depth/2) # Start Y plane
    .moveTo(cyl_x, cyl_z - lower_block_height) # Bottom Left of leg
    .lineTo(cyl_x + cutout_radius, cyl_z - lower_block_height) # Bottom Right
    .lineTo(cyl_x + cutout_radius, cyl_z) # Top Right (at cylinder centerline height)
    # Now arc back to Top Left (cylinder center)
    .radiusArc((cyl_x, cyl_z), -cutout_radius) 
    .close()
    .extrude(lower_block_depth)
)

# The leg as generated above is flush with the back of the cut. 
# In the image, the leg is centered relative to the cutout width or flush with the front?
# The image shows the leg has a finite depth (Y), likely smaller than the main cube.
# The `extrude` creates it in positive normal direction.
# If we started at -lower_block_depth/2, it goes to +lower_block_depth/2. Centered on Y=0.
# The main cube is centered on Y=0. This looks correct.

# 5. Apply the cut to the main cube
final_upper = cube.cut(tool)

# 6. Combine
result = final_upper.union(leg)