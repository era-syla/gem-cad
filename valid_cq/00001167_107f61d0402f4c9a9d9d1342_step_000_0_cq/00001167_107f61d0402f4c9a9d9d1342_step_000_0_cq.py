import cadquery as cq

# Parameters
total_height = 120.0
base_radius = 12.0
base_height = 65.0

# Transition section
mid_radius = 16.0
mid_height = 25.0
shoulder_height = 5.0
shoulder_radius = 17.0

# Threaded/Top section
top_height = 15.0
top_radius = 14.0  # Slightly smaller than shoulder
thread_pitch = 2.0
thread_depth = 1.0

# Internal dimensions
bore_radius = 8.0  # Main internal channel
top_chamfer = 1.0

# Button/Protrusion details
button_pos_z = base_height + (mid_height / 2.0)
button_radius = 6.0
button_stickout = 3.0

def create_part():
    # 1. Base Cylinder
    # We build from bottom up. Z=0 is the bottom face.
    base = cq.Workplane("XY").circle(base_radius).extrude(base_height)

    # 2. Transition Section (Conical/Lofted)
    # This section transitions from base_radius to mid_radius
    transition = (
        cq.Workplane("XY")
        .workplane(offset=base_height)
        .circle(base_radius)
        .workplane(offset=mid_height)
        .circle(mid_radius)
        .loft(combine=True)
    )
    
    # 3. Shoulder Ring
    shoulder_bottom_z = base_height + mid_height
    shoulder = (
        cq.Workplane("XY")
        .workplane(offset=shoulder_bottom_z)
        .circle(shoulder_radius)
        .extrude(shoulder_height)
    )

    # 4. Top Neck (Threaded area base)
    neck_bottom_z = shoulder_bottom_z + shoulder_height
    neck = (
        cq.Workplane("XY")
        .workplane(offset=neck_bottom_z)
        .circle(top_radius)
        .extrude(top_height)
    )

    # Combine main body parts
    body = base.union(transition).union(shoulder).union(neck)

    # 5. Create Threads (Simplified representation as grooves)
    # Real threads are computationally heavy, often represented by simple rings in CAD placeholders
    # or actual helix sweeps. Here we make a simple helix cut for visual fidelity.
    
    # Define a helix path
    helix_turns = top_height / thread_pitch
    
    # Create the cutting profile for the thread
    # A simple triangular profile
    thread_profile = (
        cq.Workplane("XZ", origin=(top_radius, 0, neck_bottom_z))
        .moveTo(0, 0)
        .lineTo(-thread_depth, thread_pitch/2)
        .lineTo(0, thread_pitch)
        .close()
    )
    
    # Creating a true helix sweep in CadQuery can be complex. 
    # A standard approach for visual models is using `cut` with a generated thread object
    # or just parallel rings if strict helical geometry isn't required.
    # Let's try a robust helix sweep approach.
    
    def helix_func(t):
        import math
        # t goes from 0 to 1
        z = t * (top_height - thread_pitch) # Don't go all the way to avoid edge artifacts
        angle = t * helix_turns * 2 * math.pi
        x = (top_radius) * math.cos(angle)
        y = (top_radius) * math.sin(angle)
        return (x, y, z + neck_bottom_z + thread_pitch/2)

    # Since helix parametric curves can be tricky without specific plugins,
    # let's approximate with a stack of torus cuts for robustness and speed
    # which looks very similar in static rendering.
    
    threaded_body = body
    for i in range(int(helix_turns) - 1):
        z_pos = neck_bottom_z + (i * thread_pitch) + thread_pitch
        cutter = (
            cq.Workplane("XY")
            .workplane(offset=z_pos)
            .circle(top_radius + 0.1) # Outer bound
            .circle(top_radius - thread_depth/2) # Inner cut depth
            .extrude(thread_pitch * 0.7) # Width of the cut
        )
        # We need a torus or a revolve for a "V" groove, but extrude is safer.
        # Let's do a revolve cut for a nicer V-shape groove.
        
        groove = (
            cq.Workplane("XZ")
            .workplane(offset=z_pos)
            .moveTo(top_radius + 0.5, 0)
            .lineTo(top_radius - thread_depth/2, thread_pitch/4)
            .lineTo(top_radius + 0.5, thread_pitch/2)
            .close()
            .revolve(360, (0,0,0), (0,0,1))
        )
        threaded_body = threaded_body.cut(groove)


    # 6. Hollow out the center (Bore)
    # The image shows a chamfer at the top entrance
    final_shape = threaded_body.faces(">Z").hole(bore_radius * 2)
    
    # Add chamfer to the inner bore at the top
    final_shape = final_shape.faces(">Z").edges(cq.selectors.RadiusNthSelector(0)).chamfer(top_chamfer)

    # 7. Add the Side Button/Detail
    # It sits on the transition section.
    # Create a workplane tangent to the surface or simply offset in Y.
    
    # We create a local boss for the button housing
    button_housing = (
        cq.Workplane("XZ")
        .workplane(offset=base_radius * 0.8) # Move out from center
        .center(0, button_pos_z) # Position along Z axis
        .circle(button_radius)
        .extrude(base_radius * 1.5) # Extrude through the surface
    )
    
    # Intersect the housing with a slightly larger version of the main body to curve the back?
    # Or just union it. The image shows it blending.
    # Let's intersect it with a specific shape to make it conform, or just union and fillet.
    # Given the clean look, a simple union then a cut for the button face is best.
    
    # To make it look like the image (a defined pad on the surface):
    # We will project a shape onto the transition area.
    # Simplified approach: Union a cylinder, then cut the face details.
    
    # Create the protrusion
    protrusion = (
        cq.Workplane("YZ")
        .workplane(offset=10) # Start from outside
        .center(0, button_pos_z)
        .circle(button_radius)
        .extrude(-15) # Extrude inwards
    )
    
    # We only want the part that sticks out slightly plus intersection
    # Let's cut the protrusion with the main body to get the intersection, 
    # then translate it out? No.
    
    # Let's just place a cylinder that intersects well.
    btn_cyl = (
        cq.Workplane("XZ", origin=(0, 0, button_pos_z))
        .circle(button_radius)
        .extrude(mid_radius + button_stickout)
    )
    
    # Cut the inner part so it doesn't block the bore
    btn_cyl = btn_cyl.cut(cq.Workplane("XY").circle(bore_radius).extrude(total_height))
    
    # Detail on the button (the flat recess)
    btn_cut = (
        cq.Workplane("XZ", origin=(0, 0, button_pos_z))
        .workplane(offset=mid_radius + button_stickout) # At the face of the button
        .circle(button_radius - 1.0)
        .extrude(-1.5) # Cut inward
    )
    
    button_assembly = btn_cyl.cut(btn_cut)
    
    # Combine everything
    result_obj = final_shape.union(button_assembly)
    
    # Fillet the button connection to the body for a smooth transition
    try:
        result_obj = result_obj.edges(cq.selectors.NearestToPointSelector((mid_radius, 0, button_pos_z))).fillet(1.0)
    except:
        pass # Fillets can fail on complex intersections

    return result_obj

result = create_part()