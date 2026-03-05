import cadquery as cq
import math

def create_star_points(outer_radius, inner_radius, num_points):
    """
    Helper function to calculate vertices for a star shape.
    """
    points = []
    angle_step = math.pi / num_points
    # Start angle adjusted to point upwards
    start_angle = math.pi / 2 
    
    for i in range(2 * num_points):
        r = outer_radius if i % 2 == 0 else inner_radius
        angle = start_angle + i * angle_step
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        points.append((x, y))
    
    return points

# --- Parameters ---
thickness = 2.0
overall_diameter = 40.0
num_petals = 8
petal_radius = 5.0  # Radius of the small circles forming the flower edge
base_circle_radius = 15.0 # Radius where the petal centers sit

# Letter 'D' parameters
d_height = 18.0
d_width = 14.0
d_thickness = 2.5 # Stroke width of the D shape (implicitly handled by cut)

# Star parameters
star_outer_radius = 8.0
star_inner_radius = 3.5
star_points_count = 5

# --- Geometry Construction ---

# 1. Create the Flower/Cloud Outline
# We place circles in a polar array and fuse them.
# The base is a central circle, but the image shows a hole in the middle, 
# so we really just need the outer perimeter first.
flower_sketch = cq.Workplane("XY")

# Create the central disk to fill gaps between petals
central_disk = cq.Workplane("XY").circle(base_circle_radius).extrude(thickness)

# Create the petals
petals = (
    cq.Workplane("XY")
    .polarArray(base_circle_radius, 0, 360, num_petals)
    .circle(petal_radius)
    .extrude(thickness)
)

# Fuse petals and central disk to make the main body
body = central_disk.union(petals)

# 2. Create the internal "D" shaped hole
# The D shape is essentially a rectangle + a semicircle on the right side.
# However, the image shows a "D" cutout where the *star* is solid inside the cutout area.
# This means we need to cut a D shape, but keep the Star. 
# Alternatively, we cut the D shape, then add the Star back in.

# Let's define the D-shape sketch.
# Center of the D seems slightly offset to the right to look balanced, or centered.
# Based on the image, the flat part of the D is on the left.
d_center_x = 0
d_center_y = 0

# Constructing the D profile
# A simple way is a rectangle unioned with a circle, then offset? 
# Or just drawing the lines.
d_path = (
    cq.Workplane("XY")
    .moveTo(-d_width/2, -d_height/2)
    .lineTo(-d_width/2, d_height/2) # Vertical left line
    .lineTo(0, d_height/2)          # Top horizontal
    .threePointArc((d_width/2, 0), (0, -d_height/2)) # The curved part of the D
    .close()
)

d_solid = d_path.extrude(thickness)

# 3. Create the Star
star_pts = create_star_points(star_outer_radius, star_inner_radius, star_points_count)
star_sketch = (
    cq.Workplane("XY")
    .polyline(star_pts)
    .close()
)
star_solid = star_sketch.extrude(thickness)

# --- Boolean Operations ---

# Strategy: 
# 1. Take the flower body.
# 2. Subtract the "D" shape.
# 3. Add the "Star" shape back in.
#
# Note: In the image, the Star is connected to the outer body by its tips. 
# If the star is completely inside the D-hole without touching edges, it would fall out in reality.
# In the image, the left tip of the star touches the vertical bar of the D, and the right tips touch the curve.
# The `star_outer_radius` needs to be large enough to bridge the gap if this is a single solid.

# Let's check overlap visually in mind:
# D width ~14, Star radius ~8 (total width ~16). Overlap is likely.

# Cut the D from the body
body_with_hole = body.cut(d_solid)

# Add the star back into the void
result = body_with_hole.union(star_solid)

# Optional: Add fillets to the flower edges to make it look smooth like the image
# This can be computationally expensive or fail on complex unions, but let's try a small fillet on Z edges.
# The image looks fairly sharp edged on top, so maybe no fillet is needed, or just a tiny one.
# We will leave it sharp as requested by the simple geometry interpretation.