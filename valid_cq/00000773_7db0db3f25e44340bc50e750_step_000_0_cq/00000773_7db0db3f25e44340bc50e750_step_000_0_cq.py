import cadquery as cq

def create_model():
    # -------------------------------------------------------------------------
    # Parameters
    # -------------------------------------------------------------------------
    
    # Main Base Rail (Black, long)
    rail_length = 500.0
    rail_width = 10.0
    rail_height = 10.0
    
    # Carriage / Slider Block (Grey block on the rail)
    carriage_length = 40.0
    carriage_width = 40.0
    carriage_thickness = 10.0
    
    # Vertical Mast (Thin vertical extrusion)
    mast_height = 40.0
    mast_width = 5.0
    mast_depth = 5.0
    
    # Side Block (Small cube on the carriage)
    side_block_size = 12.0
    
    # Cylindrical Elements (Bearings/Rollers)
    roller_radius = 5.0
    roller_length = 40.0
    
    # Perforated Beam (Looks like a LEGO technic beam or similar structural rail)
    beam_length = 60.0
    beam_width = 10.0
    beam_height = 8.0
    hole_radius = 2.0
    hole_spacing = 8.0
    
    # Wire Frame / Bail (Thin rectangular loop)
    wire_thickness = 1.5
    wire_loop_width = 50.0
    wire_loop_length = 40.0

    # Separate Plate (The floating square)
    plate_size = 50.0
    plate_thickness = 1.0

    # -------------------------------------------------------------------------
    # Component Construction
    # -------------------------------------------------------------------------

    # 1. Main Rail
    # A simple long rectangular prism, potentially with a groove
    rail = (cq.Workplane("XY")
            .box(rail_length, rail_width, rail_height)
            .faces(">X").workplane().rect(rail_width*0.6, rail_height*0.6).cutBlind(-rail_length) # Simple groove
            )
    
    # 2. Perforated Beam (Cross-beam)
    # Create the base block
    beam = (cq.Workplane("XY")
            .box(beam_length, beam_width, beam_height)
            )
    
    # Create holes along the beam
    num_holes = int(beam_length / hole_spacing) - 1
    for i in range(num_holes):
        offset = (i - (num_holes - 1) / 2) * hole_spacing
        beam = (beam.faces(">Y").workplane()
                .center(offset, 0)
                .circle(hole_radius)
                .cutBlind(-beam_width))
        
        # Add holes on top face as well for that "Technic" look
        beam = (beam.faces(">Z").workplane()
                .center(offset, 0)
                .circle(hole_radius)
                .cutBlind(-beam_height))

    # 3. Carriage Assembly
    # Base plate of the carriage
    carriage_base = cq.Workplane("XY").box(carriage_length, carriage_width, carriage_thickness)
    
    # Add grooves/features to top of carriage to match image complexity
    carriage_base = (carriage_base
                     .faces(">Z").workplane()
                     .rect(carriage_length, 5).cutBlind(-2)
                     )

    # Rollers/Cylinders on top
    roller1 = (cq.Workplane("YZ")
               .circle(roller_radius)
               .extrude(roller_length)
               .rotate((0,0,0), (0,1,0), 90) # Orient along X
               .translate((0, -carriage_width/4, carriage_thickness/2 + roller_radius))
               )
    
    roller2 = (cq.Workplane("YZ")
               .circle(roller_radius)
               .extrude(roller_length)
               .rotate((0,0,0), (0,1,0), 90)
               .translate((0, carriage_width/4, carriage_thickness/2 + roller_radius))
               )

    # Vertical Mast
    mast = (cq.Workplane("XY")
            .box(mast_depth, mast_width, mast_height)
            .translate((0, 0, carriage_thickness/2 + mast_height/2))
            )
    
    # Side Block (Motor or sensor housing)
    side_block = (cq.Workplane("XY")
                  .box(side_block_size, side_block_size, side_block_size)
                  .translate((carriage_length/2 - side_block_size/2, 
                              carriage_width/2 - side_block_size/2, 
                              carriage_thickness/2 + side_block_size/2))
                  )

    # Combine carriage parts
    carriage_assembly = carriage_base.union(roller1).union(roller2).union(mast).union(side_block)
    
    # 4. Wire Frame / Bail
    # Create a path and sweep a rectangle or circle along it, or just cut a plate
    wire_frame_outer = cq.Workplane("XY").rect(wire_loop_length, wire_loop_width).extrude(wire_thickness)
    wire_frame_inner = cq.Workplane("XY").rect(wire_loop_length - 2*wire_thickness, wire_loop_width - 2*wire_thickness).extrude(wire_thickness)
    wire_frame = wire_frame_outer.cut(wire_frame_inner)
    
    # Position the wire frame extending from the carriage
    wire_frame = wire_frame.translate((0, wire_loop_width/2 + carriage_width/2, 0))

    # 5. Separate Plate (The floating square in the image)
    plate = (cq.Workplane("XY")
             .box(plate_size, plate_size * 1.4, plate_thickness) # Aspect ratio adjustment
             .translate((-150, -100, -50)) # Arbitrary position based on image perspective
             )

    # -------------------------------------------------------------------------
    # Assembly / Positioning
    # -------------------------------------------------------------------------
    
    # Position the carriage on the rail (at the end)
    carriage_pos_x = rail_length/2 - carriage_length/2
    carriage_assembly = carriage_assembly.translate((carriage_pos_x, 0, rail_height/2 + carriage_thickness/2))
    wire_frame = wire_frame.translate((carriage_pos_x, 0, rail_height/2))
    
    # Position the perforated beam crossing underneath the carriage area
    beam = beam.rotate((0,0,0), (0,0,1), 90) # Rotate to be perpendicular to main rail
    beam = beam.translate((carriage_pos_x, -beam_length/2 - 10, rail_height/2))

    # Combine everything into one object for the result
    # (Note: In a real assembly, we might keep these separate, but for single solid viewing:)
    full_assembly = rail.union(carriage_assembly).union(beam).union(wire_frame)
    
    # Combine with the floating plate (physically disjointed union)
    final_result = full_assembly.union(plate)

    return final_result

# Generate the model
result = create_model()