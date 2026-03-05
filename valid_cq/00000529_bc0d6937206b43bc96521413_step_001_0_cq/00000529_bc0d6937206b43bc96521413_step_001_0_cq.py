import cadquery as cq

def create_hex_flange_bolt():
    # --- Parametric Dimensions ---
    # Head dimensions
    hex_size = 10.0       # Width across flats
    head_height = 6.0     # Height of the hex part
    flange_diam = 14.0    # Diameter of the integrated washer
    flange_height = 2.0   # Thickness of the flange
    
    # Shaft dimensions
    total_length = 80.0   # Length from under the flange to the tip
    shaft_diam = 6.0      # Major diameter (e.g., M6)
    
    # Thread simulation dimensions (visual representation only)
    # A fully unthreaded shank section appears at the tip in the image
    unthreaded_tip_length = 15.0
    threaded_length = total_length - unthreaded_tip_length
    
    # --- Geometry Construction ---
    
    # 1. Create the Hex Head
    # Create a polygon for the hex head extruded to its height
    # Using circumscribed circle radius from flat-to-flat distance: radius = (size/2) / cos(30)
    # Or simply use the polygon function with diameter/apothem logic if available, but vertices is safer.
    # CadQuery's polygon method takes circumradius by default if not specified otherwise, 
    # but regularPolygon uses radius. 
    # Radius of circumscribed circle = (hex_size / 2) / (sqrt(3)/2) = hex_size / sqrt(3)
    import math
    circumradius = (hex_size / 2) / (math.sqrt(3) / 2)
    
    head = (cq.Workplane("XY")
            .polygon(nSides=6, diameter=circumradius*2)
            .extrude(head_height)
           )
    
    # 2. Add Chamfer to Top of Hex Head ( Cosmetic but realistic)
    # Select the top edges and chamfer them
    head = head.faces(">Z").edges().chamfer(0.5)

    # 3. Create the Flange
    # The flange sits below the hex head. We extrude it downwards.
    flange = (cq.Workplane("XY")
              .circle(flange_diam / 2)
              .extrude(-flange_height)
             )
    
    # Combine Head and Flange
    bolt_head = head.union(flange)

    # 4. Create the Main Shaft
    # The shaft starts from the bottom of the flange
    shaft_plane = bolt_head.faces("<Z").workplane()
    shaft = (shaft_plane
             .circle(shaft_diam / 2)
             .extrude(total_length)
            )
            
    # Combine head assembly with shaft
    bolt_main = bolt_head.union(shaft)

    # 5. Model the Thread (Simplified)
    # Real threads are computationally heavy. The image shows a distinct texture/geometry
    # on the upper part of the shaft, while the tip is smooth.
    # We will create a simplified helical cut or a series of grooves to represent threads.
    # A simple way to represent threads visually without heavy computation is subtracting 
    # a slightly smaller cylinder and adding a spiral, or just cutting grooves.
    # Here, we will cut a simple spiral groove for the threaded section.
    
    # Define thread pitch
    pitch = 1.0
    thread_depth = 0.4
    
    # Create a helix path for the sweep
    # We need to create a profile to sweep along the helix
    # The helix starts at -flange_height (bottom of flange) and goes down
    
    # Alternative: Subtractive approach.
    # Create a tool for cutting threads.
    # To keep it robust and not overly complex, we will stick to the basic solid shape. 
    # However, to match the visual "threaded" look vs "smooth" look:
    # We can perform a cosmetic operation or just leave it as a cylinder. 
    # Given the request implies a model based on the image, the visual distinction is important.
    # Let's reduce the diameter of the threaded section slightly to suggest the minor diameter, 
    # then add the threads on top, or just cut into the existing diameter.
    
    # Let's cut grooves. 
    # CadQuery's helix support can be tricky. A robust visual approximation is 
    # a series of annular rings or a proper helix. Let's try a proper helix sweep.
    
    path = cq.Workplane("XY").transformed(offset=(0,0, -flange_height)).parametricCurve(lambda t: (
        (shaft_diam/2 * math.cos(t * threaded_length/pitch * 2 * math.pi), 
         shaft_diam/2 * math.sin(t * threaded_length/pitch * 2 * math.pi), 
         -t * threaded_length)
    ))
    
    # Create the triangular profile for the thread
    # The profile needs to be perpendicular to the path at the start.
    # This is complex in pure CQ without plugins. 
    # A simpler approach for the "visual" of the thread in the image (which looks like a distinct texture)
    # is to create the smooth tip as a separate cylinder to ensure the distinction is clear in the CAD topology.
    
    # Re-doing step 4 with distinct sections for better topology
    
    # Smooth Tip
    tip_plane = bolt_head.faces("<Z").workplane(offset=threaded_length)
    tip = (tip_plane
           .circle(shaft_diam / 2)
           .extrude(unthreaded_tip_length)
          )
          
    # Threaded Section (Base Cylinder)
    # We use a slightly smaller diameter for the base of the threads
    minor_diam = shaft_diam - (2 * 0.3) 
    threaded_core = (bolt_head.faces("<Z").workplane()
                     .circle(minor_diam / 2)
                     .extrude(threaded_length)
                    )

    # Create the threads using a spiral sweep
    # We define a triangular profile and sweep it.
    
    # Creating a solid helix object to union with the core
    # Define the thread profile
    thread_profile = (cq.Workplane("XZ")
                      .moveTo(minor_diam/2, -flange_height) # Start just under flange
                      .lineTo(shaft_diam/2, -flange_height - pitch/2)
                      .lineTo(minor_diam/2, -flange_height - pitch)
                      .close()
                      )
    
    # Sweep along helix
    # Note: twist is in degrees. Total rotation = (length / pitch) * 360
    num_turns = threaded_length / pitch
    threads = thread_profile.twistExtrude(threaded_length, 360 * num_turns)
    
    # Combine all parts
    result_obj = bolt_head.union(threaded_core).union(threads).union(tip)
    
    # 6. Optional: Chamfer the very tip
    result_obj = result_obj.faces("<Z").edges().chamfer(0.5)

    return result_obj

# Generate the model
result = create_hex_flange_bolt()