import cadquery as cq

def create_crankshaft():
    # --- Parameters ---
    # Shaft dimensions
    main_journal_radius = 8.0
    rod_journal_radius = 7.0
    
    # Counterweight/Web dimensions
    web_thickness = 5.0
    web_width = 30.0   # Width of the counterweight plate
    web_height_top = 22.0  # From center to top (counterweight side)
    web_height_bottom = 15.0 # From center to bottom (rod journal side)
    web_chamfer = 2.0
    
    # Spacing
    main_journal_length = 15.0
    rod_journal_length = 12.0
    rod_journal_offset = 12.0  # Throw distance
    
    # End shafts
    end_shaft_radius = 8.0
    end_shaft_length_front = 20.0
    end_shaft_length_rear = 15.0
    center_hole_radius = 2.5 # Oil passage or centering hole
    
    # --- Helper Functions ---
    
    def create_web():
        """Creates a single crank web (counterweight)."""
        # Create the basic profile of the web
        # It looks like a rectangle with rounded ends, asymmetric
        
        # Center points for top and bottom arcs
        top_center = (0, web_height_top - web_width/2)
        bottom_center = (0, -1 * (web_height_bottom - web_width/2))
        
        # We'll construct this using a hull of two circles or a loft, 
        # but a simple sketch with arcs and lines is robust.
        # Actually, looking at the image, the web is roughly oval/rectangular with a large radius on the counterweight side.
        
        # Let's try a shape that connects the main journal area to the rod journal area, plus a counterweight.
        # It's essentially a loft between the main axis and the rod journal axis, extended outwards.
        
        sketch = (
            cq.Sketch()
            .rect(web_width, web_height_top + web_height_bottom)
            .vertices().fillet(web_width/2.1) # Round off corners almost completely
        )
        
        # Extrude the basic web shape
        web = cq.Workplane("XY").placeSketch(sketch).extrude(web_thickness)
        
        # Shift it so the main journal hole would be at (0,0) locally?
        # The visual center of the web seems offset. 
        # Let's center the main axis (0,0) somewhat offset from the geometric center of the web.
        # The counterweight hangs "down" usually opposite the piston throw.
        # In the image, the throws are alternating.
        
        # Let's redesign the web to be more specific to a crankshaft web shape
        # Typically: A large circle for the main bearing, a circle for the rod bearing, connected, with a big lobe opposite the rod.
        
        # Let's just model it as a solid block first, then cut holes.
        # Center of Main Journal = (0,0)
        # Center of Rod Journal = (0, rod_journal_offset)
        
        # Counterweight lobe goes towards (0, -something)
        
        p_main = (0,0)
        p_rod = (0, rod_journal_offset)
        
        # Create the shape profile on the XY plane
        # 1. Circle around main journal
        # 2. Circle around rod journal
        # 3. Tangents connecting them
        # 4. Counterweight extension
        
        # A simple parametric web shape:
        w = web_width
        wt = web_height_top # counterweight extension
        
        pts = [
            (-w/2, rod_journal_offset), # Top left near rod
            (w/2, rod_journal_offset),  # Top right near rod
            (w/2, -wt),                 # Bottom right (counterweight)
            (-w/2, -wt)                 # Bottom left (counterweight)
        ]
        
        web_geo = (
            cq.Workplane("XY")
            .moveTo(pts[0][0], pts[0][1])
            .lineTo(pts[1][0], pts[1][1])
            .lineTo(pts[2][0], pts[2][1])
            .lineTo(pts[3][0], pts[3][1])
            .close()
            .extrude(web_thickness)
        )
        
        # Add fillets to make it look organic like a casting/forging
        web_geo = web_geo.edges("|Z").fillet(web_width/2.1) 
        
        # Now move it so the main journal is at 0,0. 
        # Currently the rect center is roughly (0, (offset-wt)/2)
        # We need (0,0) to be the axis of rotation.
        # The points defined above are relative to (0,0).
        # Wait, the polyline above creates a shape centered on the points.
        # The main axis (0,0) is inside this shape.
        
        return web_geo

    # --- Assembly Construction ---
    
    # We will build along the Z axis.
    current_z = 0.0
    assembly = cq.Workplane("XY")

    # 1. Front Shaft
    assembly = assembly.circle(end_shaft_radius).extrude(end_shaft_length_front)
    current_z += end_shaft_length_front

    # 2. First Web (Throw 1)
    # The rod journal offset is upwards (Y+)
    web1 = create_web().translate((0, 0, current_z))
    # We need to orient the web. Default web has rod offset at +Y, counterweight at -Y.
    # Image shows throws are 180 degrees apart (Flat plane crank style appearance or 4-cyl)
    # Let's assume standard 4-cylinder style: UP, DOWN, DOWN, UP or similar.
    # The image shows 4 webs, implying a 2-throw crank (like a 2-cylinder or v-twin) or a section.
    # Actually, looking closer: 
    # Left shaft -> Web -> Pin -> Web -> Main Journal -> Web -> Pin -> Web -> Right Shaft.
    # It's a 2-throw crankshaft.
    
    # Throw 1: Up
    assembly = assembly.union(web1)
    current_z += web_thickness
    
    # 3. Rod Journal 1
    # Centered at (0, rod_journal_offset)
    rod_pin1 = (
        cq.Workplane("XY")
        .center(0, rod_journal_offset)
        .circle(rod_journal_radius)
        .extrude(rod_journal_length)
        .translate((0, 0, current_z))
    )
    assembly = assembly.union(rod_pin1)
    current_z += rod_journal_length
    
    # 4. Second Web (Throw 1 closing)
    web2 = create_web().translate((0, 0, current_z))
    assembly = assembly.union(web2)
    current_z += web_thickness
    
    # 5. Middle Main Journal
    # Centered at (0,0)
    mid_journal = (
        cq.Workplane("XY")
        .circle(main_journal_radius)
        .extrude(main_journal_length)
        .translate((0, 0, current_z))
    )
    assembly = assembly.union(mid_journal)
    current_z += main_journal_length
    
    # 6. Third Web (Throw 2)
    # Throw 2 is usually 180 degrees from Throw 1 for this visual style.
    # Rotate web 180 degrees around Z.
    web3 = create_web().rotate((0,0,0), (0,0,1), 180).translate((0, 0, current_z))
    assembly = assembly.union(web3)
    current_z += web_thickness
    
    # 7. Rod Journal 2
    # Centered at (0, -rod_journal_offset)
    rod_pin2 = (
        cq.Workplane("XY")
        .center(0, -rod_journal_offset)
        .circle(rod_journal_radius)
        .extrude(rod_journal_length)
        .translate((0, 0, current_z))
    )
    assembly = assembly.union(rod_pin2)
    current_z += rod_journal_length
    
    # 8. Fourth Web (Throw 2 closing)
    web4 = create_web().rotate((0,0,0), (0,0,1), 180).translate((0, 0, current_z))
    assembly = assembly.union(web4)
    current_z += web_thickness
    
    # 9. Rear Shaft
    rear_shaft = (
        cq.Workplane("XY")
        .circle(end_shaft_radius)
        .extrude(end_shaft_length_rear)
        .translate((0, 0, current_z))
    )
    assembly = assembly.union(rear_shaft)
    current_z += end_shaft_length_rear
    
    # --- Finishing Touches ---
    
    # Fillets on main journals and rod journals to webs to reduce stress concentrations
    # This can be computationally expensive, so we'll do selected edges if possible,
    # or skip for a lightweight model. The image shows some soft edges.
    # Let's fillet the outer edges of the webs slightly to break sharpness.
    # assembly = assembly.edges("|Z").fillet(0.5) # Global fillet - risky but looks good
    
    # Oil holes / Center holes
    # Drill through the main axis
    assembly = assembly.faces("<Z").workplane().circle(center_hole_radius).cutBlind(current_z)
    
    # Chamfer the ends of the shaft
    assembly = assembly.faces("<Z or >Z").edges().chamfer(1.0)

    # Optional: Lightening holes in the webs (often seen in high perf cranks)
    # The image shows holes in the counterweights.
    hole_radius = 4.0
    hole_dist = 14.0 # distance from center towards counterweight
    
    # We need to cut holes in the specific web locations.
    # Web 1 & 2 (Up throw, counterweight down) -> Hole at (0, -hole_dist)
    # Web 3 & 4 (Down throw, counterweight up) -> Hole at (0, hole_dist)
    
    # Cut through first pair of webs
    # Z range for first pair: end_shaft_length_front to end_shaft_length_front + 2*web + rod_len
    # Simpler approach: Create a cutter cylinder and subtract
    
    # Cutter for bottom counterweights (Webs 1, 2)
    cutter1 = (
        cq.Workplane("XY")
        .center(0, -16.0) # Position in counterweight
        .circle(hole_radius)
        .extrude(current_z) # Just extrude long enough
    )
    
    # Cutter for top counterweights (Webs 3, 4)
    cutter2 = (
        cq.Workplane("XY")
        .center(0, 16.0) # Position in counterweight
        .circle(hole_radius)
        .extrude(current_z)
    )
    
    # We only want to cut the specific webs. 
    # Intersecting cutters with specific Z-ranges is safer.
    
    # Range 1: First two webs
    z_start_1 = end_shaft_length_front
    z_end_1 = z_start_1 + web_thickness*2 + rod_journal_length
    
    # Range 2: Second two webs
    z_start_2 = z_end_1 + main_journal_length
    z_end_2 = z_start_2 + web_thickness*2 + rod_journal_length
    
    # Create specific cutters positioned in Z
    c1 = (cq.Workplane("XY")
          .workplane(offset=z_start_1)
          .center(0, -15.0)
          .circle(hole_radius)
          .extrude(z_end_1 - z_start_1)
         )
         
    c2 = (cq.Workplane("XY")
          .workplane(offset=z_start_2)
          .center(0, 15.0)
          .circle(hole_radius)
          .extrude(z_end_2 - z_start_2)
         )

    assembly = assembly.cut(c1).cut(c2)

    return assembly

result = create_crankshaft()