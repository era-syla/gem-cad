import cadquery as cq
import math

# --- Parameters ---
module = 2.0             # Module of the gear (controls overall size)
num_teeth = 12           # Number of teeth
pressure_angle = 20.0    # Pressure angle in degrees
face_width = 15.0        # Thickness of the gear
bore_diameter = 4.0      # Diameter of the central hole

# --- Calculations ---
# Standard spur gear nomenclature calculations
pitch_diameter = module * num_teeth
base_diameter = pitch_diameter * math.cos(math.radians(pressure_angle))
addendum = module
dedendum = 1.25 * module
root_diameter = pitch_diameter - 2 * dedendum
outside_diameter = pitch_diameter + 2 * addendum

# --- Involute Generation Function ---
def involute_point(base_radius, angle_rad):
    """Calculate a point on the involute curve."""
    # x = rb * (cos(t) + t * sin(t))
    # y = rb * (sin(t) - t * cos(t))
    x = base_radius * (math.cos(angle_rad) + angle_rad * math.sin(angle_rad))
    y = base_radius * (math.sin(angle_rad) - angle_rad * math.cos(angle_rad))
    return x, y

def create_tooth_profile():
    """Generates the 2D profile for a single gear tooth valley."""
    # Determine angular thickness of the tooth at the pitch circle
    # For a standard gear, tooth thickness = space width = pi * module / 2 (arc length)
    # Angle subtended by tooth thickness = (pi * module / 2) / (pitch_diameter / 2) = pi / N
    tooth_angle = math.pi / num_teeth 
    
    points = []
    
    # Generate involute points
    # We need to find the "t" (parameter) that corresponds to the root and outside diameters
    # R = sqrt(x^2 + y^2) = rb * sqrt(1 + t^2)
    # t = sqrt((R/rb)^2 - 1)
    
    base_radius = base_diameter / 2.0
    root_radius = root_diameter / 2.0
    outside_radius = outside_diameter / 2.0
    
    # Start t just slightly above base circle to avoid math issues if root < base
    start_r = max(base_radius, root_radius)
    t_start = math.sqrt((start_r/base_radius)**2 - 1)
    t_end = math.sqrt((outside_radius/base_radius)**2 - 1)
    
    # Resolution of the curve
    steps = 10
    
    # Right side involute
    right_side = []
    for i in range(steps + 1):
        t = t_start + (t_end - t_start) * (i / steps)
        x, y = involute_point(base_radius, t)
        right_side.append((x, y))
        
    # Rotate points to center the tooth on the Y axis
    # The involute starts at the X-axis. At pitch radius, the angle is inv_angle.
    # We want the pitch point to be at angle = tooth_angle / 4 (half the semi-thickness)
    # Pitch point parameter t_pitch
    t_pitch = math.sqrt(( (pitch_diameter/2.0) / base_radius )**2 - 1)
    pitch_x, pitch_y = involute_point(base_radius, t_pitch)
    current_angle_at_pitch = math.atan2(pitch_y, pitch_x)
    
    # We want the tooth centered on Y axis, so the flank crosses pitch circle at 
    # angle = 90 - (90/N) degrees? No, simpler:
    # Let's align the center of the TOOTH on the X-axis for simplicity in replication.
    # The half-thickness angle is tooth_angle / 2.
    # We need to rotate the generated involute so that at pitch radius, its angle is tooth_angle/4.
    
    rotation_offset = (tooth_angle / 2.0) - current_angle_at_pitch
    
    transformed_right = []
    for x, y in right_side:
        r = math.sqrt(x*x + y*y)
        ang = math.atan2(y, x)
        new_ang = ang + rotation_offset
        transformed_right.append((r * math.cos(new_ang), r * math.sin(new_ang)))

    # Mirror for left side
    transformed_left = []
    for x, y in reversed(transformed_right):
        transformed_left.append((x, -y))
        
    # Combine
    # If root circle is smaller than base circle, we need to extend down to root
    full_profile = []
    
    # Add bottom point of left flank (at root radius)
    l_x, l_y = transformed_left[0]
    if math.sqrt(l_x**2 + l_y**2) > root_radius:
         # Radial line down to root
         full_profile.append((root_radius * l_x / math.sqrt(l_x**2+l_y**2), root_radius * l_y / math.sqrt(l_x**2+l_y**2)))
    
    full_profile.extend(transformed_left)
    
    # Top land (arc or line connecting top of involutes) - usually just straight in CAD approximation or implied by next point
    
    full_profile.extend(transformed_right)
    
    # Add bottom point of right flank
    r_x, r_y = transformed_right[-1]
    if math.sqrt(r_x**2 + r_y**2) > root_radius:
        full_profile.append((root_radius * r_x / math.sqrt(r_x**2+r_y**2), root_radius * r_y / math.sqrt(r_x**2+r_y**2)))
        
    return full_profile

# --- Geometry Construction ---

# 1. Create the single tooth profile
tooth_pts = create_tooth_profile()

# 2. Create the gear profile sketch
# We construct one tooth, then polar array it
tooth_wire = cq.Workplane("XY").polyline(tooth_pts)

# Create the full gear profile by revolving/patterning
# CadQuery's gear generation is often easier with plugins, but here is a manual constructive method
# using the 'union' approach for robustness with custom shapes.

# Base cylinder (root diameter)
gear = cq.Workplane("XY").circle(root_diameter/2.0).extrude(face_width)

# Extrude the single tooth
single_tooth = cq.Workplane("XY").polyline(tooth_pts).close().extrude(face_width)

# Pattern the tooth
for i in range(num_teeth):
    angle = 360.0 / num_teeth * i
    rotated_tooth = single_tooth.rotate((0,0,0), (0,0,1), angle)
    gear = gear.union(rotated_tooth)

# 3. Create the bore hole
result = gear.faces(">Z").workplane().circle(bore_diameter / 2.0).cutThruAll()

# 4. Optional: Fillet the root for better look (visual only, simplified)
# result = result.edges("|Z").fillet(module * 0.1) 

# Export/Render
# if 'show_object' in globals():
#     show_object(result)