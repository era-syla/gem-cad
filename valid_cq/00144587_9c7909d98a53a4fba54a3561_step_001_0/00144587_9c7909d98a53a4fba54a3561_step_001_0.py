import cadquery as cq

# Parameters
diameter = 120.0
rim_width = 20.0
dish_depth = 15.0
thickness = 3.0

boss_size = 25.0
boss_height_from_bottom = 6.0  # Height of the boss top relative to the dish lowest point
boss_fillet = 2.0

pocket_size = 15.0
pocket_depth = 4.0
pocket_bottom_fillet = 3.0

# Derived coordinates
r_outer = diameter / 2.0
r_inner = r_outer - rim_width
z_center_inner = -dish_depth
z_center_outer = -dish_depth - thickness
z_rim_bottom = -thickness

# Points for the revolution profile
# Inner/Top profile points
p_center_inner = (0, z_center_inner)
p_rim_inner = (r_inner, 0)
p_rim_outer = (r_outer, 0)

# Outer/Bottom profile points
p_rim_outer_bottom = (r_outer, z_rim_bottom)
p_rim_inner_bottom = (r_inner, z_rim_bottom)
p_center_outer = (0, z_center_outer)

# 1. Create the Main Dish Body via Revolution
# We define the cross-section face on the XZ plane
# The profile consists of the rim lines and splines for the curved dish section
dish_profile = (
    cq.Workplane("XZ")
    .moveTo(*p_center_outer)
    # Bottom curve: from center bottom to inner rim bottom
    # Tangents ensure it is flat at the center and flat at the rim transition
    .spline([p_rim_inner_bottom], tangents=[(1, 0), (1, 0)], includeCurrent=True)
    .lineTo(*p_rim_outer_bottom)
    .lineTo(*p_rim_outer)
    .lineTo(*p_rim_inner)
    # Top curve: from inner rim top to center inner
    # Tangents: Heading Left at start, Heading Left at end
    .spline([p_center_inner], tangents=[(-1, 0), (-1, 0)], includeCurrent=True)
    .close()
)

main_body = dish_profile.revolve()

# 2. Create the Center Boss
# Calculate the Z height for the top of the boss
z_boss_top = z_center_inner + boss_height_from_bottom

# Create the boss shape
# We extrude downwards from the top plane deep enough to fully penetrate the curved dish
boss_extrusion_dist = boss_height_from_bottom + thickness + 5.0

boss = (
    cq.Workplane("XY")
    .workplane(offset=z_boss_top)
    .rect(boss_size, boss_size)
    .extrude(-boss_extrusion_dist)
)

# Apply fillets to the vertical edges of the boss
boss = boss.edges("|Z").fillet(boss_fillet)

# Union the boss with the main body
result = main_body.union(boss)

# 3. Create the Center Pocket
# Create the cutting tool for the pocket
pocket_tool = (
    cq.Workplane("XY")
    .workplane(offset=z_boss_top)
    .rect(pocket_size, pocket_size)
    .extrude(-pocket_depth)
)

# Add fillets to the pocket tool
# Vertical inner corners
pocket_tool = pocket_tool.edges("|Z").fillet(boss_fillet / 2.0)
# Bottom edges to create the rounded/spherical bottom look
pocket_tool = pocket_tool.faces("<Z").edges().fillet(pocket_bottom_fillet)

# Cut the pocket from the main result
result = result.cut(pocket_tool)

# 4. Final Touches
# Optional: small fillet at the very outer edge if desired, though image shows it sharp-ish.
# We leave it clean as per the image style.