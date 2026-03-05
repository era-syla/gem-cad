import cadquery as cq

# -- Parametric Dimensions --
# Overall dimensions
length = 200.0
thickness = 2.0
strip_height = 5.0

# Left End Geometry (The deeper, hooked end)
left_drop_height = 15.0     # Distance the left end extends downwards
left_bottom_flat = 2.0      # Length of the flat bottom segment
left_taper_len = 15.0       # Length of the angled transition
tooth_height = 2.5          # Height of the small 'hook' or step at top-left
tooth_width = 3.0           # Width of the small 'hook'

# Right End Geometry (The gently rising end)
right_rise_height = 8.0     # Distance the right end extends upwards
right_taper_len = 50.0      # Length of the long angled transition
right_top_flat = 8.0        # Length of the flat top segment at the end

# -- Profile Generation --
# Points are defined in (x, y) tuples, tracing the perimeter counter-clockwise.
# Origin (0,0) is defined at the x-start, aligned with the bottom edge of the central strip.
pts = []

# 1. Start at bottom-left corner of the dropped section
pts.append((0, -left_drop_height))

# 2. Bottom flat of left section
pts.append((left_bottom_flat, -left_drop_height))

# 3. Taper up to the central strip's bottom line (y=0)
pts.append((left_bottom_flat + left_taper_len, 0))

# 4. Bottom right corner (Assuming straight bottom edge for the rest of the part)
pts.append((length, 0))

# 5. Top right corner
pts.append((length, strip_height + right_rise_height))

# 6. Top flat of right section
pts.append((length - right_top_flat, strip_height + right_rise_height))

# 7. Taper down to the central strip height
pts.append((length - right_top_flat - right_taper_len, strip_height))

# 8. Top edge of central strip (going left until the tooth)
pts.append((tooth_width, strip_height))

# 9. Step up for the tooth/hook
pts.append((tooth_width, strip_height + tooth_height))

# 10. Top-left corner (Top of tooth)
pts.append((0, strip_height + tooth_height))

# -- 3D Model Creation --
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)