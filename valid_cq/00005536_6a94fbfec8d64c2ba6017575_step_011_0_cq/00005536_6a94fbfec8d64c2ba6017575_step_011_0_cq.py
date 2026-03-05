import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions based on visual estimation
total_height = 100.0  # Height of the main body
body_width = 80.0     # Width of the rectangular section
body_depth = 60.0     # Depth of the rectangular section
cyl_radius = 40.0     # Radius of the cylindrical front part

# Top Cap dimensions
cap_thickness = 5.0
cap_overhang = 5.0    # How much the cap extends past the body
cap_radius = cyl_radius + cap_overhang

# Side Boss (Button) dimensions
boss_radius = 12.0
boss_thickness = 5.0
boss_height_ratio = 0.7 # Position relative to height (from bottom)

# --- Geometry Construction ---

# 1. Create the Rectangular Body (Back part)
# We position the center such that the front face aligns with the cylinder's diameter
rect_body = cq.Workplane("XY").box(body_width, body_depth, total_height, centered=(True, False, False))

# 2. Create the Cylindrical Body (Front part)
# Positioned at the origin, extending upwards.
# The rectangle is shifted back by half its depth to merge seamlessly.
cyl_body = cq.Workplane("XY").circle(cyl_radius).extrude(total_height)

# Move the rectangular body so its front face touches the cylinder's diameter line (Y=0)
# The box is created with centered=(True, False, False), so it starts at Y=0 and goes +Y or -Y?
# Let's adjust: We want the cylinder at the "front" and the block at the "back".
# Let's assume the cylinder is centered at (0,0).
# The block should tangent the cylinder. 
# Looking at the image, the block seems to intersect the cylinder, creating a "keyhole" shape profile.
# Let's reconstruct the profile instead for a cleaner join.

# Alternative Profile Approach:
# Create a sketch on the XY plane that combines the circle and the rectangle.
profile = (
    cq.Workplane("XY")
    # Draw the rectangle part. 
    # Let's assume the cylinder center is (0,0).
    # The flat back face is at some +Y distance.
    # The image shows the block tangent to the cylinder's sides? No, it looks like the block's width equals the cylinder diameter.
    # So the block width = 2 * cyl_radius.
    .moveTo(-cyl_radius, 0)
    .lineTo(-cyl_radius, -body_depth)
    .lineTo(cyl_radius, -body_depth)
    .lineTo(cyl_radius, 0)
    # Close with the front arc of the cylinder
    .threePointArc((0, cyl_radius), (-cyl_radius, 0))
    .close()
)

# Re-evaluating the image:
# The rectangular part is distinct. It looks like a cylinder intersecting a square prism.
# The cylinder is centered at the front. The block is at the back.
# Let's stick to boolean unions for clarity.

# Cylinder part
cylinder = cq.Workplane("XY").circle(cyl_radius).extrude(total_height)

# Block part
# Width matches cylinder diameter (approx)
# Positioned behind the cylinder center.
block = (
    cq.Workplane("XY")
    .center(0, -body_depth/2) # Move center back
    .box(cyl_radius * 2, body_depth, total_height)
)

# Union the main body
main_body = cylinder.union(block)

# 3. Create the Top Cap
# It's a larger cylinder sitting on top.
# The image shows the cap is concentric with the cylindrical front part.
cap = (
    cq.Workplane("XY")
    .workplane(offset=total_height)
    .circle(cap_radius)
    .extrude(cap_thickness)
)

# 4. Create the Side Boss
# It is located on the cylindrical surface.
# We need to find a point on the cylinder surface to extrude from, or create a cylinder and rotate/move it.
# Let's place it on the -X side (left side in a standard view, matching image perspective).
boss_z = total_height * boss_height_ratio
boss = (
    cq.Workplane("YZ")
    .workplane(offset=-cyl_radius) # Move to the surface of the cylinder on -X side
    .center(0, boss_z)             # Move up to the correct height
    .circle(boss_radius)
    .extrude(-boss_thickness)      # Extrude outwards (negative because of plane normal)
)

# --- Combine Everything ---
result = main_body.union(cap).union(boss)
