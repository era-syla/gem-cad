import cadquery as cq
import math

# --- Parameters ---

# Main Base (Polygonal disk)
poly_sides = 10       # Decagon based on visual approximation
poly_diameter = 25.0  # Circumscribed diameter
base_thickness = 2.0

# Central Tube
tube_od = 4.0
tube_id = 2.5
tube_height = 6.0

# Triangular Tail
tail_length = 60.0    # Length from center to tip
tail_width_base = 10.0 # Width of the triangle at the connection point

# Star Tip
star_points = 5
star_outer_r = 5.0
star_inner_r = 2.0

# Separate Object (Triangular Prism)
prism_side = 12.0     # Base side length
prism_height = 25.0
prism_pos_x = -40.0
prism_pos_y = -15.0

# --- Geometry Construction ---

# 1. Create the main polygonal base
# We align it on the XY plane.
base = (cq.Workplane("XY")
        .polygon(poly_sides, poly_diameter)
        .extrude(base_thickness))

# 2. Create the vertical tube feature
# Centered on the base
tube = (cq.Workplane("XY")
        .workplane(offset=base_thickness)
        .circle(tube_od / 2.0)
        .circle(tube_id / 2.0)
        .extrude(tube_height))

# 3. Create the triangular tail
# Defined as a triangle starting at the center (to ensure overlap) and extending to the right (+X)
tail = (cq.Workplane("XY")
        .moveTo(0, tail_width_base / 2.0)
        .lineTo(tail_length, 0)
        .lineTo(0, -tail_width_base / 2.0)
        .close()
        .extrude(base_thickness))

# 4. Create the Star
# We define a helper to calculate star points
def generate_star_points(cx, cy, r_out, r_in, points):
    pts = []
    angle_step = math.pi / points
    # Start at angle 0 (pointing +X)
    for i in range(2 * points):
        r = r_out if i % 2 == 0 else r_in
        angle = i * angle_step
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        pts.append((x, y))
    return pts

# Generate points centered at the tip of the tail
star_pts = generate_star_points(tail_length, 0, star_outer_r, star_inner_r, star_points)

star = (cq.Workplane("XY")
        .polyline(star_pts)
        .close()
        .extrude(base_thickness))

# Assemble the "Wand" part
wand_assembly = base.union(tube).union(tail).union(star)

# 5. Create the separate Triangular Prism
# Located to the left of the main assembly
separate_prism = (cq.Workplane("XY")
                  .polygon(3, prism_side)
                  .extrude(prism_height)
                  .translate((prism_pos_x, prism_pos_y, 0)))

# Final Result combining both disconnected parts
result = wand_assembly.union(separate_prism)