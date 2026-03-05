import cadquery as cq
import math

# --- Parameters ---
# Main ring dimensions
outer_diameter = 100.0
inner_diameter = 60.0
thickness = 3.0

# Groove/Track dimensions
groove_depth = 1.5
groove_width = 8.0
groove_offset_from_center = (outer_diameter + inner_diameter) / 4.0 # Roughly centered on the ring

# Blade dimensions
blade_angle = 60.0  # Degrees covered by the blade
blade_thickness = 1.0
pivot_hole_dia = 2.0
pivot_offset = (outer_diameter / 2) - 5.0 # Distance from center to pivot point

# Screw holes on the main ring
hole_dia = 2.5
num_hole_pairs = 3
hole_bc_dia = 88.0 # Bolt circle diameter

# --- Geometry Construction ---

# 1. Base Ring
base_ring = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(thickness)
)

# 2. Recessed Track/Groove
# Creating a circular groove cut into the top face
track_r_outer = (outer_diameter / 2) - 5.0
track_r_inner = (inner_diameter / 2) + 5.0

track_cut = (
    cq.Workplane("XY")
    .workplane(offset=thickness - groove_depth)
    .circle(track_r_outer)
    .circle(track_r_inner)
    .extrude(groove_depth)
)

ring_with_track = base_ring.cut(track_cut)

# 3. Mounting Holes
# The image shows pairs of small holes around the perimeter
def create_hole_pairs(part):
    res = part
    for i in range(num_hole_pairs):
        angle = i * (360.0 / num_hole_pairs)
        # Pair hole 1
        res = res.faces(">Z").workplane().polarArray(hole_bc_dia/2, angle - 10, 360, 1).hole(hole_dia)
        # Pair hole 2
        res = res.faces(">Z").workplane().polarArray(hole_bc_dia/2, angle + 10, 360, 1).hole(hole_dia)
    return res

final_ring = create_hole_pairs(ring_with_track)

# 4. The Shutter Blade (Leaf)
# This is a complex shape, essentially an arc sector with pivot points.
# We'll construct it separately and then place it.

# Geometric construction of the blade shape
# It looks like a "shark fin" or curvilinear triangle shape common in iris diaphragms.
blade_sketch = (
    cq.Workplane("XY")
    .moveTo(track_r_inner + 1, 0)
    .lineTo(track_r_outer - 1, 0)
    # Outer arc
    .radiusArc((0, track_r_outer - 1), -track_r_outer+1) # Negative radius for concave/convex control usually needed here, approximating with 3 points is safer often
    # Let's try a 3-point arc or parametric curve approach for better control
    # Actually, simpler: Intersection of two circles or a loft
)

# Alternative Blade Construction:
# Center of rotation for the blade arc is often offset.
# Let's make a simplified representation that matches the visual.
blade_pivot_r = (track_r_outer + track_r_inner) / 2.0
blade_width_angle = 45.0

# Create the blade body
blade = (
    cq.Workplane("XY")
    .workplane(offset=thickness - groove_depth) # Sit inside the track
    .polarArray(blade_pivot_r, 0, 360, 1) # Position helper
    .circle( (track_r_outer - track_r_inner)/2 * 1.5 ) # Crude approximation of shape via circle
    .extrude(blade_thickness)
)

# Let's do a more proper 2D shape for the blade
# It has an inner edge (curvature of ID), outer edge (curvature of OD), and pivot points.
pts = [
    (track_r_inner * math.cos(math.radians(10)), track_r_inner * math.sin(math.radians(10))),
    (track_r_outer * math.cos(math.radians(0)), track_r_outer * math.sin(math.radians(0))),
    (track_r_outer * math.cos(math.radians(50)), track_r_outer * math.sin(math.radians(50))),
    (track_r_inner * math.cos(math.radians(40)), track_r_inner * math.sin(math.radians(40)))
]

blade_shape = (
    cq.Workplane("XY")
    .moveTo(pts[0][0], pts[0][1])
    .threePointArc( ((pts[0][0]+pts[1][0])/2, (pts[0][1]+pts[1][1])/2 - 2), pts[1]) # Inner curve
    .threePointArc( ((pts[1][0]+pts[2][0])/2 + 2, (pts[1][1]+pts[2][1])/2 + 2), pts[2]) # Outer curve
    .lineTo(pts[3][0], pts[3][1])
    .close()
    .extrude(blade_thickness)
)

# Since constructing the exact mathematical curve of an iris blade is complex without specific constraints,
# we will approximate the shape visible in the image: a pie-slice like shape with rounded corners/pivots.

blade_r_outer = (outer_diameter / 2) - 2
blade_r_inner = (inner_diameter / 2) - 5 # To cover the hole slightly
blade_center_offset = 25.0 # The center of the blade arc is offset from main center

blade_solid = (
    cq.Workplane("XY")
    .workplane(offset=thickness) # Sit on top/flush
    .moveTo(25, -20) # Start point
    .threePointArc((50, 0), (25, 30)) # Outer arc
    .lineTo(5, 10)
    .threePointArc((15, 0), (5, -15)) # Inner arc
    .close()
    .extrude(blade_thickness)
)

# Let's refine the blade to match the specific "cam slot" look in the image.
# It sits in the recess.
# It has a pivot pin hole and a driving pin hole.

blade_draw = (
    cq.Workplane("XY")
    .workplane(offset=thickness - groove_depth)
    # Pivot point area
    .moveTo(track_r_outer - 3, -10)
    .circle(3.5)
    # Main body arc
    .moveTo(track_r_outer - 3, -10)
    .threePointArc( (track_r_outer - 8, 15), (track_r_inner + 2, 25) )
    .lineTo(track_r_inner - 2, 0)
    .threePointArc( (track_r_inner + 5, -15), (track_r_outer - 3, -10) )
    .close()
    .extrude(blade_thickness)
)

# Add pins/holes to blade
# The image shows a small link arm or thickened section on the outer edge of the blade
link_arm = (
    cq.Workplane("XY")
    .workplane(offset=thickness - groove_depth + blade_thickness)
    .moveTo(track_r_outer - 3, -10)
    .circle(3.5)
    .extrude(0.5)
)

blade_final = blade_draw.union(link_arm)

# Cut holes in the blade pivot points
# Pivot 1
blade_final = blade_final.faces(">Z").workplane().moveTo(track_r_outer - 3, -10).hole(pivot_hole_dia)
# Pivot 2 (approximate location based on image)
blade_final = blade_final.faces(">Z").workplane().moveTo(track_r_inner + 4, 22).hole(pivot_hole_dia)


# Combine Assembly
# We will rotate the blade slightly to match the "closing" action look
blade_positioned = blade_final.rotate((0,0,0), (0,0,1), -45)

result = final_ring.union(blade_positioned)

# Export or visualization handling would happen here externally
# Part.show(result)