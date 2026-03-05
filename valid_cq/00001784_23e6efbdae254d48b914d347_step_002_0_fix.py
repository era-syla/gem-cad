import cadquery as cq

# Create a cross/plus shape with rounded corners
# The shape looks like 4 rounded squares arranged in a cross pattern

def make_cross_shape(arm_width, arm_length, corner_radius):
    """Create a 2D cross shape using union of rounded rectangles"""
    # Center square
    center_size = arm_width
    
    # Horizontal bar
    h_bar = (cq.Workplane("XY")
             .rect(arm_length * 2 + arm_width, arm_width)
             .extrude(1))
    
    # Vertical bar
    v_bar = (cq.Workplane("XY")
             .rect(arm_width, arm_length * 2 + arm_width)
             .extrude(1))
    
    cross = h_bar.union(v_bar)
    return cross

# Parameters
arm_w = 30      # width of each arm
arm_l = 15      # extension length of each arm beyond center
total_w = arm_w + arm_l * 2  # total width
corner_r = 8    # corner radius for the lobes
height_top = 8  # height of the top (thicker) part
height_bottom = 4  # height of the bottom (thinner) part

# Create the cross shape as 4 overlapping rounded squares
# Each lobe is a rounded square, and they overlap in the center

lobe_size = arm_w  # size of each rounded square lobe
offset = arm_w / 2  # offset from center

# Top lobe
top_lobe = (cq.Workplane("XY")
            .rect(lobe_size, lobe_size)
            .extrude(height_top))

top_lobe = (top_lobe
            .edges("|Z")
            .fillet(corner_r))

# Position offsets for the 4 lobes
positions = [
    (offset, offset),    # top-right
    (-offset, offset),   # top-left
    (-offset, -offset),  # bottom-left
    (offset, -offset),   # bottom-right
]

# Build the top part as union of 4 rounded squares
top_part = None
for px, py in positions:
    lobe = (cq.Workplane("XY")
            .transformed(offset=(px, py, 0))
            .rect(lobe_size, lobe_size)
            .extrude(height_top))
    lobe = lobe.edges("|Z").fillet(corner_r)
    
    if top_part is None:
        top_part = lobe
    else:
        top_part = top_part.union(lobe)

# Build the bottom part - slightly smaller cross
# The bottom part is the 4 arms of a cross (narrower)
bottom_arm_w = arm_w * 0.85
bottom_arm_l = arm_l * 0.9

# Bottom horizontal bar
h_bottom = (cq.Workplane("XY")
            .rect(arm_w * 2 + bottom_arm_w, bottom_arm_w)
            .extrude(height_bottom))

# Bottom vertical bar  
v_bottom = (cq.Workplane("XY")
            .rect(bottom_arm_w, arm_w * 2 + bottom_arm_w)
            .extrude(height_bottom))

bottom_part = h_bottom.union(v_bottom)

# Combine bottom and top
result = top_part.union(
    bottom_part.translate((0, 0, 0))
)

# Actually, let me rebuild more carefully
# The image shows a cross shape with:
# - A thicker top platform
# - A slightly stepped/narrower bottom edge

lobe_sz = 35
off = 17
cr = 9
th = 10   # total height
step_h = 3  # step height at bottom
step_inset = 3  # how much the bottom steps in

lobes_top = None
for px, py in [(off, off), (-off, off), (-off, -off), (off, -off)]:
    lobe = (cq.Workplane("XY")
            .transformed(offset=(px, py, 0))
            .rect(lobe_sz, lobe_sz)
            .extrude(th))
    lobe = lobe.edges("|Z").fillet(cr)
    if lobes_top is None:
        lobes_top = lobe
    else:
        lobes_top = lobes_top.union(lobe)

# Bottom step - same shape but inset
lobes_bot = None
lobe_sz2 = lobe_sz - step_inset * 2
cr2 = cr - step_inset if cr > step_inset else cr
for px, py in [(off, off), (-off, off), (-off, -off), (off, -off)]:
    lobe = (cq.Workplane("XY")
            .transformed(offset=(px, py, 0))
            .rect(lobe_sz2, lobe_sz2)
            .extrude(step_h))
    if cr2 > 0:
        lobe = lobe.edges("|Z").fillet(cr2)
    if lobes_bot is None:
        lobes_bot = lobe
    else:
        lobes_bot = lobes_bot.union(lobe)

result = lobes_top.union(lobes_bot)