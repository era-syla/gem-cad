import cadquery as cq
import math

def create_model():
    # --- Parameters ---
    # Drum dimensions
    drum_radius = 25.0
    drum_height = 60.0
    wall_thickness = 1.0
    rim_height = 3.0
    rim_thickness = 2.0
    
    # Lid dimensions
    lid_thickness = 1.5
    lid_overhang = 1.0
    handle_radius = 1.0
    handle_height = 4.0
    
    # Frame/Chassis dimensions
    frame_tube_size = 2.5
    frame_width = 40.0 # Distance between handles roughly
    handle_length = 80.0
    handle_curve_start = 30.0
    axle_height = 10.0 # Height of the bottom frame from ground (relative)
    
    # Reinforcement ribs on the drum
    rib_width = 2.0
    rib_depth = 1.5
    rib_length = drum_height * 0.7
    num_ribs = 6

    # --- 1. The Drum ---
    # Main cylinder body
    drum_outer = cq.Workplane("XY").circle(drum_radius).extrude(drum_height)
    # Hollow it out (shell)
    # Alternatively, create inner cylinder and cut. Let's do simple cylinder for outer look
    # Since we need to attach ribs, a solid is easier to work with initially, but for visual accuracy:
    drum_inner = cq.Workplane("XY").workplane(offset=wall_thickness).circle(drum_radius - wall_thickness).extrude(drum_height)
    drum = drum_outer.cut(drum_inner)

    # Top Rim
    rim = (cq.Workplane("XY")
           .workplane(offset=drum_height - rim_height)
           .circle(drum_radius + rim_thickness)
           .circle(drum_radius - wall_thickness) # Keep inner diameter same
           .extrude(rim_height))
    
    drum = drum.union(rim)

    # Vertical Ribs
    # These look like stamped indentations or welded ribs. Let's model them as external ribs.
    rib_profile = cq.Workplane("XY").rect(rib_width, rib_depth)
    
    ribs = cq.Workplane("XY")
    for i in range(num_ribs):
        angle = i * (360.0 / num_ribs)
        # Create a rib at the correct angle
        # Position slightly below the rim
        r = (cq.Workplane("XY")
             .workplane(offset=drum_height - rim_height - rib_length)
             .transformed(rotate=cq.Vector(0, 0, angle))
             .center(drum_radius, 0)
             .rect(rib_depth * 2, rib_width) # Rect centered on radius edge
             .extrude(rib_length)
             )
        # Add a little tapered top detail to the rib as seen in image
        rib_top_detail = (cq.Workplane("XY")
                          .workplane(offset=drum_height - rim_height - 3)
                          .transformed(rotate=cq.Vector(0, 0, angle))
                          .center(drum_radius, 0)
                          .rect(rib_depth * 4, rib_width * 2)
                          .extrude(2)
                          )
        ribs = ribs.union(r).union(rib_top_detail)
        
    drum = drum.union(ribs)

    # --- 2. The Lid ---
    lid = (cq.Workplane("XY")
           .workplane(offset=drum_height)
           .circle(drum_radius + lid_overhang)
           .extrude(lid_thickness))
    
    # Lid Handle (center vertical rod/knob)
    lid_handle = (cq.Workplane("XY")
                  .workplane(offset=drum_height + lid_thickness)
                  .circle(handle_radius)
                  .extrude(handle_height))
    
    lid = lid.union(lid_handle)

    # --- 3. The Frame (Chassis) ---
    # Base structure under the drum
    base_frame_height = 15.0 # Height of the cradle part
    cradle_offset_z = 5.0 # Bottom of drum starts at z=0, but let's say frame is around it
    
    # We need a hoop or support ring around the drum
    support_ring_z = drum_height * 0.4
    support_ring = (cq.Workplane("XY")
                    .workplane(offset=support_ring_z)
                    .circle(drum_radius + frame_tube_size)
                    .circle(drum_radius) # Tight fit
                    .extrude(frame_tube_size))
    
    # The handles/long rails
    # They curve. Let's define a path for the handles.
    # Left Handle Path
    # Points: (x, y, z)
    # Start far back, go to drum, curve down/around
    
    # Simplified approach: Create straight segments and curve them or loft.
    # Let's use a sweep along a wire.
    
    def make_handle_path(side_factor):
        # side_factor: 1 for right, -1 for left
        y_pos = side_factor * (drum_radius + 2.0)
        
        # Define points for a spline
        # Tip of handle (far back)
        p1 = (-handle_length, y_pos * 1.5, support_ring_z * 0.5) 
        # Mid point before curve
        p2 = (-20, y_pos, support_ring_z)
        # Attachment at drum
        p3 = (0, y_pos, support_ring_z)
        # Front extension
        p4 = (20, y_pos, support_ring_z)
        
        return cq.Workplane("XZ").spline([p1, p2, p3, p4], include_current=True)

    # Let's try constructing the frame with box primitives for robustness instead of complex sweeps if possible,
    # or simple polyline sweeps.
    
    # Handle Tubes
    handle_y_offset = drum_radius + 4.0
    
    # Path for one handle (Left)
    # Using 2D sketch on XZ plane and extruding? No, handles are 3D.
    # Let's simply build them out of segments.
    
    # Long straight part of handle
    handle_arm_len = 60
    handle_angle = 15 # degrees down
    
    # Constructing the handle rails
    # Center section attached to drum
    rail_center_l = (cq.Workplane("XY")
                     .workplane(offset=support_ring_z - frame_tube_size/2)
                     .center(0, handle_y_offset)
                     .box(drum_radius*2 + 10, frame_tube_size, frame_tube_size))

    rail_center_r = (cq.Workplane("XY")
                     .workplane(offset=support_ring_z - frame_tube_size/2)
                     .center(0, -handle_y_offset)
                     .box(drum_radius*2 + 10, frame_tube_size, frame_tube_size))
    
    # Angled extensions (Handles)
    # We position a plane at the end of the center rail and extrude along a vector
    handle_extension_l = (cq.Workplane("YZ")
                          .workplane(offset=- (drum_radius + 5)) # Front/back position
                          .center(handle_y_offset, support_ring_z)
                          .rect(frame_tube_size, frame_tube_size)
                          .extrude(-handle_arm_len) # Extrude backwards
                          # To curve it, we might need a sweep, but a straight rotation is easier to code reliably without visual feedback
                          .rotate((0,0,0), (0,1,0), -15) # Rotate down
                          )
                          
    # Let's do a sweep for the handle to match the image's "S" curve better
    path_pts_l = [
        (- (drum_radius), handle_y_offset, support_ring_z),
        (- (drum_radius) - 30, handle_y_offset * 1.2, support_ring_z - 5),
        (- (drum_radius) - 70, handle_y_offset * 1.5, support_ring_z - 25)
    ]
    
    path_pts_r = [
        (- (drum_radius), -handle_y_offset, support_ring_z),
        (- (drum_radius) - 30, -handle_y_offset * 1.2, support_ring_z - 5),
        (- (drum_radius) - 70, -handle_y_offset * 1.5, support_ring_z - 25)
    ]
    
    def create_handle_sweep(pts):
        path = cq.Workplane("XY").polyline(pts) # This is 2D, we need 3D spline
        # CadQuery 3D spline construction
        # Make a wire from points
        w = cq.Wire.makeSpline([cq.Vector(*p) for p in pts])
        # Profile
        p = cq.Workplane("YZ").center(pts[0][1], pts[0][2]).rect(frame_tube_size, frame_tube_size)
        # This is tricky because the profile plane must be normal to path.
        # Easier method: Create a solid box and rotate/move sections?
        # Let's use simple cylinders/boxes for stability.
        return None 

    # Fallback: Construct handles from segments for assured validity
    # Segment 1: Attached to drum ring
    seg1_l = (cq.Workplane("XY")
              .workplane(offset=support_ring_z - frame_tube_size/2)
              .center(0, handle_y_offset)
              .box(drum_radius*2.5, frame_tube_size, frame_tube_size))
              
    seg1_r = (cq.Workplane("XY")
              .workplane(offset=support_ring_z - frame_tube_size/2)
              .center(0, -handle_y_offset)
              .box(drum_radius*2.5, frame_tube_size, frame_tube_size))
    
    # Segment 2: Angled handle extension
    # Calculate start point for extension (back of the straight rail)
    back_x = - (drum_radius * 1.25)
    
    seg2_l = (cq.Workplane("XY")
              .workplane(offset=support_ring_z - frame_tube_size/2)
              .transformed(offset=cq.Vector(back_x, handle_y_offset, 0), rotate=cq.Vector(0, -20, 10))
              .box(50, frame_tube_size, frame_tube_size, centered=(False, True, True)))
              
    seg2_r = (cq.Workplane("XY")
              .workplane(offset=support_ring_z - frame_tube_size/2)
              .transformed(offset=cq.Vector(back_x, -handle_y_offset, 0), rotate=cq.Vector(0, -20, -10))
              .box(50, frame_tube_size, frame_tube_size, centered=(False, True, True)))

    frame = seg1_l.union(seg1_r).union(seg2_l).union(seg2_r).union(support_ring)
    
    # Bottom Frame / Axle mount
    # Vertical struts connecting handles to bottom
    strut_height = 20
    v_strut_l = (cq.Workplane("XY")
                 .workplane(offset=support_ring_z - strut_height)
                 .center(0, handle_y_offset)
                 .box(frame_tube_size, frame_tube_size, strut_height, centered=(True, True, False)))
                 
    v_strut_r = (cq.Workplane("XY")
                 .workplane(offset=support_ring_z - strut_height)
                 .center(0, -handle_y_offset)
                 .box(frame_tube_size, frame_tube_size, strut_height, centered=(True, True, False)))
                 
    # Cross brace at bottom
    bottom_cross = (cq.Workplane("XY")
                    .workplane(offset=support_ring_z - strut_height)
                    .box(frame_tube_size, handle_y_offset * 2 + frame_tube_size, frame_tube_size))

    # Axle / Wheel mount area
    # A triangle structure at the bottom
    tri_frame = (cq.Workplane("XY")
                 .workplane(offset=support_ring_z - strut_height)
                 .center(0, 0)
                 .rect(20, handle_y_offset*2) # Base rectangle
                 .extrude(frame_tube_size)) # Flat plate style or tubes
    
    # Let's make it look like tubes
    axle_tube = (cq.Workplane("XY")
                 .workplane(offset=support_ring_z - strut_height)
                 .box(frame_tube_size, handle_y_offset * 2 + 4, frame_tube_size))
                 
    diag_brace_l = (cq.Workplane("YZ")
                    .workplane(offset=0)
                    .center(handle_y_offset, (support_ring_z - strut_height)/2 + strut_height/2 ) # Approximate center
                    .box(frame_tube_size, 25, frame_tube_size) # rough diagonal
                    )
                    # Rotated diagonal is complex without specific anchor points, skipping for clean blocky rep
    
    frame = frame.union(v_strut_l).union(v_strut_r).union(bottom_cross)
    
    # Extra support under drum
    under_support = (cq.Workplane("XY")
                     .workplane(offset=support_ring_z - strut_height)
                     .box(15, 15, frame_tube_size))
    
    frame = frame.union(under_support)

    # --- 4. The mysterious floating piece ---
    # The image shows a small curved piece floating to the right. 
    # It looks like a detached handle segment or a clip.
    # Let's model it as a simple bent bracket.
    floater = (cq.Workplane("XY")
               .workplane(offset=drum_height/2)
               .center(drum_radius * 2.5, 0) # Position to the right
               .box(10, 2, 2)
               .union(
                   cq.Workplane("XY")
                   .workplane(offset=drum_height/2)
                   .center(drum_radius * 2.5 - 4, 1)
                   .box(2, 4, 2)
               ))
               
    # Assemble final
    result = drum.union(lid).union(frame).union(floater)
    
    return result

result = create_model()