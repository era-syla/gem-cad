import cadquery as cq
import math

def timing_pulley_gt2(tooth_count=20, tooth_pitch=2.0, profile_height=16.0, 
                      flange_diameter=16.0, flange_thickness=1.0, 
                      hub_diameter=10.0, hub_height=6.0, 
                      bore_diameter=5.0):
    """
    Creates a parametric GT2-style timing pulley.
    
    Args:
        tooth_count: Number of teeth
        tooth_pitch: Distance between teeth (GT2 is 2mm)
        profile_height: Width of the toothed area (between flanges)
        flange_diameter: Outer diameter of the side flanges
        flange_thickness: Thickness of the flanges
        hub_diameter: Diameter of the protruding hub
        hub_height: Height of the protruding hub
        bore_diameter: Diameter of the central hole
    """

    # --- Calculations ---
    # Pitch Circle Diameter (PCD) = (Tooth Count * Pitch) / PI
    pcd = (tooth_count * tooth_pitch) / math.pi
    pitch_radius = pcd / 2.0
    
    # GT2 profile approximation parameters
    # The tooth shape is roughly a rounded trapezoid or semicircle.
    # For a procedural model, we'll cut simplified grooves.
    # Depth of cut for GT2 is approx 0.75mm
    tooth_depth = 0.75
    # The "valley" of the tooth is roughly half the pitch minus some clearance
    tooth_width = 1.2 # Approximation for the cut width at pitch line
    
    # Outer diameter is slightly smaller than PCD
    # For GT2-20T: PCD=12.73, OD~12.22 (so ~0.5mm less)
    outer_radius = (pcd - 0.508) / 2.0
    
    # --- Geometry Creation ---

    # 1. Main Body Cylinder (the core of the pulley)
    # Total length = flange + profile + flange + hub
    # We will build it up in sections along the Z axis
    
    # Section 1: First Flange
    pulley = cq.Workplane("XY").circle(flange_diameter / 2.0).extrude(flange_thickness)
    
    # Section 2: Toothed Area (Solid cylinder first)
    toothed_section = (
        cq.Workplane("XY")
        .workplane(offset=flange_thickness)
        .circle(outer_radius)
        .extrude(profile_height)
    )
    pulley = pulley.union(toothed_section)
    
    # Section 3: Second Flange
    second_flange = (
        cq.Workplane("XY")
        .workplane(offset=flange_thickness + profile_height)
        .circle(flange_diameter / 2.0)
        .extrude(flange_thickness)
    )
    pulley = pulley.union(second_flange)
    
    # Section 4: Hub
    hub = (
        cq.Workplane("XY")
        .workplane(offset=flange_thickness + profile_height + flange_thickness)
        .circle(hub_diameter / 2.0)
        .extrude(hub_height)
    )
    pulley = pulley.union(hub)
    
    # --- Creating Teeth ---
    # We will cut the teeth from the 'toothed_section' area.
    # We define a single cutting tool shape and polar array it.
    
    # Define a custom tooth cutter profile
    # It's shaped like the gap between the pulley teeth
    cut_depth_radius = outer_radius - tooth_depth
    
    # Shape of the cutter (trapezoid with rounded corners is typical, simple trapezoid here)
    # This sketch is drawn on the XZ plane, centered on the X-axis (radius)
    # Position: X = outer_radius, Z = middle of toothed section
    z_mid = flange_thickness + (profile_height / 2.0)
    
    # Creating a cutter solid to subtract
    cutter_profile = (
        cq.Workplane("XZ")
        .workplane(offset=0) # centered in Y
        .moveTo(outer_radius + 1.0, -tooth_width/2.0) # Start outside
        .lineTo(cut_depth_radius, -tooth_width/3.0)   # Bottom of groove
        .lineTo(cut_depth_radius, tooth_width/3.0)    # Bottom width
        .lineTo(outer_radius + 1.0, tooth_width/2.0)  # Top width
        .close()
        .extrude(profile_height * 3) # Make it long enough to cut through Z
    )
    
    # Center the cutter on the toothed section Z-wise
    # The extrusion above went from Y=0 to Y=length. We need to shift it.
    # Actually, simpler approach: create profile on XY, extrude, rotate, position.
    
    # Let's try a different approach: Sketch the profile on the top face of the toothed section
    # and cut downwards? No, the teeth run axially.
    # Sketch on XY plane? No, teeth are radial.
    
    # Standard CadQuery approach for gears/pulleys:
    # Create the cutter shape, move it to the radius, then use cut with polar array?
    # Or subtract a gear profile extruded axially? 
    # Extruding a 2D gear profile is cleanest. Let's rebuild the core.
    
    # --- REBUILDING CORE STRATEGY ---
    # It is cleaner to generate the toothed profile as a single sketch and extrude it,
    # rather than cutting slots.
    
    # Generate the 2D profile of the gear
    tooth_angle = 360.0 / tooth_count
    
    def tooth_profile(t_count, o_rad, root_rad, t_width_angular_deg):
        """Creates the scalloped outline of a timing pulley"""
        s = cq.Sketch()
        # Start with outer circle
        s = s.circle(o_rad)
        
        # Create a single cutter shape (the gap)
        # We model the negative space (the gap) to subtract from the circle
        # Gap shape: somewhat circular/trapezoidal
        gap_center_radius = o_rad
        gap_radius = (o_rad - root_rad) # rough depth
        
        # We will iterate and place cuts
        for i in range(t_count):
            angle = i * (360.0 / t_count)
            rad_angle = math.radians(angle)
            
            # Calculate position for a circular cutout (simplified GT2)
            cx = o_rad * math.cos(rad_angle)
            cy = o_rad * math.sin(rad_angle)
            
            # To simulate the trapezoidal/rounded GT2 gap:
            # We can cut with a small circle or polygon.
            # Let's use a rectangle/trapezoid moved to the edge
            
            # Using specific logic for the cut is tricky inside a single Sketch chain efficiently without plugins.
            # Let's go back to solid operations (cut).
            pass
        return s

    # --- Refined Strategy: Solid Operations ---
    
    # 1. Base shape again
    full_body = cq.Workplane("XY").circle(flange_diameter / 2.0).extrude(flange_thickness)
    
    # 2. Toothed Cylinder Core
    # We create a cylinder and cut grooves
    core_z_start = flange_thickness
    core = (
        cq.Workplane("XY")
        .workplane(offset=core_z_start)
        .circle(outer_radius)
        .extrude(profile_height)
    )
    
    # Define the cutter shape (a prism representing the gap between teeth)
    # We define it on XZ plane to cut along Z
    # Dimensions of the gap
    gap_w_top = 1.3
    gap_w_bottom = 0.8
    gap_depth = 0.75
    
    # Create one cutter
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=core_z_start - 1) # Start slightly below
        .moveTo(outer_radius + 0.5, -gap_w_top/2)
        .lineTo(outer_radius - gap_depth, -gap_w_bottom/2)
        .lineTo(outer_radius - gap_depth, gap_w_bottom/2)
        .lineTo(outer_radius + 0.5, gap_w_top/2)
        .close()
        .extrude(profile_height + 2) # Extrude well past the height
    )
    
    # Cut the teeth using polar array
    for i in range(tooth_count):
        angle = i * (360.0 / tooth_count)
        # Rotate cutter and subtract
        rotated_cutter = cutter.rotate((0,0,0), (0,0,1), angle)
        core = core.cut(rotated_cutter)
        
    full_body = full_body.union(core)
    
    # 3. Second Flange
    flange2 = (
        cq.Workplane("XY")
        .workplane(offset=core_z_start + profile_height)
        .circle(flange_diameter / 2.0)
        .extrude(flange_thickness)
    )
    full_body = full_body.union(flange2)
    
    # 4. Hub
    hub_z_start = core_z_start + profile_height + flange_thickness
    hub_part = (
        cq.Workplane("XY")
        .workplane(offset=hub_z_start)
        .circle(hub_diameter / 2.0)
        .extrude(hub_height)
    )
    full_body = full_body.union(hub_part)
    
    # 5. Bore
    full_body = full_body.faces(">Z").workplane().circle(bore_diameter / 2.0).cutThruAll()
    
    # 6. Fillets
    # Add a small fillet where the hub meets the flange for strength/aesthetics
    try:
        full_body = full_body.edges(
            cq.selectors.NearestToPointSelector((hub_diameter/2.0, 0, hub_z_start))
        ).fillet(0.5)
    except:
        pass # Skip fillet if geometry fails resolution

    return full_body

# Generate the model
# Parameters roughly estimated from a standard GT2 20-tooth 6mm belt pulley
result = timing_pulley_gt2(
    tooth_count=20,
    tooth_pitch=2.0,
    profile_height=7.0,     # Typical width for 6mm belt
    flange_diameter=16.0,   # Approx for 20T
    flange_thickness=1.0,
    hub_diameter=10.0,
    hub_height=6.5,
    bore_diameter=5.0
)

if 'show_object' in globals():
    show_object(result)