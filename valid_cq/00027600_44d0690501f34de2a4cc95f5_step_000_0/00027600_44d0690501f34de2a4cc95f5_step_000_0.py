import cadquery as cq
import math

# --- Parametric Dimensions ---
module = 1.0                # Metric gear module
num_teeth = 40              # Number of teeth
pressure_angle = 20.0       # Standard pressure angle in degrees
face_width = 10.0           # Thickness of the gear
bore_diameter = 12.0        # Diameter of the central hole
mount_hole_diameter = 4.0   # Diameter of the 4 surrounding holes
mount_hole_radius = 12.0    # Radius of the bolt circle for mounting holes
num_mount_holes = 5         # Number of mounting holes

# --- Gear Calculation Logic ---
# While CadQuery doesn't have a built-in "gear" primitive in the core library that returns a solid instantly,
# we can construct one mathematically.
# Basic Gear Formulas:
pitch_diameter = module * num_teeth
base_diameter = pitch_diameter * math.cos(math.radians(pressure_angle))
addendum = module
dedendum = 1.25 * module
outside_diameter = pitch_diameter + 2 * addendum
root_diameter = pitch_diameter - 2 * dedendum

def involute(radius, angle):
    """Calculate point on an involute curve."""
    x = radius * (math.cos(angle) + angle * math.sin(angle))
    y = radius * (math.sin(angle) - angle * math.cos(angle))
    return x, y

def generate_gear_profile(m, z, alpha=20):
    """
    Generates a 2D profile of a single gear tooth space and patterns it.
    m: module
    z: number of teeth
    alpha: pressure angle
    """
    r_pitch = (m * z) / 2.0
    r_base = r_pitch * math.cos(math.radians(alpha))
    r_addendum = r_pitch + m
    r_dedendum = r_pitch - 1.25 * m
    
    # Calculate angles
    # Tooth thickness at pitch circle is pi*m/2
    # Angle subtended by tooth thickness at pitch circle
    theta_pitch = (math.pi * m / 2.0) / r_pitch 
    
    # Involute angle at pitch circle
    inv_alpha = math.tan(math.radians(alpha)) - math.radians(alpha)
    
    # Angle offset for the involute start to center the tooth on X axis
    # The tooth symmetry line is at angle 0.
    # The involute starts at the base circle.
    # We need to find the angle at the base circle that results in the correct width at pitch circle.
    
    # Let's construct one side of the tooth and mirror it.
    points = []
    
    # Root fillet/bottom land (simplified as straight line here, or small arc)
    # Start slightly before the involute if base circle > dedendum circle
    
    # Resolution for involute curve
    steps = 10
    
    # Determine start and end angles for the involute parameter (u)
    # The involute function is defined by the parameter u (unrolling angle in radians)
    # Radius at a given u is r_base * sqrt(1 + u^2)
    # We need u such that radius goes from r_base (or r_dedendum) to r_addendum
    
    r_start = max(r_base, r_dedendum)
    
    # Calculate 'u' at r_start
    # r^2 = r_base^2 * (1 + u^2) => u = sqrt((r/r_base)^2 - 1)
    if r_start <= r_base:
        u_start = 0.0
    else:
        u_start = math.sqrt((r_start/r_base)**2 - 1)
        
    u_end = math.sqrt((r_addendum/r_base)**2 - 1)
    
    # Generate points for the right side of the tooth
    # We need to rotate these points so the tooth is centered.
    # The angle of the involute point (polar coord) is u - atan(u)
    # We want the thickness at pitch radius to be correct.
    # Angle of point at pitch radius = inv_alpha
    # We want this point to be at theta_pitch/2 relative to centerline.
    # So we rotate the whole curve by -(inv_alpha - theta_pitch/4)  <-- Approximation logic check
    
    # Better approach for CadQuery polylines:
    # 1. Create one involute flank.
    # 2. Rotate it to position.
    # 3. Mirror to make the tooth.
    
    # Angle where the involute profile intersects the pitch circle (relative to the base of the involute)
    # is inv_alpha.
    # Half angular width of tooth at pitch circle = (pi / (2*z))
    # Angular shift required = (pi / (2*z)) + inv_alpha
    
    shift_angle = (math.pi / (2.0 * z)) + inv_alpha
    
    right_flank = []
    
    # If dedendum is below base circle, add radial line segment
    if r_dedendum < r_base:
         right_flank.append((r_dedendum, 0)) # Placeholder, will rotate later
    
    dt = (u_end - u_start) / steps
    for i in range(steps + 1):
        u = u_start + i * dt
        x_inv = r_base * (math.cos(u) + u * math.sin(u))
        y_inv = r_base * (math.sin(u) - u * math.cos(u))
        right_flank.append((x_inv, y_inv))
        
    # Rotate flank points to correct position
    # The involute formula generates a curve starting at (r_base, 0) and winding CCW.
    # We want the right flank of a tooth centered on X+.
    # We rotate clockwise by shift_angle.
    
    rot_flank = []
    cos_shift = math.cos(-shift_angle)
    sin_shift = math.sin(-shift_angle)
    
    for x, y in right_flank:
        xr = x * cos_shift - y * sin_shift
        yr = x * sin_shift + y * cos_shift
        rot_flank.append((xr, yr))
        
    # If we started at r_dedendum < r_base, the first point is not connected to origin properly
    # Let's define the tooth profile
    
    # Final tooth points (CCW winding)
    # 1. Top Land (arc or line)
    # 2. Left Flank
    # 3. Bottom Land
    # 4. Right Flank
    
    # Actually, simpler to define one full tooth and wire it.
    
    # Left flank is mirror of Right flank over X axis
    left_flank = [(x, -y) for x, y in reversed(rot_flank)]
    
    # Assemble single tooth points
    tooth_points = rot_flank + left_flank
    
    return tooth_points, r_dedendum, r_addendum

# --- Building the Gear ---

# Instead of complex math from scratch, let's use CadQuery's parametric power.
# We will create a cylinder and cut the teeth slots, or extrude a 2D profile.
# Generating a true involute profile via spline is accurate.

def make_gear(m, z, h, alpha=20):
    r_pitch = (m * z) / 2.0
    r_base = r_pitch * math.cos(math.radians(alpha))
    r_addendum = r_pitch + m
    r_dedendum = r_pitch - 1.25 * m
    
    # Calculate Involute points for one side of a tooth
    # We solve for 1/4 of a tooth cycle (center of tooth to center of gap)
    
    # Angle corresponding to half-tooth-thickness at pitch circle
    # Tooth thickness t = pi * m / 2
    # Angle theta_t = t / r_pitch = pi / z
    # Half angle = pi / (2 * z)
    half_tooth_angle = math.pi / (2 * z)
    
    # Involute function angle at pitch radius
    inv_alpha = math.tan(math.radians(alpha)) - math.radians(alpha)
    
    # The involute curve starts at the base circle (angle 0 in calculation)
    # At pitch radius, the involute has unwound by inv_alpha.
    # We want the point at pitch radius to be at angle 'half_tooth_angle'
    # So we rotate the standard involute by beta
    beta = half_tooth_angle + inv_alpha
    
    points = []
    
    # If root circle is smaller than base circle, we need a radial line
    if r_dedendum < r_base:
        points.append((r_dedendum * math.cos(-beta), r_dedendum * math.sin(-beta)))
    
    # Sample the involute from base circle (or root) to addendum
    n_steps = 15
    
    # Determine u_max (at addendum)
    # r^2 = rb^2(1+u^2)
    u_max = math.sqrt((r_addendum/r_base)**2 - 1)
    
    # Determine u_min 
    u_min = 0
    if r_dedendum > r_base:
         u_min = math.sqrt((r_dedendum/r_base)**2 - 1)

    for i in range(n_steps + 1):
        u = u_min + (u_max - u_min) * (i / n_steps)
        # Standard involute coords
        x_val = r_base * (math.cos(u) + u * math.sin(u))
        y_val = r_base * (math.sin(u) - u * math.cos(u))
        
        # Rotate by -beta to position the flank
        x = x_val * math.cos(-beta) - y_val * math.sin(-beta)
        y = x_val * math.sin(-beta) + y_val * math.cos(-beta)
        points.append((x, y))
        
    # Mirror points to get the other side of the tooth
    # The current points define the right flank (y < 0 roughly)
    # We mirror across X-axis to get left flank
    upper_flank = [(x, -y) for x, y in reversed(points)]
    
    # Full tooth profile points
    tooth_profile = points + upper_flank
    
    # Create the tooth wire
    tooth = (cq.Workplane("XY")
             .polyline(tooth_profile)
             .close() # Close implicitly assumes straight line for top land?
                      # Polyline closes start to end. 
                      # But we have a gap at the root and a gap at the tip.
    )
    
    # Let's do it differently. Create the shape of the GEAR by subtracting gaps? 
    # Or creating a union of teeth?
    # Union of teeth on a cylinder is robust.
    
    # Let's fix the polyline to be a closed loop shape representing ONE TOOTH
    # We need to close the shape at the root (center of gear).
    tooth_poly = points + upper_flank
    tooth_poly.append((0,0)) # Go to center to make a pie wedge shape solid
    tooth_poly.insert(0, (0,0))
    
    single_tooth_wire = cq.Workplane("XY").polyline(tooth_poly).close()
    single_tooth = single_tooth_wire.extrude(h)
    
    # The top land is currently a straight line chord, which is close enough for visual models,
    # but strictly it should be an arc. 
    # For a high fidelity model, we intersect with the addendum cylinder.
    
    # Pattern the tooth
    gear_teeth = single_tooth.rotate((0,0,0), (0,0,1), 0).union(
        single_tooth.rotate((0,0,0), (0,0,1), 360/z)
    )
    
    # Efficient union via polar pattern usually works on features, 
    # but here we are unioning solids. CadQuery pattern logic:
    
    # Create the base cylinder (root to base)
    base_cyl = cq.Workplane("XY").circle(r_dedendum).extrude(h)
    
    # Create one tooth solid (wedge style)
    tooth_contour = (cq.Workplane("XY")
        .polyline(tooth_profile)
        .lineTo(0,0)
        .close()
        .extrude(h)
    )
    
    # Create the full gear using polar pattern of the tooth solid
    # We union all teeth
    import math
    angle_step = 360.0 / z
    
    # Accumulate the union
    final_gear = base_cyl
    for i in range(z):
        # Rotate the tooth solid
        rotated_tooth = tooth_contour.rotate((0,0,0), (0,0,1), i * angle_step)
        final_gear = final_gear.union(rotated_tooth)
        
    # Trim the outside to be a perfect circle (remove chords at top land)
    final_gear = final_gear.intersect(
        cq.Workplane("XY").circle(r_addendum).extrude(h)
    )
        
    return final_gear

# --- Main Construction ---

# 1. Generate the Gear Blank with Teeth
# Note: The 'make_gear' function above is logically sound but computationally heavy 
# due to looping unions. A faster way in CadQuery is creating a 2D sketch and extruding.

def make_gear_2d_profile(m, z, alpha=20):
    r_pitch = (m * z) / 2.0
    r_base = r_pitch * math.cos(math.radians(alpha))
    r_addendum = r_pitch + m
    r_dedendum = r_pitch - 1.25 * m
    
    half_tooth_angle = math.pi / (2 * z)
    inv_alpha = math.tan(math.radians(alpha)) - math.radians(alpha)
    beta = half_tooth_angle + inv_alpha
    
    u_max = math.sqrt((r_addendum/r_base)**2 - 1)
    u_min = 0
    if r_dedendum > r_base:
         u_min = math.sqrt((r_dedendum/r_base)**2 - 1)
         
    # Generate right flank points
    n_steps = 10
    flank_points = []
    
    # Add point at root if needed
    if r_dedendum < r_base:
        flank_points.append((r_dedendum * math.cos(-beta), r_dedendum * math.sin(-beta)))
        
    for i in range(n_steps + 1):
        u = u_min + (u_max - u_min) * (i / n_steps)
        x_val = r_base * (math.cos(u) + u * math.sin(u))
        y_val = r_base * (math.sin(u) - u * math.cos(u))
        
        x = x_val * math.cos(-beta) - y_val * math.sin(-beta)
        y = x_val * math.sin(-beta) + y_val * math.cos(-beta)
        flank_points.append((x, y))
        
    # Create the full points list for one tooth
    # Right flank (bottom to top) -> Top Land (implicit) -> Left Flank (top to bottom) -> Bottom Land (implicit)
    
    points_one_tooth = []
    points_one_tooth.extend(flank_points)
    
    # Mirror for left flank
    left_flank = [(x, -y) for x, y in reversed(flank_points)]
    points_one_tooth.extend(left_flank)
    
    # Now we need to replicate this pattern z times
    # This involves rotating the points and stitching them into one giant list
    
    full_gear_points = []
    angle_step = 2 * math.pi / z
    
    for i in range(z):
        theta = i * angle_step
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        
        # Rotate and append
        for x, y in points_one_tooth:
            rx = x * cos_t - y * sin_t
            ry = x * sin_t + y * cos_t
            full_gear_points.append((rx, ry))
            
    # Create the wire
    # Using spline makes it smooth, polyline is faster/easier for valid geometry
    return cq.Workplane("XY").polyline(full_gear_points).close()

# Create the base gear solid
gear_profile = make_gear_2d_profile(module, num_teeth, pressure_angle)
gear_solid = gear_profile.extrude(face_width)

# Cut the central bore
result = gear_solid.faces("<Z").workplane().circle(bore_diameter / 2.0).cutThruAll()

# Cut the mounting/lightening holes
# We use a polar pattern of circles
result = (result.faces("<Z").workplane()
          .polarArray(mount_hole_radius, 0, 360, num_mount_holes)
          .circle(mount_hole_diameter / 2.0)
          .cutThruAll())

# Clean up / Fillet (Optional, visual enhancement similar to image)
# The image shows slight chamfers or clean edges, but standard CAD keeps them sharp unless specified.
# We will leave edges sharp to ensure robust kernel execution.
