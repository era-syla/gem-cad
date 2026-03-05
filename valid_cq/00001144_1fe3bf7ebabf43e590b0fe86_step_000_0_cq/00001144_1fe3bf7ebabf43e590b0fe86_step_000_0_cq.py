import cadquery as cq

def create_snap_fit_collet():
    # Parameters
    base_diameter = 12.0
    base_height = 2.0
    
    body_diameter = 10.0
    body_height = 15.0  # Height of the cylindrical part
    
    dome_height = 4.0   # Height of the rounded top
    total_height = base_height + body_height + dome_height
    
    inner_hole_diameter = 5.0
    
    slot_width = 1.5
    slot_depth = 3.0 # How deep the slot cuts into the radius
    num_slots = 3
    
    # 1. Create the base disk
    base = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_height)
    
    # 2. Create the main cylindrical body
    body = (
        cq.Workplane("XY")
        .workplane(offset=base_height)
        .circle(body_diameter / 2)
        .extrude(body_height)
    )
    
    # 3. Create the dome top
    # We'll use a revolve operation for a smooth dome
    # Profile: start at outer edge, arc to top center
    dome_profile = (
        cq.Workplane("XZ")
        .workplane(offset=base_height + body_height)
        .moveTo(body_diameter / 2, 0)
        .threePointArc((body_diameter/4, dome_height*0.8), (0, dome_height))
        .lineTo(0, 0)
        .close()
    )
    dome = dome_profile.revolve()

    # Combine base, body, and dome
    part = base.union(body).union(dome)
    
    # 4. Create the central hole
    # We drill through the entire part
    part = part.faces(">Z").hole(inner_hole_diameter)
    
    # 5. Create the slots
    # The slots cut vertically from the top down to the base
    # They are arranged radially.
    
    # We'll create a single slot cutter and rotate it.
    # The cutter needs to be wider than the part to cut through one side,
    # or positioned carefully. A rectangle centered on the radius works well.
    
    slot_cutter_shape = (
        cq.Workplane("XY")
        .workplane(offset=base_height) # Start cutting above the base
        .rect(body_diameter + 5, slot_width) # Make it long enough to cross the diameter
        .extrude(body_height + dome_height + 5) # Cut way past the top
    )
    
    # Since we want 3 slots evenly spaced (120 degrees), but cutting through the center
    # would create 6 "fingers" if we just rotate a full diameter bar. 
    # Looking at the image, there are 3 distinct cuts meeting in the center, 
    # dividing the collet into 3 segments.
    # To do this, we can rotate a rectangle that extends from the center outwards.
    
    for i in range(num_slots):
        angle = i * (360.0 / num_slots)
        
        # Define a cutter for one slot extending from center
        single_slot_cutter = (
            cq.Workplane("XY")
            .workplane(offset=base_height) # Start cut at top of base
            .moveTo(0,0)
            # Create a rectangle extending from center outwards
            .rect(body_diameter/2 + 2, slot_width, centered=False) 
            .extrude(body_height + dome_height + 1)
            # Center the width of the slot on the axis
            .translate((0, -slot_width/2, 0))
            .rotate((0,0,0), (0,0,1), angle)
        )
        part = part.cut(single_slot_cutter)
        
    return part

# Create one instance
single_collet = create_snap_fit_collet()

# Arrange 4 of them in a grid as shown in the image
spacing = 18.0
collet_1 = single_collet.translate((-spacing/2, -spacing/2, 0))
collet_2 = single_collet.translate((spacing/2, -spacing/2, 0))
collet_3 = single_collet.translate((-spacing/2, spacing/2, 0))
collet_4 = single_collet.translate((spacing/2, spacing/2, 0))

# Combine into result
result = collet_1.union(collet_2).union(collet_3).union(collet_4)