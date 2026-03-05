import cadquery as cq
import math

# --- Parameters ---
# Dimensions estimated from the visual representation
num_teeth = 20           # Number of teeth
module = 2.0             # Module (controls overall size)
pressure_angle = 20.0    # Pressure angle in degrees
cone_angle = 45.0        # Half-cone angle (45 degrees for miter gears)
face_width = 12.0        # Width of the gear face
bore_diameter = 12.0     # Central hole diameter
hub_diameter = 20.0      # Diameter of the inner hub/rim
hub_height = 5.0         # Height of the cylindrical base part inside

# Calculated parameters
pitch_radius = (num_teeth * module) / 2.0
outer_radius = pitch_radius + module # Approx addendum radius
root_radius = pitch_radius - (1.25 * module) # Approx dedendum radius

# --- Helper Functions ---

def involute_curve(radius, num_points=10):
    """Generates points for an involute curve."""
    points = []
    for i in range(num_points):
        # Parametric involute calculation
        t = i / (num_points - 1) * math.pi / 4  # Range of involute
        x = radius * (math.cos(t) + t * math.sin(t))
        y = radius * (math.sin(t) - t * math.cos(t))
        points.append((x, y))
    return points

def create_gear_tooth_profile(module, num_teeth, pressure_angle=20.0):
    """Creates a 2D profile of a single gear tooth gap."""
    pitch_radius = (num_teeth * module) / 2.0
    base_radius = pitch_radius * math.cos(math.radians(pressure_angle))
    addendum = module
    dedendum = 1.25 * module
    
    # Calculate angular widths
    pitch_circular_width = math.pi * module / 2.0 # Width of tooth at pitch circle
    pitch_angle_width = pitch_circular_width / pitch_radius # Angle in radians
    
    # Involute generation
    # We generate one side and mirror it
    involute_pts = involute_curve(base_radius, num_points=15)
    
    # Transform involute to start at the right angle relative to centerline
    # The involute starts at the base circle. We need to rotate it so the intersection
    # with the pitch circle creates the correct tooth width.
    
    # Find angle where involute crosses pitch radius (approximate)
    # inv(alpha) = tan(alpha) - alpha
    # angle at pitch circle = inv(pressure_angle)
    inv_alpha = math.tan(math.radians(pressure_angle)) - math.radians(pressure_angle)
    
    # The half-angle of the tooth at the base circle needs adjustment
    # Angle to rotate the involute:
    # half_tooth_angle_at_pitch = pitch_angle_width / 2
    # angular_offset = half_tooth_angle_at_pitch + inv_alpha
    
    angular_offset = (math.pi / (2 * num_teeth)) + inv_alpha
    
    # Generate the side profile points
    right_side = []
    for x, y in involute_pts:
        # Rotate point by -angular_offset
        r = math.sqrt(x**2 + y**2)
        theta = math.atan2(y, x)
        
        # Clip top and bottom
        if r < (pitch_radius - dedendum) or r > (pitch_radius + addendum):
            continue
            
        new_theta = theta - angular_offset
        nx = r * math.cos(new_theta)
        ny = r * math.sin(new_theta)
        right_side.append((nx, ny))

    # Add root and tip points
    # Root
    r_root = pitch_radius - dedendum
    right_side.insert(0, (r_root * math.cos(-angular_offset), r_root * math.sin(-angular_offset)))
    
    # Tip
    r_tip = pitch_radius + addendum
    # Extrapolate slightly or just take last point
    last_pt = right_side[-1]
    last_r = math.sqrt(last_pt[0]**2 + last_pt[1]**2)
    last_theta = math.atan2(last_pt[1], last_pt[0])
    right_side.append((r_tip * math.cos(last_theta), r_tip * math.sin(last_theta)))
    
    # Mirror for left side
    left_side = [(x, -y) for x, y in right_side]
    left_side.reverse()
    
    # Combine to form a wedge shape representing the *solid* tooth
    # To make the whole gear, we usually loft these
    return left_side + right_side

# --- Modeling Strategy ---
# 1. Create the base cone frustum shape.
# 2. Create a cutting tool representing the "gap" between teeth.
#    Since bevel gears are complex lofts, a simplified visual approximation 
#    often uses a lofted cut or an additive loft of teeth.
#    Here, we will create a single tooth solid using a loft from the outer back cone to the inner front cone.

# Back cone parameters (large end)
back_cone_radius = pitch_radius
back_cone_dist = back_cone_radius / math.tan(math.radians(cone_angle))

# Front cone parameters (small end)
# The face width determines where the front cone is
# By similar triangles:
front_cone_dist = back_cone_dist - (face_width * math.cos(math.radians(cone_angle)))
scale_factor = front_cone_dist / back_cone_dist
front_module = module * scale_factor

# Generate profiles
back_profile_pts = create_gear_tooth_profile(module, num_teeth, pressure_angle)
front_profile_pts = create_gear_tooth_profile(front_module, num_teeth, pressure_angle)

# Close the profiles to make wires
back_profile_pts.append(back_profile_pts[0])
front_profile_pts.append(front_profile_pts[0])

# Construct the single tooth solid
# The loft needs to be positioned correctly in 3D space
# The "Back" profile is at Z=0 (conceptually), Y radial
# Bevel gears are defined on cones. We place the profiles on planes perpendicular to the cone generatrix,
# or for simplicity in CAD, simply on Z planes and scale them, then rotate/loft.

# Let's use a simpler approach for a visual model:
# Loft two sketches separated by the face width projected along Z.
# Since it's a bevel gear, the 'front' profile is smaller and closer to the center.

# Define Workplanes for the loft
wp_back = cq.Workplane("XY").workplane(offset=0)
wp_front = cq.Workplane("XY").workplane(offset=face_width) # Simplified: Vertical loft for now, we will cut it later

# We need to construct wires for the loft
tooth_back = wp_back.polyline(back_profile_pts).close()
tooth_front = wp_front.polyline(front_profile_pts).close()

# Create one tooth
# Note: straight loft is an approximation, real bevels are spherical involutes.
single_tooth = cq.Workplane("XY").polyline(back_profile_pts).close().workplane(offset=face_width/math.cos(math.radians(cone_angle))).polyline(front_profile_pts).close().loft(combine=True)


# The tooth we just made is "standing up" along Z. 
# We need to rotate it to match the cone angle.
# Half cone angle is 45 deg.
# The tooth is currently generated along Z. We need to rotate it so its axis matches the cone surface.
# However, standard bevel gear generation in CadQuery often uses a subtractive method or a complex additive ring.

# --- Alternative simpler approach: Additive Ring of Teeth on a Cone ---

# Create the main conical body
# Base radius = pitch_radius approx. 
# Top radius = smaller due to cone angle.
height_cone = face_width * math.sin(math.radians(cone_angle)) # Axial height
base_r_cone = pitch_radius + module # Slightly larger for the backing
top_r_cone = base_r_cone - (face_width * math.cos(math.radians(cone_angle)))

# Main hub/body
gear_body = (cq.Workplane("XY")
    .circle(base_r_cone)
    .workplane(offset=height_cone)
    .circle(top_r_cone)
    .loft(combine=True)
)

# Cut the bore
gear_body = gear_body.faces("<Z").workplane().circle(bore_diameter/2).cutThruAll()

# Create the "Hub" depression on top
# Looking at the image, there's a rim.
inner_cut_depth = height_cone * 0.3
gear_body = gear_body.faces(">Z").workplane().circle(hub_diameter/2).cutBlind(-inner_cut_depth)

# Now, we cut the teeth "slots" instead of adding teeth.
# This ensures the conical shape is preserved.
# We define a "cutter" shape. A trapezoidal or triangular prism that tapers.

# Define the Cutter Profile (a V-shape gap)
# Gap width at pitch circle
pitch_circumference = 2 * math.pi * pitch_radius
tooth_width_arc = pitch_circumference / (2 * num_teeth) # Tooth thickness = Gap thickness approx
# Make the cutter slightly wider at top, narrower at bottom
gap_top_width = tooth_width_arc * 1.5 
gap_bottom_width = tooth_width_arc * 0.4
cut_depth = 2.25 * module

def make_cutter(scale=1.0):
    w_top = gap_top_width * scale
    w_bot = gap_bottom_width * scale
    depth = cut_depth * scale
    
    pts = [
        (-w_top/2, cut_depth/2), # Top Left relative to pitch line
        (w_top/2, cut_depth/2),  # Top Right
        (w_bot/2, -cut_depth/2), # Bottom Right
        (-w_bot/2, -cut_depth/2) # Bottom Left
    ]
    return pts

# Back Cutter (Large)
cutter_back_pts = make_cutter(1.0)
# Front Cutter (Small)
cutter_front_pts = make_cutter(scale_factor)

# Create the cutter solid
# Orientation: The cutter runs along the face width.
# We build it along Z, then rotate it 90 degrees to lie on the cone, then tilt by cone angle.
# Actually, easier to loft along Z, then rotate and subtract.

cutter_solid = (cq.Workplane("XY")
    .polyline(cutter_back_pts).close()
    .workplane(offset=face_width) # Length of the cut
    .polyline(cutter_front_pts).close()
    .loft()
)

# Position the cutter
# 1. Rotate 90 deg around X to lay flat-ish
# 2. Translate to pitch radius
# 3. Rotate by cone angle to align with the conical face
c_rot = cutter_solid.rotate((0,0,0), (1,0,0), -90)

# Move cutter to the edge of the gear
# Distance from center is roughly pitch radius
c_trans = c_rot.translate((0, pitch_radius, 0))

# Tilt the cutter to match the bevel angle
# The gear face is at 45 degrees. The cutter needs to plunge perpendicular to that or parallel?
# Bevel gears are cut radially towards the apex.
# The previous loft was linear. Let's adjust the position.
# The Apex of the cone is at (0,0, Z_apex).
# For a 45 deg gear, Z_apex = pitch_radius.
# We need to orient the cutter so it points at the apex.

# Let's simplify: Rotate the cutter by (90 - cone_angle) around X relative to the gear center?
# The cutter is currently horizontal along Y axis (after translate).
# We need to tilt the "tail" (Z=0 original) down and "head" (Z=face_width original) up?
# Or rather, the cutter represents the gap.

tilt_angle = 45 # for miter gear

# Adjust cutter:
# The loft axis is Y. Z is up.
# We need to tilt the whole cutter assembly around the X axis so it matches the cone slope.
final_cutter = c_trans.rotate((0,0,0), (1,0,0), -tilt_angle)

# Adjust height relative to Z=0
# The cutter is centered on its own Y axis. We need to shift it up so the "pitch line" matches the cone surface.
# The cutter depth is `cut_depth`. We want the middle of that to align roughly with the surface?
# Usually, pitch line is somewhat below the outer surface.
z_offset = module
final_cutter = final_cutter.translate((0, 0, z_offset))

# Perform cuts in a pattern
final_gear = gear_body
for i in range(num_teeth):
    angle = i * (360.0 / num_teeth)
    # Rotate the cutter around Z for each tooth position
    rotated_cutter = final_cutter.rotate((0,0,0), (0,0,1), angle)
    final_gear = final_gear.cut(rotated_cutter)

# Refine the central hub area based on image
# The image shows a flat top face on the inner hub, and the teeth start outside a specific radius.
# We create a union with a clean hub to cover messy roots.
hub_cleaner = (cq.Workplane("XY")
    .workplane(offset=height_cone - 1.0)
    .circle(hub_diameter/2 + 1.0) # Slightly larger than the cut
    .extrude(2.0)
)
# Make the hub tapered to blend
hub_cone = (cq.Workplane("XY")
    .circle(hub_diameter/2 + 4)
    .workplane(offset=height_cone)
    .circle(hub_diameter/2)
    .loft()
).cut(cq.Workplane("XY").circle(bore_diameter/2).extrude(100)) # Re-cut bore

# Combine
result = final_gear.union(hub_cone)

# Fillet the bore edge for a finished look
result = result.edges(cq.selectors.RadiusNthSelector(0)).fillet(0.5)

# --- Final Output ---
result = result