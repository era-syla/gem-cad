import cadquery as cq
import math

def chainring_generator(
    num_teeth=32,
    thickness=3.0,
    narrow_width=2.0,
    wide_width=3.6,
    chain_pitch=12.7, # 1/2 inch in mm
    roller_diameter=7.75,
    crank_interface="direct_mount"
):
    """
    Generates a bicycle chainring with narrow-wide teeth profile.
    """
    
    # --- derived calculations ---
    # Pitch Circle Diameter
    pcd = chain_pitch / math.sin(math.pi / num_teeth)
    radius = pcd / 2.0
    
    # Root radius (approximate)
    root_radius = radius - (roller_diameter / 2.0) - 0.5
    outer_radius = radius + (roller_diameter / 2.0) + 1.5
    
    # --- Geometry construction ---

    # 1. Base Disc
    # We create the main ring body first
    ring = cq.Workplane("XY").circle(outer_radius).extrude(thickness)
    
    # 2. Teeth Generation (Narrow-Wide profile)
    # This is a simplified tooth profile for visualization
    tooth_height = outer_radius - root_radius
    tooth_base_width = chain_pitch * 0.45
    
    def create_tooth_profile(is_wide):
        """Creates a single tooth shape as a wire"""
        # Define tooth points relative to center of tooth at root radius
        t_w_half = tooth_base_width / 2.0
        tip_w_half = tooth_base_width / 4.0
        
        pts = [
            (-t_w_half, 0),          # Base left
            (-tip_w_half, tooth_height), # Tip left
            (tip_w_half, tooth_height),  # Tip right
            (t_w_half, 0)            # Base right
        ]
        
        # Create the profile
        t = (cq.Workplane("XY")
             .workplane(offset=0)
             .polyline(pts).close()
             .extrude(thickness)
            )
            
        # Move tooth out to the correct radius
        t = t.translate((0, root_radius, 0))
        
        # Chamfer the wide teeth or cut the narrow teeth
        current_width = thickness
        target_width = wide_width if is_wide else narrow_width
        
        cut_depth = (thickness - target_width) / 2.0
        
        if cut_depth > 0:
            # Cut from both sides to thin the tooth
            cut_box = cq.Workplane("XY").box(chain_pitch, tooth_height*2, cut_depth)
            
            # Front cut
            cut_front = cut_box.translate((0, root_radius + tooth_height/2, thickness - cut_depth/2))
            # Back cut
            cut_back = cut_box.translate((0, root_radius + tooth_height/2, cut_depth/2))
            
            t = t.cut(cut_front).cut(cut_back)
            
            # Add chamfers to the tips for smooth engagement
            # This is complex in basic CSG, simplified here by tapering the extrusion if needed
            # but usually handled by chamfering edges.
        
        return t

    # Generate all teeth and fuse them
    teeth_solid = None
    
    for i in range(num_teeth):
        is_wide = (i % 2 == 0)
        tooth = create_tooth_profile(is_wide)
        
        # Rotate tooth to position
        angle = 360.0 / num_teeth * i
        tooth = tooth.rotate((0,0,0), (0,0,1), angle + 90) # Adjust +90 to align 0 deg to Y axis
        
        if teeth_solid is None:
            teeth_solid = tooth
        else:
            teeth_solid = teeth_solid.union(tooth)

    # Union the teeth ring with the base disc, but first we need to trim the base disc
    # so the teeth sit on top properly. 
    # Actually, better strategy: Create a solid ring up to root radius, then add teeth.
    
    base_ring = cq.Workplane("XY").circle(root_radius).extrude(thickness)
    main_body = base_ring.union(teeth_solid)
    
    # 3. Cutouts (The "Spokes")
    # We want roughly 8 spokes based on the image
    num_spokes = 8
    spoke_angle = 360 / num_spokes
    
    # Radii for the cutouts
    inner_cut_radius = 28.0
    outer_cut_radius = root_radius - 8.0 # Leave a rim
    
    # Define a trapezoidal cutout shape
    cutout_pts = [
        (10, inner_cut_radius), 
        (18, outer_cut_radius),
        (-18, outer_cut_radius),
        (-10, inner_cut_radius)
    ]
    
    cutout_shape = (cq.Workplane("XY")
                    .polyline(cutout_pts).close()
                    .extrude(thickness)
                    )
    
    # Apply fillets to the cutout corners before rotating
    cutout_shape = cutout_shape.edges("|Z").fillet(3.0)

    # Perform the polar array cut
    for i in range(num_spokes):
        rot_angle = i * spoke_angle
        rotated_cutout = cutout_shape.rotate((0,0,0), (0,0,1), rot_angle)
        main_body = main_body.cut(rotated_cutout)

    # 4. Central Interface (Direct Mount Spline)
    # Simplified spline pattern (e.g., SRAM/Cinch style approximation)
    center_hole_radius = 20.0
    spline_outer_radius = 24.0
    num_splines = 12 # Simplified count
    
    # Create the central hole
    center_hole = cq.Workplane("XY").circle(center_hole_radius).extrude(thickness)
    main_body = main_body.cut(center_hole)
    
    # Create the spline cutouts
    spline_tooth = (cq.Workplane("XY")
                    .rect(5, 5) # Small rectangle for spline notch
                    .translate((0, center_hole_radius, 0)) # Move to edge
                    .extrude(thickness)
                   )
    
    # Usually 3 small lobes, one big lobe pattern. We will do a regular pattern for generic look.
    for i in range(num_splines):
        # We model the negative space (the notch)
        rot_angle = i * (360.0 / num_splines)
        notch = spline_tooth.rotate((0,0,0), (0,0,1), rot_angle)
        main_body = main_body.cut(notch)
        
    # Add a recessed area around the mounting splines (often seen on these rings)
    recess_radius = 35.0
    recess_depth = 1.0
    recess = cq.Workplane("XY").workplane(offset=thickness-recess_depth).circle(recess_radius).extrude(recess_depth)
    
    # But we want to keep material where the spokes connect, so we only recess the inner ring area
    # This logic is tricky with unions. Let's instead cut a chamfer/relief on the inner edge.
    
    # 5. Pocketing / Reliefs (Aesthetic and weight saving)
    # The image shows pockets on the spokes.
    
    # Let's add a slight pocket on the face of the spokes
    pocket_depth = 0.8
    pocket_shape = cutout_shape # Reuse the cutout geometry but inverted somewhat?
    # No, it's easier to create a new shape that represents the solid spoke, scale it down, and cut.
    # Given the complexity, we will skip intricate pocketing inside the spokes and focus on chamfers.
    
    # 6. Final Details (Chamfers/Fillets)
    # Fillet the inner corners of the cutouts on the main body
    # Selecting edges is sensitive, let's try a general fillet on the inner faces
    
    # Chamfer the outer edge of the teeth ring (aesthetic)
    # This is hard to select procedurally on complex unions.
    
    # Apply a chamfer to the central hole edge
    main_body = main_body.faces(">Z").edges(cq.selectors.RadiusNthSelector(0)).chamfer(0.5)

    return main_body

# Generate the model
result = chainring_generator()