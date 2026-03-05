import cadquery as cq
import math

def bevel_gear(m=2, n_teeth=20, pressure_angle=20, cone_angle=45, face_width=10, bore_d=10):
    """
    Creates a simplified straight bevel gear.
    
    Parameters:
    - m: Module (size of teeth)
    - n_teeth: Number of teeth
    - pressure_angle: Pressure angle in degrees
    - cone_angle: Pitch cone angle in degrees (half-angle of the cone)
    - face_width: Width of the gear face
    - bore_d: Diameter of the central hole
    """
    
    # Calculate derived parameters
    pitch_radius = (m * n_teeth) / 2.0
    cone_dist = pitch_radius / math.sin(math.radians(cone_angle))
    
    # Base circle radius (used for involute profile approximation)
    base_radius = pitch_radius * math.cos(math.radians(pressure_angle))
    
    # Tooth dimensions
    addendum = m
    dedendum = 1.25 * m
    root_radius = pitch_radius - dedendum
    outer_radius = pitch_radius + addendum
    
    # --- Step 1: Create the Tooth Profile ---
    # We will approximate the involute profile with a trapezoid for simplicity in this parametric model,
    # as generating a true spherical involute is complex. 
    # This profile is drawn on the "back cone" plane.
    
    # Width of the tooth at the pitch circle
    circular_pitch = math.pi * m
    tooth_thickness_angle = (circular_pitch / 2) / pitch_radius # in radians
    
    # Define points for a single tooth cross-section (trapezoidal approximation)
    # Coordinates are essentially polar converted to cartesian on the XY plane
    # The profile is centered on the X-axis
    
    # Points on the pitch circle
    pitch_p1 = (pitch_radius * math.cos(tooth_thickness_angle/2), pitch_radius * math.sin(tooth_thickness_angle/2))
    pitch_p2 = (pitch_radius * math.cos(-tooth_thickness_angle/2), pitch_radius * math.sin(-tooth_thickness_angle/2))
    
    # Rough approximation of tip and root width based on pressure angle
    tip_width_half = (circular_pitch/4) - (addendum * math.tan(math.radians(pressure_angle)))
    root_width_half = (circular_pitch/4) + (dedendum * math.tan(math.radians(pressure_angle)))
    
    # Create the 2D sketch of the tooth + gear body segment
    # We need a closed wire representing the gear cross-section "slice"
    
    # Create the basic gear blank cone profile first to subtract material from, 
    # or build the teeth additively. 
    # Let's try the lofting approach: Create a large profile and a small profile and loft them towards the apex.
    
    # --- Better Approach: Lofting wire profiles towards the center ---
    
    def create_gear_profile(radius_scale=1.0):
        """Creates the 2D profile of the gear teeth at a specific scaling factor."""
        
        # Scale all radial dimensions
        r_pitch = pitch_radius * radius_scale
        r_root = (pitch_radius - dedendum) * radius_scale
        r_outer = (pitch_radius + addendum) * radius_scale
        
        # Calculate angular widths (constant regardless of scale)
        # Tooth thickness (arc length) scales, but the angle subtended is constant
        half_thick_angle = (math.pi / n_teeth) / 2 # Half the angle of one tooth
        
        # Pressure angle effect on tooth width at top and bottom
        # This is an angular offset
        ang_offset = (math.tan(math.radians(pressure_angle)) * addendum) / pitch_radius
        ang_offset_root = (math.tan(math.radians(pressure_angle)) * dedendum) / pitch_radius
        
        top_half_angle = half_thick_angle - ang_offset
        root_half_angle = half_thick_angle + ang_offset_root
        
        # Points for one tooth
        # We'll create points for all teeth
        pts = []
        
        for i in range(n_teeth):
            angle_center = i * (2 * math.pi / n_teeth)
            
            # Tip points
            a1 = angle_center - top_half_angle
            a2 = angle_center + top_half_angle
            pts.append((r_outer * math.cos(a1), r_outer * math.sin(a1)))
            pts.append((r_outer * math.cos(a2), r_outer * math.sin(a2)))
            
            # Root points (connect to next tooth)
            a3 = angle_center + root_half_angle
            
            # Calculate start of next tooth root
            next_angle_center = (i + 1) * (2 * math.pi / n_teeth)
            a4 = next_angle_center - root_half_angle
            
            pts.append((r_root * math.cos(a3), r_root * math.sin(a3)))
            pts.append((r_root * math.cos(a4), r_root * math.sin(a4)))
            
        return pts

    # --- Geometry Generation ---
    
    # 1. Define the scaling for the "front" and "back" of the bevel gear
    # The back is at cone_dist
    # The front is at cone_dist - face_width
    
    scale_back = 1.0
    scale_front = (cone_dist - face_width) / cone_dist
    
    # Generate point lists
    pts_back = create_gear_profile(scale_back)
    pts_front = create_gear_profile(scale_front)
    
    # 2. Position the profiles in 3D space
    # The Apex of the cone is at (0,0,0)
    # The gear axis is Z
    # We need to position the profiles at the correct Z height based on the cone angle
    
    # Z-height for the back face (largest diameter)
    z_back = cone_dist * math.cos(math.radians(cone_angle))
    # Z-height for the front face (smallest diameter)
    z_front = (cone_dist - face_width) * math.cos(math.radians(cone_angle))
    
    # Create the solid gear teeth by lofting
    teeth = (
        cq.Workplane("XY")
        .workplane(offset=z_front)
        .polyline(pts_front).close()
        .workplane(offset=z_back - z_front)
        .polyline(pts_back).close()
        .loft(combine=True)
    )
    
    # 3. Create the inner solid (the hub/web under the teeth to make it solid)
    # It's a cone frustum matching the root diameter
    r_root_back = (pitch_radius - dedendum)
    r_root_front = r_root_back * scale_front
    
    # We extend the bottom slightly to ensure clean boolean operations if needed, 
    # but the image shows a relatively flat back. Let's add a backing plate.
    
    # Backing (mounting face) thickness
    backing_thickness = m * 2
    
    # Create the main conical body underneath the teeth
    body_cone = cq.Solid.makeCone(r_root_front, r_root_back, z_back - z_front).translate((0,0,z_front))
    
    # Combine teeth and body
    gear_solid = teeth.union(cq.Workplane(obj=body_cone))
    
    # 4. Add the mounting hub/backing
    # The image shows the gear teeth end, and there is a flat surface or slight recess.
    # Usually bevel gears have a cylindrical extension on the back for a set screw.
    # Let's add a simple backing cylinder that tapers into the gear.
    
    # However, looking at the specific image provided:
    # It looks like a "miter gear" (1:1 ratio, 45 deg).
    # There is a flat recessed area in the front face.
    
    # Recess on the front face (small end)
    recess_d = r_root_front * 1.5
    recess_depth = face_width * 0.2
    
    # Cut the bore
    result = gear_solid.faces("<Z").workplane().circle(bore_d/2).cutThruAll()
    
    # Cut a recess in the front face (smaller face)
    # Note: loft direction was z_front to z_back (bottom to top).
    # z_front is the small diameter (bottom in construction, but visual top in image potentially)
    # Let's orient it so Z-up is the apex.
    
    # Actually, standard is Z is axis. 
    # Let's add the distinctive recess seen in the image on the larger face (the back face usually)
    # In the image, we see the "front" of the gear (the smaller cone face is inside, larger is outside).
    # Wait, the image shows the *face* of the gear. The teeth radiate outwards. 
    # The inner circle is a recess.
    
    # Let's clarify orientation:
    # The "top" of the image is the large diameter back face? No, usually bevel gears are depicted showing the teeth.
    # The image shows the converging teeth. The center is "lower" than the rim.
    # This means we are looking at the "front" (small end) or a recessed back.
    # Given the geometry of bevel gears, the visible face with the bore is usually the mounting distance face.
    
    # Let's just apply a cut to the geometric center to mimic the image's hub.
    
    # Create a cut-out for the inner hub area
    hub_radius = pitch_radius * 0.4
    hub_depth = face_width * 0.4
    
    result = (
        result
        .faces(">Z") # Select the large face (back)
        .workplane()
        .circle(hub_radius)
        .cutBlind(-hub_depth)
    )
    
    # 5. Flip it to match the visual perspective (Large face down, small face up?)
    # The image looks like the large diameter is the base, tapering up to a smaller diameter.
    # Our construction has z_front (small) at Low Z? No:
    # z_back is at high Z (large diameter). z_front is at low Z (small diameter).
    # Loft went Front -> Back.
    # So Small -> Large.
    # The image shows the large diameter at the bottom? 
    # It looks like a "crown" shape. 
    # The large diameter is the outer rim. The teeth slope *inward* and *downward* towards the center hole.
    # This implies the Apex is "down".
    
    # Let's rotate the result so the Apex points roughly down, matching the "bowl" look.
    result = result.rotate((0,0,0), (1,0,0), 180)

    return result

# Parameters to match the visual style of the image
# High tooth count, approx 45 degree angle
result = bevel_gear(
    m=2.0,            # Module
    n_teeth=24,       # Number of Teeth
    pressure_angle=20,# Standard pressure angle
    cone_angle=45,    # 45 degrees makes it a miter gear
    face_width=12,    # Length of the tooth
    bore_d=8          # Central shaft hole
)

# Export or Render helper (not executed in silent mode, but good for context)
# show_object(result)