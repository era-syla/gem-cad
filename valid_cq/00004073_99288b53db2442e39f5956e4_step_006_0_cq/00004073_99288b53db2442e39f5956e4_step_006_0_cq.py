import cadquery as cq
import math

def involute_gear(module, num_teeth, thickness, pressure_angle=20.0, clearance=0.0,
                  bore_diameter=0.0, keyway_width=0.0, keyway_height=0.0):
    """
    Creates a simple spur gear with an involute profile and optional bore/keyway.
    
    Args:
        module: The gear module (pitch diameter / num_teeth)
        num_teeth: Number of teeth
        thickness: Gear face width
        pressure_angle: Pressure angle in degrees
        clearance: Bottom clearance
        bore_diameter: Diameter of center hole (0 for none)
        keyway_width: Width of the keyway (0 for none)
        keyway_height: Height of the keyway into the hub (0 for none)
        
    Returns:
        A CadQuery Workplane object representing the gear
    """
    
    # Calculate geometric parameters
    pitch_radius = (module * num_teeth) / 2.0
    base_radius = pitch_radius * math.cos(math.radians(pressure_angle))
    addendum = module
    dedendum = 1.25 * module + clearance
    outer_radius = pitch_radius + addendum
    root_radius = pitch_radius - dedendum
    
    # Generate the profile for a single tooth
    # We construct points for one side of the involute, mirror it, and join
    points = []
    
    # Resolution for the involute curve
    steps = 15
    
    # Create the involute curve
    # Angle where the involute profile starts (at base circle)
    # to where it ends (at outer circle)
    
    # Iterate through the involute curve
    for i in range(steps + 1):
        # r varies from base_radius to outer_radius
        # However, if base_radius > root_radius, we need to handle the flank below base circle
        # For simplicity in this procedural generation, we start the involute at base_radius 
        # (or root_radius if base is smaller, though physically involute starts at base)
        r = base_radius + (outer_radius - base_radius) * (i / steps)
        
        # Involute angle calculation: alpha = pressure angle at radius r
        alpha = math.acos(base_radius / r)
        # Involute function: inv(alpha) = tan(alpha) - alpha
        inv_alpha = math.tan(alpha) - alpha
        
        # We need the polar coordinate theta for this radius
        # We shift the coordinate system so the center of the tooth is at angle 0
        # Tooth thickness at pitch circle is (pi * m) / 2
        # Angular semi-thickness at pitch circle
        s_pitch = (math.pi * module) / 2
        phi_pitch = s_pitch / pitch_radius # angle subtended by half tooth thickness
        
        # Involute angle at pitch radius
        alpha_pitch = math.acos(base_radius / pitch_radius)
        inv_alpha_pitch = math.tan(alpha_pitch) - alpha_pitch
        
        # Theta for the current point r
        theta = (inv_alpha_pitch - inv_alpha) + (phi_pitch / 2)
        
        # Convert polar to cartesian
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        points.append((x, y))

    # Add the root point (connecting to the root circle) if base radius > root radius
    if base_radius > root_radius:
        points.insert(0, (root_radius * math.cos(points[0][2] if len(points)>0 and len(points[0])>2 else math.atan2(points[0][1], points[0][0])), 
                          root_radius * math.sin(points[0][2] if len(points)>0 and len(points[0])>2 else math.atan2(points[0][1], points[0][0]))))

    # Create the tooth shape by mirroring
    # Convert points to Vector objects for easier manipulation if needed, but tuples work for polyline
    
    # To define the full gear, we need to draw the profile in a sketch and polar array it
    # But constructing a robust involute from scratch with lines/splines can be tricky in pure code
    # without a dedicated gear generator.
    # CadQuery often has a parametric gear plugin, but here we will approximate closely
    # using a dedicated high-level approach or manual construction.
    
    # Let's use a simpler, cleaner approach: construct one tooth wire, then pattern.
    
    # 1. Define one flank
    flank_pts = points
    
    # 2. Define top land (arc at outer radius)
    # The current points end at one side of the top land.
    # We need to mirror this flank across the X axis (y=0) to get the other side
    
    top_pt = flank_pts[-1]
    bottom_pt = flank_pts[0]
    
    # Mirror flank points across X axis
    mirrored_flank_pts = [(x, -y) for x, y in reversed(flank_pts)]
    
    # Combine to make a full tooth shape (open at the bottom)
    tooth_pts = mirrored_flank_pts + flank_pts
    
    # We need to rotate this tooth so the gap is correct when arrayed
    # Current tooth is centered on X axis (angle 0).
    # Angular pitch = 360 / num_teeth
    
    # Let's create the solid using the efficient built-in extrusion of a sketch
    
    # Construct the sketch for the gear profile
    s = cq.Sketch()
    
    angle_step = 360.0 / num_teeth
    
    for i in range(num_teeth):
        rotation_angle = i * angle_step
        
        # Rotate the generated single-tooth points
        rad = math.radians(rotation_angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        rotated_tooth = []
        for px, py in tooth_pts:
            rx = px * cos_a - py * sin_a
            ry = px * sin_a + py * cos_a
            rotated_tooth.append((rx, ry))
            
        # Add tooth segment
        if i == 0:
            s = s.push([rotated_tooth[0]])
        
        # Draw the tooth profile (spline for smooth involute approximation)
        s = s.spline(rotated_tooth)
        
        # Draw the root arc to the next tooth
        # Calculate start of next tooth
        next_angle = (i + 1) * angle_step
        rad_next = math.radians(next_angle)
        
        # Start point of next tooth (corresponding to bottom_pt of original profile, rotated)
        # Original bottom_pt is (root_radius * cos(theta_max), -root_radius * sin(theta_max)) essentially
        # We need the first point of the next iteration's mirrored flank
        
        # Simply, we draw an arc from the end of this tooth to the start of the next 
        # The end of this tooth is rotated_tooth[-1]
        
        # But wait, the loop logic above draws the tooth points. We need to connect them.
        # It's safer to generate ALL points for the entire gear perimeter first, then make one wire.
        pass

    # REVISED STRATEGY: 
    # Generating raw points for involutes manually is error-prone without a library.
    # Let's use CadQuery's parametric curve capabilities or a simpler approximation 
    # that visually matches the request perfectly.
    
    # Based on the image: 
    # 1. Roughly 12 teeth.
    # 2. Significant central bore.
    # 3. Rectangular keyway.
    
    # Let's use a simpler geometric construction for the tooth that is topologically robust.
    # We will build one tooth sector and polar array it.
    
    sector_angle = 360.0 / num_teeth
    half_sector = sector_angle / 2.0
    
    # Construct a single tooth wire
    # Points definition
    r_root = root_radius
    r_outer = outer_radius
    r_pitch = pitch_radius
    
    # Angular widths (approximate for visual accuracy based on standard gear theory)
    # At pitch circle, tooth and gap are equal.
    # Angle of half tooth at pitch circle
    half_tooth_angle = 360.0 / (4 * num_teeth) # 90 degrees of the sector/pitch
    
    # Define key points in polar coordinates (radius, angle_degrees)
    # Center of tooth is at angle 0
    
    # P1: Root start (left)
    t1 = -half_sector
    # P2: Tooth base start (left) - transition from root circle to involute
    t2 = -half_tooth_angle * 1.5 # slightly wider at base
    # P3: Pitch point (left)
    t3 = -half_tooth_angle
    # P4: Tip start (left)
    t4 = -half_tooth_angle * 0.6 # narrower at top
    # P5: Tip end (left) - center of tip is 0
    t5 = 0
    
    # Convert polar (r, theta_deg) to cartesian (x, y)
    def p2c(r, theta_deg):
        rad = math.radians(theta_deg)
        return (r * math.cos(rad), r * math.sin(rad))

    pt_root_start = p2c(r_root, -half_sector)
    pt_base_start = p2c(r_root, t2)
    pt_pitch = p2c(r_pitch, t3)
    pt_tip_start = p2c(r_outer, t4)
    pt_tip_mid = p2c(r_outer, 0)
    
    # Create the wire for half a tooth
    # Root arc
    # Flank spline
    # Top Land (we'll just make the spline go to the top center)
    
    # Using CadQuery Sketch is the most robust way to fuse this
    s = cq.Sketch()
    
    # Draw one full gear profile by repeating a logic
    full_wire_pts = []
    
    for i in range(num_teeth):
        mid_angle = i * sector_angle
        
        # Angle offsets relative to the tooth center
        # We model the tooth as a spline going: Root -> Pitch -> Tip -> Pitch -> Root
        
        # Coordinates relative to tooth center
        # Root Left
        a_rl = mid_angle - (sector_angle * 0.5)
        # Involute Start Left (approx at root)
        a_isl = mid_angle - (sector_angle * 0.35)
        # Tip Left
        a_tl = mid_angle - (sector_angle * 0.15)
        # Tip Right
        a_tr = mid_angle + (sector_angle * 0.15)
        # Involute Start Right
        a_isr = mid_angle + (sector_angle * 0.35)
        # Root Right (next sector start)
        a_rr = mid_angle + (sector_angle * 0.5)

        p_rl = p2c(r_root, a_rl)
        p_isl = p2c(r_root, a_isl)
        p_pitch_l = p2c(r_pitch, mid_angle - (sector_angle * 0.25))
        p_tl = p2c(r_outer, a_tl)
        p_tr = p2c(r_outer, a_tr)
        p_pitch_r = p2c(r_pitch, mid_angle + (sector_angle * 0.25))
        p_isr = p2c(r_root, a_isr)
        
        # We need tangents or extra control points to make it look like a gear
        # Spline Points for this tooth
        tooth_spline = [p_isl, p_pitch_l, p_tl, p_tr, p_pitch_r, p_isr]
        
        # Add arc for root (from previous tooth end to this tooth start)
        # If it's the first tooth, we just start the list.
        # If it's subsequent, we need an arc from last point to p_isl
        
        if i == 0:
            full_wire_pts.extend(tooth_spline)
        else:
            # We connect previous p_isr to current p_isl with an arc/line
            # Here we just add the points to a big spline list for simplicity
            # To get distinct root radius, we explicitly add points on the root circle
            
            # Midpoint between teeth on root circle
            a_root_mid = mid_angle - (sector_angle * 0.5)
            p_root_mid = p2c(r_root, a_root_mid)
            
            # Insert root points before the tooth points
            full_wire_pts.append(p_root_mid)
            full_wire_pts.extend(tooth_spline)

    # Close the loop
    a_last_root = 360 - (sector_angle * 0.5)
    full_wire_pts.append(p2c(r_root, a_last_root))
    
    # Extrude the gear
    gear_solid = (cq.Workplane("XY")
                  .spline(full_wire_pts, includeCurrent=True).close()
                  .extrude(thickness)
                 )

    # Cut Bore
    if bore_diameter > 0:
        gear_solid = gear_solid.faces("<Z").workplane().circle(bore_diameter/2).cutThruAll()
        
    # Cut Keyway
    if keyway_width > 0 and keyway_height > 0:
        # Keyway is typically cut from the bore upwards
        # Center of keyway at top of bore (Y axis)
        
        # Calculate keyway rectangle position
        # The keyway sits at the top of the bore (radius = bore_diameter/2)
        # Width is centered on Y axis
        # Height is measured from the bore circumference or center? 
        # Standard: keyway depth is often given from the bore edge.
        # We will assume keyway_height is the depth of cut INTO the solid from the bore radius.
        
        kw_w = keyway_width
        kw_h = (bore_diameter / 2.0) + keyway_height # Total height from center
        
        # Cut profile: A rectangle centered on Y axis, starting at center, going up
        gear_solid = (gear_solid.faces("<Z").workplane()
                      .moveTo(0, (bore_diameter/2.0) + (keyway_height/2.0))
                      .rect(kw_w, keyway_height)
                      .cutThruAll()
                      )

    return gear_solid

# --- Parametric Configuration ---
# Parameters estimated from the image
module = 2.0
num_teeth = 12
pressure_angle = 20.0
gear_thickness = 25.0

# Calculated dimensions for bore and keyway based on visual proportion
pitch_dia = module * num_teeth # 24mm
root_dia = pitch_dia - (2 * 1.25 * module) # approx 19mm
outer_dia = pitch_dia + (2 * module) # 28mm

bore_dia = 12.0 # Looks like about half the pitch diameter
keyway_w = 3.0
keyway_h = 1.5 # Depth into the hub material

# --- Model Generation ---

result = involute_gear(
    module=module,
    num_teeth=num_teeth,
    thickness=gear_thickness,
    pressure_angle=pressure_angle,
    bore_diameter=bore_dia,
    keyway_width=keyway_w,
    keyway_height=keyway_h
)