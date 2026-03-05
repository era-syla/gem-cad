import cadquery as cq
import math

# Main dimensions
outer_r = 12.0
inner_r = 7.0
mid_r = 15.0
top_h = 35.0
mid_h = 12.0
bot_h = 35.0
total_h = top_h + mid_h + bot_h

# Build main body: bottom cylinder + middle wider ring + top cylinder
bottom = cq.Workplane("XY").cylinder(bot_h, outer_r)
middle = cq.Workplane("XY").workplane(offset=bot_h).cylinder(mid_h, mid_r)
top = cq.Workplane("XY").workplane(offset=bot_h + mid_h).cylinder(top_h, outer_r)

# Combine
result = (
    cq.Workplane("XY")
    .union(bottom)
    .union(middle)
    .union(top)
)

# Hollow out the center bore through entire height
result = result.cut(
    cq.Workplane("XY").cylinder(total_h + 2, inner_r)
)

# Add notches/slots on top section - 4 vertical slots equally spaced
# These are small rectangular cuts on the outer surface of the top cylinder
slot_w = 3.0
slot_d = 4.0
slot_h = 12.0
slot_z_top = bot_h + mid_h + top_h / 2  # middle of top section

for i in range(4):
    angle = i * 90.0
    rad = math.radians(angle)
    x = (outer_r - slot_d / 2) * math.cos(rad)
    y = (outer_r - slot_d / 2) * math.sin(rad)
    
    slot = (
        cq.Workplane("XY")
        .workplane(offset=slot_z_top - slot_h / 2)
        .center(x, y)
        .box(slot_w, slot_d + 4, slot_h)
    )
    result = result.cut(slot)

# Add notches/slots on bottom section - 4 vertical slots equally spaced
slot_z_bot = bot_h / 2  # middle of bottom section

for i in range(4):
    angle = i * 90.0 + 45.0  # offset by 45 degrees for bottom
    rad = math.radians(angle)
    x = (outer_r - slot_d / 2) * math.cos(rad)
    y = (outer_r - slot_d / 2) * math.sin(rad)
    
    slot = (
        cq.Workplane("XY")
        .workplane(offset=slot_z_bot - slot_h / 2)
        .center(x, y)
        .box(slot_w, slot_d + 4, slot_h)
    )
    result = result.cut(slot)

# Add small clip features on top section (the small tabs visible in the image)
clip_w = 2.5
clip_h = 4.0
clip_d = 2.0
clip_z = bot_h + mid_h + top_h * 0.35

for i in range(4):
    angle = i * 90.0
    rad = math.radians(angle)
    cx = (outer_r + clip_d / 2) * math.cos(rad)
    cy = (outer_r + clip_d / 2) * math.sin(rad)
    
    clip = (
        cq.Workplane("XY")
        .workplane(offset=clip_z - clip_h / 2)
        .center(cx, cy)
        .box(clip_w, clip_d, clip_h)
    )
    result = result.union(clip)

# Add small clip features on bottom section
clip_z_bot = bot_h * 0.65

for i in range(4):
    angle = i * 90.0 + 45.0
    rad = math.radians(angle)
    cx = (outer_r + clip_d / 2) * math.cos(rad)
    cy = (outer_r + clip_d / 2) * math.sin(rad)
    
    clip = (
        cq.Workplane("XY")
        .workplane(offset=clip_z_bot - clip_h / 2)
        .center(cx, cy)
        .box(clip_w, clip_d, clip_h)
    )
    result = result.union(clip)