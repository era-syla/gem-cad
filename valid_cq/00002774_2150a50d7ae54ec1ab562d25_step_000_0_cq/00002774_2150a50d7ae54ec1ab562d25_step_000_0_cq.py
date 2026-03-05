import cadquery as cq
import math

def create_carburetor():
    # --- Parameters ---
    # Main Body
    body_width = 16.0
    body_height = 20.0
    body_length = 22.0
    body_fillet = 0.5
    
    # Air Intake (Top)
    intake_outer_diam = 12.0
    intake_inner_diam = 9.0
    intake_height = 5.0
    intake_lip_height = 1.0
    intake_lip_diam = 13.0
    
    # Lower Outlet
    outlet_diam = 10.0
    outlet_height = 6.0
    
    # Side Needle Valve Assembly (Right side)
    needle_housing_diam = 14.0
    needle_housing_thickness = 2.0
    needle_stem_diam = 3.0
    needle_stem_length = 15.0
    needle_knob_diam = 8.0
    needle_knob_length = 5.0
    
    # Throttle Lever Assembly (Front face)
    throttle_boss_diam = 8.0
    throttle_boss_height = 3.0
    throttle_nut_hex_size = 6.0
    throttle_nut_height = 3.0
    throttle_shaft_diam = 4.0
    
    lever_thickness = 1.0
    lever_width = 4.0
    lever_length_segment1 = 8.0
    lever_angle_segment2 = 45 # degrees
    lever_length_segment2 = 10.0
    lever_hole_diam = 2.0
    
    # Idle Screw (Top-Front Corner)
    idle_screw_diam = 3.0
    idle_screw_head_diam = 4.5
    idle_screw_height = 6.0

    # --- Geometry Construction ---

    # 1. Main Block Body
    # We start with a cube and fillet the vertical edges
    main_body = (
        cq.Workplane("XY")
        .box(body_length, body_width, body_height)
        .edges("|Z")
        .fillet(1.0)
    )

    # 2. Air Intake (Top Cylinder)
    # Cylinder on top face
    intake = (
        cq.Workplane("XY")
        .workplane(offset=body_height / 2)
        .circle(intake_outer_diam / 2)
        .extrude(intake_height)
    )
    
    # Lip on the intake
    intake_lip = (
        cq.Workplane("XY")
        .workplane(offset=body_height / 2 + intake_height - intake_lip_height)
        .circle(intake_lip_diam / 2)
        .extrude(intake_lip_height)
    )
    
    # Cut the throat (venturi)
    # We'll cut this later to ensure it goes through everything

    # 3. Lower Outlet (Bottom Cylinder)
    outlet = (
        cq.Workplane("XY")
        .workplane(offset=-body_height / 2)
        .circle(outlet_diam / 2)
        .extrude(-outlet_height)
    )

    # 4. Needle Valve Side (Right Face)
    # The knurled housing right against the body
    needle_housing = (
        cq.Workplane("YZ")
        .workplane(offset=body_length / 2)
        .circle(needle_housing_diam / 2)
        .extrude(needle_housing_thickness)
    )
    
    # The threaded stem
    needle_stem = (
        cq.Workplane("YZ")
        .workplane(offset=body_length / 2 + needle_housing_thickness)
        .circle(needle_stem_diam / 2)
        .extrude(needle_stem_length)
    )
    
    # The knob at the end
    needle_knob = (
        cq.Workplane("YZ")
        .workplane(offset=body_length / 2 + needle_housing_thickness + needle_stem_length - needle_knob_length)
        .circle(needle_knob_diam / 2)
        .extrude(needle_knob_length)
    )
    
    # Add texture/knurls to the knob (simplified as cuts)
    knob_cuts = (
        cq.Workplane("YZ")
        .workplane(offset=body_length / 2 + needle_housing_thickness + needle_stem_length - needle_knob_length)
        .polarArray(needle_knob_diam/2, 0, 360, 12)
        .circle(0.5)
        .extrude(needle_knob_length)
    )
    needle_knob = needle_knob.cut(knob_cuts)

    # A small tip at the very end of the needle
    needle_tip = (
         cq.Workplane("YZ")
        .workplane(offset=body_length / 2 + needle_housing_thickness + needle_stem_length)
        .circle(2.0)
        .extrude(2.0)
    )

    # 5. Throttle Lever Assembly (Front Face)
    # Boss on the front face
    throttle_boss = (
        cq.Workplane("XZ")
        .workplane(offset=-body_width / 2)
        .center(0, -2) # Shift down slightly relative to center
        .circle(throttle_boss_diam / 2)
        .extrude(-throttle_boss_height)
    )
    
    # Create the bent lever using a path sweep
    # Define the path for the lever
    lever_path_pts = [
        (0, 0, 0),
        (0, -lever_length_segment1, 0),
        (0, -lever_length_segment1 - lever_length_segment2 * math.cos(math.radians(lever_angle_segment2)), 
             -lever_length_segment2 * math.sin(math.radians(lever_angle_segment2)))
    ]
    
    # We construct the lever geometry relative to the boss
    lever_workplane = (
        cq.Workplane("YZ")
        .workplane(offset=-(body_length/2) + 5) # Position horizontally
        .workplane(offset=-(body_width/2) - throttle_boss_height - lever_thickness) # Position depth-wise
    )
    
    # Simply modeling the lever as a union of boxes/extrusions for robustness instead of a complex sweep
    # Segment 1 (Vertical-ish)
    lever_seg1 = (
        cq.Workplane("XZ")
        .workplane(offset=-body_width / 2 - throttle_boss_height)
        .center(0, -2) # Match boss center
        .rect(lever_width, lever_width) # Center hub of lever
        .extrude(-lever_thickness)
    )
    
    lever_arm1 = (
        cq.Workplane("XZ")
        .workplane(offset=-body_width / 2 - throttle_boss_height)
        .center(0, -2)
        .center(0, -lever_length_segment1/2)
        .rect(lever_width, lever_length_segment1)
        .extrude(-lever_thickness)
    )

    # Segment 2 (Angled)
    # Calculate offset for the end of segment 1
    seg2_start_y = -2 - lever_length_segment1
    
    lever_arm2 = (
        cq.Workplane("XZ")
        .workplane(offset=-body_width / 2 - throttle_boss_height)
        .center(0, seg2_start_y)
        .transformed(rotate=(0, 0, -30)) # Angle the arm
        .center(0, -lever_length_segment2/2)
        .rect(lever_width, lever_length_segment2)
        .extrude(-lever_thickness)
    )
    
    # End hole on lever
    lever_end_pos = lever_arm2.faces("<Z").val().Center()
    
    # The actual hole needs to be cut from the union later, but let's make the round end
    lever_end_round = (
        cq.Workplane("XZ")
        .workplane(offset=-body_width / 2 - throttle_boss_height)
        .center(0, seg2_start_y)
        .transformed(rotate=(0, 0, -30))
        .center(0, -lever_length_segment2)
        .circle(lever_width/2)
        .extrude(-lever_thickness)
    )

    # Nut holding the lever
    throttle_nut = (
        cq.Workplane("XZ")
        .workplane(offset=-body_width / 2 - throttle_boss_height - lever_thickness)
        .center(0, -2)
        .polygon(6, throttle_nut_hex_size)
        .extrude(-throttle_nut_height)
    )
    
    throttle_screw_head = (
        cq.Workplane("XZ")
        .workplane(offset=-body_width / 2 - throttle_boss_height - lever_thickness - throttle_nut_height)
        .center(0, -2)
        .circle(throttle_shaft_diam / 2)
        .extrude(-1.5) # Screw head height
    )
    
    # Slot in screw head
    screw_slot = (
        cq.Workplane("XZ")
        .workplane(offset=-body_width / 2 - throttle_boss_height - lever_thickness - throttle_nut_height - 1.5)
        .center(0, -2)
        .rect(throttle_shaft_diam + 2, 0.8)
        .extrude(1.0)
    )
    throttle_screw_head = throttle_screw_head.cut(screw_slot)


    # 6. Idle Screw (Top Front Left)
    idle_screw_base = (
        cq.Workplane("XY")
        .workplane(offset=body_height/2)
        .center(-body_length/3, -body_width/3)
        .circle(idle_screw_head_diam/2)
        .extrude(2.0)
    )
    
    idle_screw_slot = (
        cq.Workplane("XY")
        .workplane(offset=body_height/2 + 2.0)
        .center(-body_length/3, -body_width/3)
        .rect(idle_screw_head_diam + 1, 0.8)
        .extrude(-1.0)
    )
    
    idle_screw = idle_screw_base.cut(idle_screw_slot)
    
    # Make a small support boss for the idle screw
    idle_boss = (
        cq.Workplane("XY")
        .workplane(offset=body_height/2 - 2)
        .center(-body_length/3, -body_width/3)
        .rect(5, 5)
        .extrude(2)
    )


    # --- Combine and Refine ---

    # Combine main parts
    carb = main_body.union(intake).union(intake_lip).union(outlet)
    carb = carb.union(needle_housing).union(needle_stem).union(needle_knob).union(needle_tip)
    carb = carb.union(throttle_boss).union(lever_seg1).union(lever_arm1).union(lever_arm2).union(lever_end_round)
    carb = carb.union(throttle_nut).union(throttle_screw_head)
    carb = carb.union(idle_boss).union(idle_screw)

    # 7. Internal Cuts (Bore)
    # Main Venturi through hole
    venturi_cut = (
        cq.Workplane("XY")
        .workplane(offset=body_height / 2 + intake_height + 5)
        .circle(intake_inner_diam / 2)
        .extrude(-(body_height + intake_height + outlet_height + 10))
    )
    
    # Apply chamfer to the top of the intake for the velocity stack look
    carb = carb.edges(cq.selectors.NearestToPointSelector((0, 0, body_height/2 + intake_height))).fillet(0.5)

    # Cut the hole in the lever arm
    lever_hole_cut = (
        cq.Workplane("XZ")
        .workplane(offset=-body_width / 2 - throttle_boss_height - 5) # Start cutting from outside
        .center(0, seg2_start_y)
        .transformed(rotate=(0, 0, -30))
        .center(0, -lever_length_segment2)
        .circle(lever_hole_diam/2)
        .extrude(10) # Cut inwards
    )

    # Horizontal bore for the throttle barrel
    throttle_bore = (
        cq.Workplane("YZ")
        .circle(10.0 / 2) # Internal barrel diameter
        .extrude(body_length + 10, both=True)
    )

    final_carb = carb.cut(venturi_cut).cut(throttle_bore).cut(lever_hole_cut)
    
    # Add a horizontal seam line on the main body to simulate split casting or detail
    seam = (
        cq.Workplane("XY")
        .rect(body_length + 1, body_width + 1)
        .extrude(0.2)
        .translate((0, 0, 0)) # At Z=0
    )
    # We don't cut, we just leave it or maybe add a tiny chamfer. 
    # Let's add a small fillet to the main body edges for realism
    # final_carb = final_carb.edges("|Z").fillet(0.5) # Already done on base block

    return final_carb

result = create_carburetor()