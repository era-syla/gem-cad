import cadquery as cq
import math

# --- Parameters ---
# Central Body
sphere_radius = 10.0
boss_radius = 6.0
boss_height = 2.5

# Left Arm (Vertical Tab)
left_arm_length = 14.0   # Length extending from sphere
left_arm_height = 14.0   # Vertical height (Z)
left_arm_thickness = 3.5 # Horizontal thickness (Y)
left_hole_diameter = 4.0
hex_width = 7.0          # Flat-to-flat distance
hex_depth = 1.5

# Right Arm (Horizontal Key)
right_arm_dist = 24.0    # Distance from center to key center
key_outer_radius = 10.0
key_thickness = 2.5      # Vertical thickness (Z)
neck_width = 6.0         # Connection width (Y)
spline_hole_od = 5.0     # Outer diameter of the spline pattern

# --- Helper Functions ---
def star_profile(r_outer, r_inner, n_points):
    """Generates a list of (x, y) points for a star/gear/spline profile."""
    pts = []
    for i in range(2 * n_points):
        angle = math.radians(i * 360 / (2 * n_points))
        r = r_outer if i % 2 == 0 else r_inner
        pts.append((r * math.cos(angle), r * math.sin(angle)))
    return pts

# --- Modeling ---

# 1. Central Body
# Create the main sphere
center_sphere = cq.Workplane("XY").sphere(sphere_radius)

# Create the top boss (domed cylinder)
top_boss = (
    cq.Workplane("XY")
    .workplane(offset=sphere_radius - 1.5)
    .circle(boss_radius)
    .extrude(boss_height + 2.0)
    .edges(">Z").fillet(boss_radius * 0.4)
)

# Union sphere and boss
body = center_sphere.union(top_boss)

# 2. Left Arm (Vertical Tab)
# Defined on XZ plane, extruded along Y
l_overlap = 2.0
l_start = -sphere_radius + l_overlap
l_end = -(sphere_radius + left_arm_length)

left_arm = (
    cq.Workplane("XZ")
    .workplane(offset=-left_arm_thickness/2)
    .moveTo(l_start, -left_arm_height/2)
    .lineTo(l_end, -left_arm_height/2)
    .lineTo(l_end, left_arm_height/2)
    .lineTo(l_start, left_arm_height/2)
    .close()
    .extrude(left_arm_thickness)
)

# Fillet the end of the arm
left_arm = left_arm.edges("|Y").filter(lambda e: e.Center().x < l_end + 1.0).fillet(1.0)

# Create Hexagonal Recess and Through Hole
hole_x_pos = (l_start + l_end) / 2
# Calculate circumradius for hexagon from flat-to-flat width
hex_circumradius = (hex_width / 2) / math.cos(math.radians(30))

left_arm = (
    left_arm.faces(">Y").workplane()
    .moveTo(hole_x_pos, 0)
    .polygon(6, hex_circumradius * 2) # CadQuery polygon takes diameter
    .cutBlind(-hex_depth)
    .workplane(offset=-hex_depth) # Move deeper
    .moveTo(hole_x_pos, 0)
    .circle(left_hole_diameter / 2)
    .cutThruAll()
)

# 3. Right Arm (Horizontal Key)
# Neck connection
neck_overlap = 2.0
neck_start = sphere_radius - neck_overlap
neck_end = right_arm_dist

neck = (
    cq.Workplane("XY")
    .workplane(offset=-key_thickness/2)
    .moveTo(neck_start, neck_width/2)
    .lineTo(neck_end, neck_width/2)
    .lineTo(neck_end, -neck_width/2)
    .lineTo(neck_start, -neck_width/2)
    .close()
    .extrude(key_thickness)
)

# Key Head (Serrated Disk)
# Generate points for serrated edge
serration_depth = 0.5
serrations_count = 24
outer_profile = star_profile(key_outer_radius, key_outer_radius - serration_depth, serrations_count)

key_head = (
    cq.Workplane("XY")
    .workplane(offset=-key_thickness/2)
    .center(right_arm_dist, 0)
    .polyline(outer_profile).close()
    .extrude(key_thickness)
)

# Internal Spline Cut
# Generate points for internal splines
spline_depth = 0.5
splines_count = 14
# For a hole, outer points are the valleys, inner points are the teeth tips
inner_profile = star_profile(spline_hole_od/2 + spline_depth, spline_hole_od/2, splines_count)

key_head = (
    key_head.faces(">Z").workplane()
    .center(right_arm_dist, 0)
    .polyline(inner_profile).close()
    .cutThruAll()
)

# 4. Assembly and Finishing
# Union all parts
result = body.union(left_arm).union(neck).union(key_head)

# Apply Fillets to transitions
# We select edges based on their proximity to the sphere intersection zones
try:
    fillet_radius = 2.5
    
    # Left Arm to Sphere junction
    # Selecting edges near x = -sphere_radius
    result = result.edges(
        cq.selectors.BoxSelector(
            (l_start - 3, -left_arm_thickness*2, -left_arm_height), 
            (l_start + 3, left_arm_thickness*2, left_arm_height)
        )
    ).fillet(fillet_radius)
    
    # Right Neck to Sphere junction
    # Selecting edges near x = sphere_radius
    result = result.edges(
        cq.selectors.BoxSelector(
            (neck_start - 3, -neck_width*2, -key_thickness*2), 
            (neck_start + 3, neck_width*2, key_thickness*2)
        )
    ).fillet(fillet_radius)
    
    # Neck to Key Head transition (smoothing)
    result = result.edges(
        cq.selectors.BoxSelector(
            (right_arm_dist - key_outer_radius - 1, -neck_width*1.5, -key_thickness),
            (right_arm_dist - key_outer_radius + 4, neck_width*1.5, key_thickness)
        )
    ).fillet(1.5)

except Exception:
    # Fallback in case fillet geometry is invalid
    pass
