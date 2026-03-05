import cadquery as cq
import math

# --- Parameters ---
# Main body dimensions
height_main = 70.0
radius_base_outer = 22.0
radius_base_inner = 18.0
radius_top_outer = 14.0
radius_top_inner = 11.0
twist_angle = 60.0  # Degrees of twist over the main body
num_ribs = 10       # Number of helical flutes

# Top cap and neck dimensions
neck_height = 4.0
neck_radius = 11.0
cap_height = 5.0
cap_radius = 15.0
groove_radius = 12.0 # Detail between neck and cap
groove_height = 2.0

# Bottom shaft dimensions
shaft_height = 10.0
shaft_radius = 12.0

# --- Helper Functions ---

def generate_star_profile(r_outer, r_inner, n_ribs, z_pos, rotation_deg):
    """
    Generates a list of (x, y, z) points representing a star/gear profile.
    Used for the cross-sections of the twisted main body.
    """
    points = []
    angle_step = (2 * math.pi) / (2 * n_ribs)
    rotation_rad = math.radians(rotation_deg)
    
    for i in range(2 * n_ribs):
        theta = i * angle_step + rotation_rad
        # Alternate between outer and inner radius to create ribs
        r = r_outer if i % 2 == 0 else r_inner
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        points.append((x, y, z_pos))
        
    return points

# --- Geometry Construction ---

# 1. Create the Main Body (Lofted Twisted Star)
# Generate points for bottom and top profiles
pts_bottom = generate_star_profile(radius_base_outer, radius_base_inner, num_ribs, 0, 0)
pts_top = generate_star_profile(radius_top_outer, radius_top_inner, num_ribs, height_main, twist_angle)

# Create wires from points
# Note: We create separate workplanes/wires and add them to a loft operation
wire_bottom = cq.Workplane("XY").polyline(pts_bottom).close().val()
wire_top = cq.Workplane("XY").workplane(offset=height_main).polyline(pts_top).close().val()

# Loft between the two wires to create the twisted tapered body
main_body = cq.Workplane("XY").add(wire_bottom).add(wire_top).toPending().loft()

# 2. Create the Neck and Cap
# Position: On top of the main body
# Neck cylinder
neck = (
    cq.Workplane("XY")
    .workplane(offset=height_main)
    .circle(neck_radius)
    .extrude(neck_height)
)

# Small Groove/Transition Detail
groove_z = height_main + neck_height
groove = (
    cq.Workplane("XY")
    .workplane(offset=groove_z)
    .circle(groove_radius)
    .extrude(groove_height)
)

# Top Cap
cap_z = groove_z + groove_height
cap = (
    cq.Workplane("XY")
    .workplane(offset=cap_z)
    .circle(cap_radius)
    .extrude(cap_height)
)

# Add chamfer to the top edge of the cap for detail
cap = cap.edges(">Z").chamfer(1.0)

# 3. Create the Bottom Shaft
# Position: Extending downwards from z=0
shaft = (
    cq.Workplane("XY")
    .workplane(offset=-shaft_height)
    .circle(shaft_radius)
    .extrude(shaft_height)
)

# 4. Combine all parts
result = main_body.union(neck).union(groove).union(cap).union(shaft)

# Optional: Fillet the bottom of the main body ribs slightly if desired, 
# but usually lofted sharp edges fail with simple fillets. 
# We leave it sharp as per the technical look of the image.