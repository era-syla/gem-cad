import cadquery as cq
from math import cos, sin, pi, radians, sqrt

def involute_gear(num_teeth, modulus, pressure_angle=20.0, face_width=5.0):
    """
    Creates a simple involute spur gear.
    
    :param num_teeth: Number of teeth
    :param modulus: Module of the gear (pitch diameter / num_teeth)
    :param pressure_angle: Pressure angle in degrees
    :param face_width: Thickness of the gear
    :return: A CadQuery Workplane object representing the gear
    """
    
    # Calculate gear parameters
    pitch_diameter = modulus * num_teeth
    base_diameter = pitch_diameter * cos(radians(pressure_angle))
    addendum = modulus
    dedendum = 1.25 * modulus
    outer_diameter = pitch_diameter + 2 * addendum
    root_diameter = pitch_diameter - 2 * dedendum
    
    # Tooth profile calculation
    # We will generate points for one tooth flank and mirror it
    points = []
    
    # Involute curve generation
    # Angle where the involute starts on the base circle
    num_points = 20
    
    # Calculate the angle span of the involute part we need
    # The involute needs to go from the base circle (or root circle) to the outer circle
    # Calculate max pressure angle at the tip
    max_pressure_angle_rad = c = cq.Workplane("XY")
    
    # Let's use a simpler approximation approach for robust code generation 
    # or use the built-in parametric curve if possible. 
    # However, constructing a precise involute curve point-by-point is standard.
    
    # Tooth thickness angle at pitch circle
    # Arc length of tooth thickness = pi * m / 2
    # Angle = (pi * m / 2) / (pitch_diameter / 2) = pi / num_teeth
    tooth_thickness_angle = pi / num_teeth
    
    # Involute function: inv(alpha) = tan(alpha) - alpha
    def inv(alpha):
        return cq.tan(alpha) - alpha

    # Calculate the angle offset for the involute curve so the tooth is centered on X axis
    # The intersection of the involute with the pitch circle determines the offset.
    # At pitch radius R, the pressure angle is alpha.
    # The polar angle theta = inv(alpha).
    # We want the tooth thickness at pitch radius to be centered.
    # Half tooth thickness angle = pi / (2 * N)
    # So the involute origin angle on base circle relative to center line = pi/(2*N) + inv(pressure_angle)
    
    alpha_pitch = radians(pressure_angle)
    base_radius = base_diameter / 2.0
    pitch_radius = pitch_diameter / 2.0
    outer_radius = outer_diameter / 2.0
    root_radius = root_diameter / 2.0
    
    # Angle offset to center the tooth
    inv_alpha_pitch = cq.tan(alpha_pitch) - alpha_pitch
    half_tooth_angle = pi / (2 * num_teeth)
    beta = half_tooth_angle + inv_alpha_pitch 
    
    # Generate points for the right flank of the tooth
    flank_points = []
    
    # We define the involute from the base circle up to the outer circle
    # Parameter t goes from 0 to t_max
    # r = Rb / cos(alpha) -> alpha = acos(Rb/r)
    # theta = inv(alpha)
    
    # Start slightly above base radius to avoid numerical issues if base < root
    start_r = max(base_radius, root_radius)
    
    r_step = (outer_radius - start_r) / (num_points - 1)
    
    for i in range(num_points):
        r = start_r + i * r_step
        if r < base_radius: 
            alpha = 0
        else:
            alpha = cq.acos(base_radius / r)
        
        theta = cq.tan(alpha) - alpha
        
        # Current polar coordinates: (r, theta)
        # We need to rotate this by -beta so the tooth is symmetric around X-axis
        # Wait, standard involute starts at theta=0 at base circle.
        # We want the right flank. 
        # The angle of the point is theta_point = -beta + theta
        
        theta_point = theta - beta
        x = r * cos(theta_point)
        y = r * sin(theta_point)
        flank_points.append((x, y))

    # Mirror for left flank
    left_flank_points = [(x, -y) for x, y in reversed(flank_points)]
    
    # Construct the full tooth shape
    # 1. Root circle segment from previous tooth (handled by logic or simple line)
    # 2. Left flank
    # 3. Top land (arc on outer circle)
    # 4. Right flank
    # 5. Root circle segment to next tooth
    
    # Actually, simpler to define one tooth as a wire and polar array it
    
    # Create the wire for one tooth
    # Start at root radius
    root_angle_span = 2 * pi / num_teeth
    
    # Calculate angular width of the tooth at the root circle to determine spacing
    # This is complex to get exact. Let's build the profile and loft/extrude.
    
    # Better approach with CadQuery: Define the points for one tooth, 
    # then replicate and connect.
    
    # Let's adjust points to ensure closed loop
    # Bottom of right flank
    br_x, br_y = flank_points[0]
    # Top of right flank
    tr_x, tr_y = flank_points[-1]
    # Top of left flank
    tl_x, tl_y = left_flank_points[0]
    # Bottom of left flank
    bl_x, bl_y = left_flank_points[-1]
    
    # We need to connect the bottom of the right flank of tooth i 
    # to the bottom of the left flank of tooth i+1
    
    all_points = []
    
    for i in range(num_teeth):
        angle_offset = 2 * pi * i / num_teeth
        
        # Rotate and append right flank points
        for x, y in flank_points:
            # Rotate (x,y) by angle_offset
            rx = x * cos(angle_offset) - y * sin(angle_offset)
            ry = x * sin(angle_offset) + y * cos(angle_offset)
            all_points.append((rx, ry))
            
        # Rotate and append left flank points
        # Note: left flank points are ordered top-to-bottom
        for x, y in left_flank_points:
            rx = x * cos(angle_offset) - y * sin(angle_offset)
            ry = x * sin(angle_offset) + y * cos(angle_offset)
            all_points.append((rx, ry))
            
    # Create the spline
    # Note: CadQuery spline might need tweaking for sharp corners at root
    # Ideally we use splines for flanks and arcs for root/tip, but a single polyline/spline 
    # with enough resolution is fine for visual representation.
    
    gear_profile = cq.Workplane("XY").polyline(all_points).close()
    
    # Extrude
    gear = gear_profile.extrude(face_width)
    
    return gear

# --- Parametric Dimensions ---
module = 2.0             # Scales the size of the teeth
pressure_angle = 20.0    # Standard pressure angle
thickness = 10.0         # Thickness of the gears

# Gear 1 (Large)
n_teeth_1 = 20
pitch_radius_1 = (module * n_teeth_1) / 2

# Gear 2 (Small)
n_teeth_2 = 12
pitch_radius_2 = (module * n_teeth_2) / 2

# Center distance
center_distance = pitch_radius_1 + pitch_radius_2

# --- Generate Gears ---

# Create the large gear
# Since building a custom involute from scratch in raw code can be verbose and prone to 
# small geometric errors without a robust library, we will use a simpler approximation 
# that generates a valid visual gear shape using CadQuery's gear plugin logic simplified 
# or constructing it manually as defined above.

# Let's refine the manual generation to be robust for the result variable.
def make_gear_shape(num_teeth, module, thickness):
    # Parameters
    root_radius = (module * num_teeth) / 2 - 1.25 * module
    base_radius = (module * num_teeth) / 2 * cos(radians(20))
    outer_radius = (module * num_teeth) / 2 + module
    
    # We will construct a single tooth profile and array it
    path = cq.Workplane("XY")
    
    # A simplified trapezoidal tooth for robustness if involute math fails silently
    # But let's try a decent approximation with splines
    
    points = []
    res = 10 # resolution per flank
    
    # One tooth sector angle
    sector = 2 * pi / num_teeth
    
    for i in range(num_teeth):
        angle_center = i * sector
        
        # Build one tooth
        # We need roughly 4 key points: Root-Left, Tip-Left, Tip-Right, Root-Right
        # But relative to the angle_center
        
        # Approximate angular widths
        # At root, width is approx larger
        # At tip, width is smaller
        
        # Width angles (half-widths)
        half_angle_root = (pi / num_teeth) * 0.7  # Heuristic gap
        half_angle_tip = (pi / num_teeth) * 0.3   # Heuristic tip thickness
        
        # Coordinates
        # Root Left
        rl_angle = angle_center - half_angle_root
        rl_x = root_radius * cos(rl_angle)
        rl_y = root_radius * sin(rl_angle)
        
        # Tip Left
        tl_angle = angle_center - half_angle_tip
        tl_x = outer_radius * cos(tl_angle)
        tl_y = outer_radius * sin(tl_angle)
        
        # Tip Right
        tr_angle = angle_center + half_angle_tip
        tr_x = outer_radius * cos(tr_angle)
        tr_y = outer_radius * sin(tr_angle)
        
        # Root Right
        rr_angle = angle_center + half_angle_root
        rr_x = root_radius * cos(rr_angle)
        rr_y = root_radius * sin(rr_angle)
        
        # Append for polyline
        points.extend([(rl_x, rl_y), (tl_x, tl_y), (tr_x, tr_y), (rr_x, rr_y)])
        
    return cq.Workplane("XY").polyline(points).close().extrude(thickness)

# Create Gear 1
gear1 = make_gear_shape(n_teeth_1, module, thickness)

# Create Gear 2
gear2 = make_gear_shape(n_teeth_2, module, thickness)

# Position Gear 2
# We need to rotate Gear 2 slightly so teeth mesh
# The angle to rotate is half a tooth pitch usually: 360 / (2 * n_teeth)
rotation_angle = 180.0 / n_teeth_2 
gear2 = gear2.rotate((0,0,0), (0,0,1), rotation_angle)
gear2 = gear2.translate((center_distance, 0, 0))

# Combine
result = gear1.union(gear2)