import cadquery as cq

# --- Parameters ---
# Overall dimensions
length = 200.0
height = 100.0
thickness = 10.0
frame_width = 12.0

# Decoration dimensions
diamond_width = 28.0
diamond_height = 42.0
rim_width = 3.5      # Width of the frame of the diamond and arches
stem_width = 4.0
arch_radius = 12.0

# --- Derived Parameters ---
inner_width = length - 2 * frame_width
inner_height = height - 2 * frame_width
rail_y_top = inner_height / 2.0
rail_y_bottom = -inner_height / 2.0

# --- 1. Generate Frame ---
# Left Post
left_post = (
    cq.Workplane("XY")
    .center(-length / 2 + frame_width / 2, 0)
    .box(frame_width, height, thickness)
)

# Right Post
right_post = (
    cq.Workplane("XY")
    .center(length / 2 - frame_width / 2, 0)
    .box(frame_width, height, thickness)
)

# Top Rail (fits between posts)
top_rail = (
    cq.Workplane("XY")
    .center(0, height / 2 - frame_width / 2)
    .box(inner_width, frame_width, thickness)
)

# Bottom Rail (fits between posts)
bottom_rail = (
    cq.Workplane("XY")
    .center(0, -height / 2 + frame_width / 2)
    .box(inner_width, frame_width, thickness)
)

frame = left_post.union(right_post).union(top_rail).union(bottom_rail)

# --- 2. Generate Baluster Geometry ---
def make_baluster():
    # A. Diamond Center
    # Define diamond polygon points
    pts = [
        (0, diamond_height / 2),
        (diamond_width / 2, 0),
        (0, -diamond_height / 2),
        (-diamond_width / 2, 0)
    ]
    
    # Extrude outer shape and cut inner shape to make a frame
    diamond_outer = cq.Workplane("XY").polyline(pts).close().extrude(thickness)
    diamond_inner = (
        cq.Workplane("XY")
        .polyline(pts)
        .close()
        .offset2D(-rim_width)
        .extrude(thickness)
    )
    diamond = diamond_outer.cut(diamond_inner)
    
    # B. Arches
    # Create semi-circular rings attached to rails
    
    # Top Arch (facing down)
    c_top = cq.Workplane("XY").center(0, rail_y_top)
    top_arch_solid = c_top.circle(arch_radius).extrude(thickness)
    top_arch_hole = c_top.circle(arch_radius - rim_width).extrude(thickness)
    top_ring = top_arch_solid.cut(top_arch_hole)
    # Cut top half to leave bottom semi-circle
    cutter_top = c_top.center(0, arch_radius).box(arch_radius * 3, arch_radius * 2, thickness)
    top_arch = top_ring.cut(cutter_top)
    
    # Bottom Arch (facing up)
    c_bot = cq.Workplane("XY").center(0, rail_y_bottom)
    bot_arch_solid = c_bot.circle(arch_radius).extrude(thickness)
    bot_arch_hole = c_bot.circle(arch_radius - rim_width).extrude(thickness)
    bot_ring = bot_arch_solid.cut(bot_arch_hole)
    # Cut bottom half to leave top semi-circle
    cutter_bot = c_bot.center(0, -arch_radius).box(arch_radius * 3, arch_radius * 2, thickness)
    bot_arch = bot_ring.cut(cutter_bot)
    
    # C. Stems
    # Vertical bars connecting diamond to arches
    # Include slight overlap for boolean robustness
    overlap = 1.0
    
    # Top Stem
    y_start_top = diamond_height / 2 - overlap
    y_end_top = rail_y_top - arch_radius + overlap
    h_stem_top = y_end_top - y_start_top
    
    stem_top = (
        cq.Workplane("XY")
        .center(0, y_start_top + h_stem_top / 2)
        .box(stem_width, h_stem_top, thickness)
    )
    
    # Bottom Stem
    y_start_bot = rail_y_bottom + arch_radius - overlap
    y_end_bot = -diamond_height / 2 + overlap
    h_stem_bot = y_end_bot - y_start_bot
    
    stem_bot = (
        cq.Workplane("XY")
        .center(0, y_start_bot + h_stem_bot / 2)
        .box(stem_width, h_stem_bot, thickness)
    )
    
    # Combine parts
    return diamond.union(top_arch).union(bot_arch).union(stem_top).union(stem_bot)

# --- 3. Assemble ---
baluster_element = make_baluster()

# Position two balusters evenly within the frame
# Divides the inner space into 3 equal zones relative to centers/edges
offset_x = inner_width / 6.0

baluster_left = baluster_element.translate((-offset_x, 0, 0))
baluster_right = baluster_element.translate((offset_x, 0, 0))

# Combine all into final result
result = frame.union(baluster_left).union(baluster_right)