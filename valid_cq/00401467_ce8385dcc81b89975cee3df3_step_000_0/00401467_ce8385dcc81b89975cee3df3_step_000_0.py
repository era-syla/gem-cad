import cadquery as cq

# --- Parameters ---
grip_length = 130.0
# Grip Cross Section Dimensions (Mid and Ends to create barrel shape)
mid_width, mid_height = 32.0, 44.0
end_width, end_height = 22.0, 32.0

# Leg / Support Dimensions
leg_top_x = 42.0
leg_bot_x = 82.0
leg_bot_z = -55.0
leg_width = 24.0
leg_thick = 14.0
foot_len = 20.0
foot_h = 6.0

# --- 1. Main Grip Body (Loft) ---
# Create elliptical profiles at center and ends
p_mid = cq.Workplane("YZ").ellipse(mid_width/2, mid_height/2).val()
p_end_pos = cq.Workplane("YZ").workplane(offset=grip_length/2).ellipse(end_width/2, end_height/2).val()
p_end_neg = cq.Workplane("YZ").workplane(offset=-grip_length/2).ellipse(end_width/2, end_height/2).val()

# Loft the profiles to create the barrel-shaped grip
grip = cq.Workplane("YZ").add(p_end_neg).add(p_mid).add(p_end_pos).toPending().loft()

# --- 2. Top Ridge (Loft) ---
# Create a raised strip along the top curvature
ridge_w = 10.0
ridge_h = 3.0
z_top_mid = mid_height/2
z_top_end = end_height/2

# Rectangles centered at the top edge of the ellipses
r_mid = cq.Workplane("YZ").center(0, z_top_mid).rect(ridge_w, ridge_h*4).val()
r_end_pos = cq.Workplane("YZ").workplane(offset=grip_length/2).center(0, z_top_end).rect(ridge_w, ridge_h*4).val()
r_end_neg = cq.Workplane("YZ").workplane(offset=-grip_length/2).center(0, z_top_end).rect(ridge_w, ridge_h*4).val()

ridge = cq.Workplane("YZ").add(r_end_neg).add(r_mid).add(r_end_pos).toPending().loft()

# --- 3. Top Groove (Cut Tool) ---
# A smaller loft to cut a groove along the ridge
groove_w = 3.0
g_mid = cq.Workplane("YZ").center(0, z_top_mid + ridge_h).rect(groove_w, ridge_h).val()
g_end_pos = cq.Workplane("YZ").workplane(offset=grip_length/2).center(0, z_top_end + ridge_h).rect(groove_w, ridge_h).val()
g_end_neg = cq.Workplane("YZ").workplane(offset=-grip_length/2).center(0, z_top_end + ridge_h).rect(groove_w, ridge_h).val()

groove_tool = cq.Workplane("YZ").add(g_end_neg).add(g_mid).add(g_end_pos).toPending().loft()
# Shift slightly down to ensure cut
groove_tool = groove_tool.translate((0, 0, -0.5))

# --- 4. Rivets ---
rivets = cq.Workplane("XY")
rivet_x_pos = [-35, -12, 12, 35]

for x in rivet_x_pos:
    # Interpolate Z height based on x position to match barrel curve
    factor = abs(x) / (grip_length/2)
    z = z_top_mid - (z_top_mid - z_top_end) * factor
    rivets = rivets.add(
        cq.Workplane("XY").center(x, 0).workplane(offset=z + ridge_h).circle(3.5).extrude(1.5)
    )

# --- 5. Legs ---
# Define leg profile in XZ plane
# Coordinates for the main strut
pts_leg_outer = [
    (leg_top_x, 0),
    (leg_bot_x + foot_len, leg_bot_z),
    (leg_bot_x - 5, leg_bot_z),
    (leg_top_x - 18, 0)
]

leg_base = (
    cq.Workplane("XZ")
    .polyline(pts_leg_outer)
    .close()
    .extrude(leg_width/2, both=True)
)

# Triangular cutout (through hole)
pts_hole = [
    (leg_top_x - 5, -12),
    (leg_bot_x + foot_len - 10, leg_bot_z + foot_h + 4),
    (leg_bot_x + 5, leg_bot_z + foot_h + 4)
]
leg_hole = (
    cq.Workplane("XZ")
    .polyline(pts_hole)
    .close()
    .extrude(leg_width, both=True)
)

# Recess detail (cuts on side faces)
pts_recess = [
    (leg_top_x - 2, -8),
    (leg_bot_x + foot_len - 6, leg_bot_z + 4),
    (leg_bot_x - 2, leg_bot_z + 4),
    (leg_top_x - 15, -8)
]
recess_tool = (
    cq.Workplane("XZ")
    .polyline(pts_recess)
    .close()
    .extrude(3)
)

# Apply cuts to the leg
leg = leg_base.cut(leg_hole)
leg = leg.cut(recess_tool.translate((0, leg_width/2 - 2.5, 0))) # +Y side
leg = leg.cut(recess_tool.translate((0, -(leg_width/2), 0)))    # -Y side

# Foot Plate
foot = (
    cq.Workplane("XY")
    .workplane(offset=leg_bot_z)
    .center(leg_bot_x + foot_len/2 - 2, 0)
    .rect(foot_len+8, leg_width+4)
    .extrude(foot_h)
)

# End Lip (L-bracket style)
foot_lip = (
    cq.Workplane("XZ")
    .center(leg_bot_x + foot_len + 2, leg_bot_z + foot_h/2 + 2)
    .rect(3, foot_h + 8)
    .extrude(leg_width/2 + 2, both=True)
)

# Assemble single leg
right_leg = leg.union(foot).union(foot_lip)
# Mirror for left leg
left_leg = right_leg.mirror("YZ")

# --- 6. Bottom Details ---
bot_nubs = cq.Workplane("XY")
for x in [-20, 0, 20]:
    factor = abs(x) / (grip_length/2)
    z = -(z_top_mid - (z_top_mid - z_top_end) * factor)
    bot_nubs = bot_nubs.add(
        cq.Workplane("XY").center(x, 0).workplane(offset=z + 3).circle(2.5).extrude(-5)
    )

# --- 7. Final Assembly ---
# Union Grip and Ridge, then cut groove
body = grip.union(ridge).cut(groove_tool)

# Union all components
result = body.union(rivets).union(right_leg).union(left_leg).union(bot_nubs)

# Optional: Add fillets to soften edges slightly
# result = result.edges("|Z").fillet(0.5) 