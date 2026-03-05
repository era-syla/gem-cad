import cadquery as cq

# --- Parameters ---

# Shaft dimensions
shaft_diam = 8.0
shaft_rad = shaft_diam / 2.0

# Bottom Support dimensions
bot_diam = 20.0
bot_height = 12.0
bot_rim_diam = 24.0
bot_rim_height = 3.0

# Middle Nut dimensions
nut_z_pos = 180.0
nut_body_diam = 22.0
nut_body_len = 30.0
nut_flange_width = 34.0
nut_flange_thick = 8.0
nut_flange_offset = 18.0  # Offset from bottom of the nut body
nut_hole_spacing = 26.0
nut_hole_diam = 3.5

# Top Bearing Block dimensions
top_z_pos = 350.0
top_body_diam = 22.0
top_body_len = 25.0
top_flange_width = 34.0
top_flange_thick = 8.0
top_flange_offset = 8.0   # Offset from bottom of the block body
top_neck_diam = 14.0
top_neck_height = 5.0
top_hole_spacing = 26.0
top_hole_diam = 3.5

# Calculate total shaft length to be flush with the top neck
shaft_length = top_z_pos + top_body_len + top_neck_height

# --- Modeling ---

# 1. Create the Main Shaft
shaft = cq.Workplane("XY").circle(shaft_rad).extrude(shaft_length)

# 2. Create Bottom Support
# Base rim
bot_rim = cq.Workplane("XY").circle(bot_rim_diam / 2.0).extrude(bot_rim_height)
# Main cylinder body
bot_body = (
    cq.Workplane("XY")
    .workplane(offset=bot_rim_height)
    .circle(bot_diam / 2.0)
    .extrude(bot_height - bot_rim_height)
)
# Union and cut hole for shaft
bottom_assembly = bot_rim.union(bot_body).cut(
    cq.Workplane("XY").circle(shaft_rad + 0.2).extrude(bot_height)
)

# 3. Create Middle Nut Component
# Cylindrical Body
nut_body = (
    cq.Workplane("XY")
    .workplane(offset=nut_z_pos)
    .circle(nut_body_diam / 2.0)
    .extrude(nut_body_len)
)
# Square Flange
nut_flange = (
    cq.Workplane("XY")
    .workplane(offset=nut_z_pos + nut_flange_offset)
    .rect(nut_flange_width, nut_flange_width)
    .extrude(nut_flange_thick)
)
# Add mounting holes to flange
nut_flange = (
    nut_flange.faces(">Z").workplane()
    .rect(nut_hole_spacing, nut_hole_spacing, forConstruction=True)
    .vertices()
    .hole(nut_hole_diam)
)
# Combine nut parts and cut shaft hole
nut_assembly = nut_body.union(nut_flange).cut(
    cq.Workplane("XY")
    .workplane(offset=nut_z_pos)
    .circle(shaft_rad + 0.2)
    .extrude(nut_body_len)
)

# 4. Create Top Bearing Block Component
# Cylindrical Body
top_body = (
    cq.Workplane("XY")
    .workplane(offset=top_z_pos)
    .circle(top_body_diam / 2.0)
    .extrude(top_body_len)
)
# Square Flange
top_flange = (
    cq.Workplane("XY")
    .workplane(offset=top_z_pos + top_flange_offset)
    .rect(top_flange_width, top_flange_width)
    .extrude(top_flange_thick)
)
# Add mounting holes to flange
top_flange = (
    top_flange.faces(">Z").workplane()
    .rect(top_hole_spacing, top_hole_spacing, forConstruction=True)
    .vertices()
    .hole(top_hole_diam)
)
# Top Neck Extrusion
top_neck = (
    cq.Workplane("XY")
    .workplane(offset=top_z_pos + top_body_len)
    .circle(top_neck_diam / 2.0)
    .extrude(top_neck_height)
)
# Combine top parts and cut shaft hole
top_assembly = top_body.union(top_flange).union(top_neck).cut(
    cq.Workplane("XY")
    .workplane(offset=top_z_pos)
    .circle(shaft_rad + 0.2)
    .extrude(top_body_len + top_neck_height)
)

# 5. Final Assembly
# Union all components into a single solid result
result = shaft.union(bottom_assembly).union(nut_assembly).union(top_assembly)