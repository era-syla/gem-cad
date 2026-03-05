import cadquery as cq
import math

def create_bender():
    # --- Parameters ---
    # Body
    body_dia_top = 30.0
    body_dia_bot = 26.0
    body_height = 40.0
    
    # Head
    head_dia = 20.0
    head_cyl_height = 15.0
    antenna_rod_h = 5.0
    antenna_rod_r = 0.5
    antenna_bulb_r = 1.5
    visor_protrusion = 6.0
    visor_width = 16.0
    visor_height = 8.0
    
    # Legs
    leg_length = 40.0
    leg_dia = 7.0
    leg_spacing = 14.0
    foot_dia_base = 15.0
    foot_dia_top = 7.0
    foot_height = 4.0
    
    # Arms
    arm_dia = 5.0
    shoulder_dia = 7.0
    arm_length_straight = 30.0
    hand_dia = 6.0
    finger_length = 3.0
    finger_dia = 1.2
    
    # --- Construction ---

    # 1. Torso (Main Body)
    # The body is slightly tapered, wider at top than bottom
    torso = cq.Workplane("XY").circle(body_dia_bot/2).workplane(offset=body_height).circle(body_dia_top/2).loft(combine=True)
    
    # 2. Door/Chest Detail (Optional but nice for likeness)
    # A simple cut or protrusion for the door
    door_width = body_dia_bot * 0.6
    door_height = body_height * 0.7
    door = (cq.Workplane("XZ")
            .workplane(offset=body_dia_bot/2 - 2) # Position slightly inside
            .center(0, body_height/2)
            .rect(door_width, door_height)
            .extrude(5) # Extrude out
            .intersect(torso) # Keep only part inside/on surface
           )
    # Actually, a simple flat cut or slight inset looks better for the door outline
    # Let's skip complex boolean for the door to keep the mesh clean and focus on the main shape
    
    # 3. Head Assembly
    # The head sits on top of the torso. Often there is a slight shoulder/neck taper.
    shoulder_plate_h = 2.0
    shoulders = (cq.Workplane("XY")
                 .workplane(offset=body_height)
                 .circle(body_dia_top/2)
                 .workplane(offset=shoulder_plate_h)
                 .circle(head_dia/2)
                 .loft(combine=True))
    
    head_base_z = body_height + shoulder_plate_h
    head_cylinder = (cq.Workplane("XY")
                     .workplane(offset=head_base_z)
                     .circle(head_dia/2)
                     .extrude(head_cyl_height))
    
    head_dome = (cq.Workplane("XY")
                 .workplane(offset=head_base_z + head_cyl_height)
                 .sphere(head_dia/2)
                 .cut(cq.Workplane("XY").workplane(offset=head_base_z + head_cyl_height).rect(100,100).extrude(-100))) # Half sphere
    
    # Antenna
    antenna_base = (cq.Workplane("XY")
                    .workplane(offset=head_base_z + head_cyl_height + head_dia/2)
                    .circle(antenna_rod_r * 2) # small base
                    .extrude(1))
    
    antenna_rod = (cq.Workplane("XY")
                   .workplane(offset=head_base_z + head_cyl_height + head_dia/2)
                   .circle(antenna_rod_r)
                   .extrude(antenna_rod_h))
    
    antenna_bulb = (cq.Workplane("XY")
                    .workplane(offset=head_base_z + head_cyl_height + head_dia/2 + antenna_rod_h)
                    .sphere(antenna_bulb_r))

    # Eyes/Visor Area
    # Create a box protruding from the head
    visor = (cq.Workplane("XY")
             .workplane(offset=head_base_z + head_cyl_height/2)
             .center(0, head_dia/3) # Shift forward in Y
             .box(visor_width, visor_protrusion, visor_height)
             )
    # Fillet the visor edges to make it look like the casing
    visor = visor.edges("|Z").fillet(1.0)
    
    head_assembly = shoulders.union(head_cylinder).union(head_dome).union(antenna_base).union(antenna_rod).union(antenna_bulb).union(visor)

    # 4. Legs
    def create_leg(x_offset):
        # Path for the leg - slightly curved or straight. The image shows slight curve.
        path = (cq.Workplane("XZ")
                .moveTo(x_offset, 0)
                .spline([(x_offset * 1.2, -leg_length/2), (x_offset, -leg_length)], includeCurrent=True))
        
        leg = (cq.Workplane("XY")
               .workplane(offset=0)
               .circle(leg_dia/2)
               .sweep(path, isFrenet=True))
        
        # Foot
        foot_z = -leg_length
        foot = (cq.Workplane("XY")
                .workplane(offset=foot_z)
                .circle(foot_dia_base/2)
                .workplane(offset=foot_height)
                .circle(foot_dia_top/2)
                .loft(combine=True))
        
        # Position foot relative to leg end (sweep ends can be tricky, approximating x pos)
        # Since spline returns roughly to x_offset, we center foot there.
        foot = foot.translate((x_offset - foot.val().Center().x, 0, 0))
        
        return leg.union(foot)

    left_leg = create_leg(-leg_spacing/2)
    right_leg = create_leg(leg_spacing/2)

    # 5. Arms
    def create_arm(is_right):
        side_factor = 1 if is_right else -1
        shoulder_z = body_height * 0.85
        shoulder_y = 0
        shoulder_x = (body_dia_top/2) * side_factor
        
        # Shoulder socket
        shoulder = (cq.Workplane("YZ")
                    .workplane(offset=shoulder_x) # Start from side of body
                    .circle(shoulder_dia/2)
                    .extrude(side_factor * 2) # Extrude outwards slightly
                    )
        
        # Arm Path: Down and slightly outward
        # Start point needs to be relative to the sweep plane
        path = (cq.Workplane("XZ")
                .moveTo(shoulder_x + (side_factor * 2), shoulder_z)
                .spline([(shoulder_x + (side_factor * 8), shoulder_z - arm_length_straight/2), 
                         (shoulder_x + (side_factor * 6), shoulder_z - arm_length_straight)], includeCurrent=True))
        
        arm_tube = (cq.Workplane("XY")
                    .workplane(offset=shoulder_z) # Plane to start sweep profile
                    .center(shoulder_x + (side_factor * 2), 0)
                    .circle(arm_dia/2)
                    .sweep(path, isFrenet=True))
        
        # Hand (Cuff)
        end_point = path.val().endPoint()
        hand_cuff = (cq.Workplane("XY")
                     .workplane(offset=end_point.z)
                     .center(end_point.x, end_point.y)
                     .circle(arm_dia/2 + 1) # Top of cuff
                     .workplane(offset=-2)
                     .circle(hand_dia/2 + 2) # Bottom of flared cuff
                     .loft())
        
        # Fingers (simplified as small cylinders)
        fingers = cq.Workplane("XY").workplane(offset=end_point.z - 2)
        finger_solids = []
        for i in range(3):
            angle = math.radians(i * 120 + (0 if is_right else 60))
            fx = end_point.x + math.cos(angle) * (hand_dia/2)
            fy = end_point.y + math.sin(angle) * (hand_dia/2)
            f = (cq.Workplane("XY")
                 .workplane(offset=end_point.z - 2)
                 .center(fx, fy)
                 .circle(finger_dia/2)
                 .extrude(-finger_length))
            finger_solids.append(f)
            
        full_arm = shoulder.union(arm_tube).union(hand_cuff)
        for f in finger_solids:
            full_arm = full_arm.union(f)
            
        return full_arm

    right_arm = create_arm(True)
    left_arm = create_arm(False)

    # Combine everything
    final_model = torso.union(head_assembly).union(left_leg).union(right_leg).union(right_arm).union(left_arm)
    
    return final_model

result = create_bender()