import cadquery as cq
import math

# --- Parameters ---
height = 10.0
width = 6.0
thickness = 2.0
extrude_depth = 2.0

# Spacing
char_spacing = 1.0  # Gap between letters in a pair (e.g., L and A)
group_spacing = 2.5 # Gap around the central star

# --- Helper Functions ---

def star_polygon(outer_radius, inner_radius, num_points=5):
    """Generates a list of (x, y) points for a star."""
    points = []
    angle = math.pi / 2  # Start pointing straight up
    angle_step = math.pi / num_points
    for i in range(2 * num_points):
        r = outer_radius if i % 2 == 0 else inner_radius
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        points.append((x, y))
        angle += angle_step
    return points

# --- Geometry Definition ---

# 1. Define 'L' Shape
# Outline: Vertical bar on left, horizontal bar on bottom
pts_L = [
    (0, 0),
    (width, 0),
    (width, thickness),
    (thickness, thickness),
    (thickness, height),
    (0, height)
]
solid_L = cq.Workplane("XY").polyline(pts_L).close().extrude(extrude_depth)

# 2. Define 'Reverse F' Shape (Backwards F)
# Outline: Vertical bar on right, horizontal bars pointing left
# Determine middle bar position
mid_bar_bottom = (height - thickness) / 2
mid_bar_top = mid_bar_bottom + thickness

pts_RevF = [
    (width, 0),
    (width, height),
    (0, height),
    (0, height - thickness),
    (width - thickness, height - thickness),
    (width - thickness, mid_bar_top),
    (0, mid_bar_top),
    (0, mid_bar_bottom),
    (width - thickness, mid_bar_bottom),
    (width - thickness, 0)
]
solid_RevF = cq.Workplane("XY").polyline(pts_RevF).close().extrude(extrude_depth)

# 3. Define 'F' Shape
# Outline: Vertical bar on left, horizontal bars pointing right
pts_F = [
    (0, 0),
    (thickness, 0),
    (thickness, mid_bar_bottom),
    (width, mid_bar_bottom),
    (width, mid_bar_top),
    (thickness, mid_bar_top),
    (thickness, height - thickness),
    (width, height - thickness),
    (width, height),
    (0, height)
]
solid_F = cq.Workplane("XY").polyline(pts_F).close().extrude(extrude_depth)

# 4. Define Star Shape
star_outer_r = height / 2.0
star_inner_r = star_outer_r * 0.4
pts_star = star_polygon(star_outer_r, star_inner_r)

# Create star solid and lift it so it sits within the 0-height range vertically
# (Star points are centered at 0,0, radius R implies range -R to +R)
solid_Star = cq.Workplane("XY").polyline(pts_star).close().extrude(extrude_depth).translate((0, height / 2.0, 0))


# --- Assembly ---

current_x = 0.0

# 1. Left 'L'
part1 = solid_L
current_x += width + char_spacing

# 2. Left 'Reverse F'
part2 = solid_RevF.translate((current_x, 0, 0))
current_x += width + group_spacing

# 3. Center Star
# We translate by current_x + radius because the star is defined around its center
part3 = solid_Star.translate((current_x + star_outer_r, 0, 0))
current_x += (star_outer_r * 2) + group_spacing

# 4. Right 'F'
part4 = solid_F.translate((current_x, 0, 0))
current_x += width + char_spacing

# 5. Right 'L'
part5 = solid_L.translate((current_x, 0, 0))

# Combine all parts
result = part1.union(part2).union(part3).union(part4).union(part5)