import cadquery as cq
import math

# -----------------------------------------------------------------------------
# Part Parameters
# -----------------------------------------------------------------------------
module = 2.5
num_teeth_full = 21       # Estimated total teeth for full gear circle
num_teeth_sector = 7      # Number of visible teeth in the sector
pressure_angle_deg = 20.0
thickness = 15.0          # Thickness of the gear
bore_diameter = 12.0      # Central hole diameter

# -----------------------------------------------------------------------------
# Geometric Calculations
# -----------------------------------------------------------------------------
pressure_angle = math.radians(pressure_angle_deg)
pitch_radius = (module * num_teeth_full) / 2.0
base_radius = pitch_radius * math.cos(pressure_angle)
addendum = module
dedendum = 1.25 * module
tip_radius = pitch_radius + addendum
root_radius = pitch_radius - dedendum

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------
def get_involute_points(base_r, tip_r, resolution=10):
    """Generates (x, y) points for a standard involute curve."""
    pts = []
    # Maximum parameter u for the tip radius
    if tip_r < base_r:
        max_u = 0 
    else:
        # r^2 = rb^2 * (1 + u^2)
        max_u = math.sqrt((tip_r / base_r) ** 2 - 1)
    
    for i in range(resolution + 1):
        u = max_u * (i / resolution)
        x = base_r * (math.cos(u) + u * math.sin(u))
        y = base_r * (math.sin(u) - u * math.cos(u))
        pts.append((x, y))
    return pts

def generate_tooth_wire_points():
    """Generates the closed polygon points for a single gear tooth."""
    # 1. Generate one flank (involute)
    flank_pts = get_involute_points(base_radius, tip_radius, resolution=15)
    
    # 2. Rotate flank to correct angular position
    # The tooth thickness at pitch circle is (pi * m / 2).
    # The half-thickness angle is pi / (2 * N).
    # The involute function generates a curve starting at angle 0.
    # At pitch radius, the involute angle is (tan(alpha) - alpha).
    # We need to rotate the curve so the point at pitch radius aligns with the half-thickness angle.
    inv_alpha = math.tan(pressure_angle) - pressure_angle
    half_tooth_angle = math.pi / (2 * num_teeth_full)
    rotation_offset = half_tooth_angle - inv_alpha
    
    upper_flank = []
    for x, y in flank_pts:
        r = math.sqrt(x*x + y*y)
        theta = math.atan2(y, x)
        new_theta = theta + rotation_offset
        upper_flank.append((r * math.cos(new_theta), r * math.sin(new_theta)))
        
    # 3. Create lower flank by mirroring upper flank across X-axis
    lower_flank = [(x, -y) for x, y in upper_flank]
    lower_flank.reverse() # Reverse to maintain CCW order
    
    # 4. Define points extending into the hub (root)
    # We extend the profile slightly inside the root radius to ensure a solid boolean union.
    inner_r = root_radius - 0.5  # Slightly deeper than root surface
    
    pts = []
    
    # Start point (deep inside root, matching lower flank angle)
    p_start = lower_flank[0]
    ang_start = math.atan2(p_start[1], p_start[0])
    pts.append((inner_r * math.cos(ang_start), inner_r * math.sin(ang_start)))
    
    # Flank points
    pts.extend(lower_flank)
    pts.extend(upper_flank)
    
    # End point (deep inside root, matching upper flank angle)
    p_end = upper_flank[-1]
    ang_end = math.atan2(p_end[1], p_end[0])
    pts.append((inner_r * math.cos(ang_end), inner_r * math.sin(ang_end)))
    
    # Close the loop
    pts.append(pts[0])
    
    return pts

# -----------------------------------------------------------------------------
# Model Construction
# -----------------------------------------------------------------------------

# 1. Create the central hub (Sector Base)
# The non-toothed part acts as the root cylinder.
hub = cq.Workplane("XY").circle(root_radius).extrude(thickness)

# 2. Create a single tooth solid
tooth_pts = generate_tooth_wire_points()
single_tooth = cq.Workplane("XY").polyline(tooth_pts).close().extrude(thickness)

# 3. Pattern the teeth to form the sector
# We want the teeth centered at the "top" (90 degrees).
angle_step = 360.0 / num_teeth_full
half_sector = num_teeth_sector // 2
teeth_solid = None

for i in range(-half_sector, half_sector + 1):
    # Calculate angle for this tooth
    # 90 degrees is the center of the sector
    angle = 90.0 + (i * angle_step)
    
    # Rotate the basic tooth (which is defined on X-axis) to the position
    rotated_tooth = single_tooth.rotate((0, 0, 0), (0, 0, 1), angle)
    
    if teeth_solid is None:
        teeth_solid = rotated_tooth
    else:
        teeth_solid = teeth_solid.union(rotated_tooth)

# 4. Union Hub and Teeth
result = hub.union(teeth_solid)

# 5. Cut the central bore
result = result.faces(">Z").workplane().circle(bore_diameter / 2).cutThruAll()

# 6. Apply Chamfers
# Chamfer the bore edges for a finished look
result = result.edges(cq.selectors.RadiusNthSelector(0)).chamfer(0.5)

# Optional: Chamfer the outer edges of the hub faces for realism
# Selecting edges with radius close to root_radius
try:
    result = result.edges(cq.selectors.RadiusNthSelector(1)).chamfer(0.5)
except:
    pass # Skip if geometry is too complex for simple selector
