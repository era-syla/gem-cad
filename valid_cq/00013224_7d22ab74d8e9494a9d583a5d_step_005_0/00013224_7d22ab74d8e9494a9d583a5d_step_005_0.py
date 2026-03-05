import cadquery as cq

def create_large_knob():
    """Creates the large bottom-center control knob with pill-shaped side indents."""
    radius = 20.0
    height = 18.0
    fillet_r = 4.0
    
    # Base cylinder with fillets
    k = cq.Workplane("XY").circle(radius).extrude(height)
    k = k.edges().fillet(fillet_r)
    
    # Side Indentations (Pill-shaped recesses)
    # Create tools rotated around the center to cut the side pills
    num_pills = 10
    pill_w = 4.0
    pill_h = 10.0
    pill_depth = 1.5
    
    # Helper to create one cutting tool oriented correctly
    def make_pill_tool(angle):
        # Workplane on XZ plane (side view), move to surface radius
        return (cq.Workplane("XZ")
                .workplane(offset=radius)
                .center(0, height/2)
                .slot2D(pill_h, pill_w, 90) # 90 deg for vertical slot
                .extrude(-pill_depth * 3)   # Cut inwards
                .rotate((0,0,0), (0,0,1), angle))

    # Apply cuts
    for i in range(num_pills):
        angle = i * (360.0 / num_pills)
        k = k.cut(make_pill_tool(angle))

    # Top Slot (Channel across diameter)
    slot_w = 4.0
    slot_d = 2.0
    k = k.faces(">Z").workplane().rect(radius * 2.5, slot_w).cutBlind(-slot_d)
    
    # Holes inside the slot
    k = (k.faces(">Z").workplane(offset=-slot_d)
         .pushPoints([(6, 0), (-6, 0)])
         .circle(1.5)
         .cutBlind(-5.0))
         
    return k

def create_small_knob():
    """Creates the middle-right small slotted knob."""
    radius = 12.0
    height = 14.0
    fillet_r = 1.5
    
    k = cq.Workplane("XY").circle(radius).extrude(height)
    k = k.edges(">Z").fillet(fillet_r)
    
    # Side Knurling (Vertical grooves)
    num_grooves = 16
    groove_r = 1.0 
    
    # Create array of cylinders to cut grooves
    cutters = (cq.Workplane("XY")
               .polarArray(radius, 0, 360, num_grooves)
               .circle(groove_r)
               .extrude(height))
               
    k = k.cut(cutters)
    
    # Top Slot (Recess)
    k = k.faces(">Z").workplane().slot2D(14, 3.0).cutBlind(-2.0)
    
    return k

def create_dome_knob():
    """Creates the top-right pointer knob."""
    radius = 11.0
    fin_h = 8.0
    fin_thick = 2.0
    
    # Base Hemisphere (Sphere cut in half)
    k = cq.Workplane("XY").sphere(radius)
    k = k.cut(cq.Workplane("XY").rect(radius*4, radius*4).extrude(-radius*2))
    
    # Pointer Fin
    fin = (cq.Workplane("XY")
           .rect(fin_thick, radius * 1.8)
           .extrude(radius + fin_h/2)
           .translate((0, 0, -2)) # Lower slightly to ensure intersection
          )
    
    k = k.union(fin)
    
    # Ensure bottom is flat
    k = k.cut(cq.Workplane("XY").rect(radius*4, radius*4).extrude(-10))
    
    return k

def create_flanged_knob():
    """Creates the left flanged knob."""
    r_base = 15.0
    r_body = 12.0
    h_base = 2.5
    h_body = 12.0
    
    # Base Flange
    base = cq.Workplane("XY").circle(r_base).extrude(h_base)
    
    # Main Body
    body = (cq.Workplane("XY")
            .workplane(offset=h_base)
            .circle(r_body)
            .extrude(h_body))
            
    k = base.union(body)
    k = k.edges(">Z").fillet(1.0)
    
    # Side Knurling
    num_grooves = 12
    cutters = (cq.Workplane("XY")
               .polarArray(r_body, 0, 360, num_grooves)
               .circle(0.8)
               .extrude(h_base + h_body))
               
    k = k.cut(cutters)
    
    # Indicator Mark
    k = k.faces(">Z").workplane().rect(r_body, 1.5).cutBlind(-0.5)
    
    return k

# Generate parts
knob_large = create_large_knob()
knob_small = create_small_knob()
knob_dome = create_dome_knob()
knob_flanged = create_flanged_knob()

# Position parts to match the image layout
# Large (Front Center)
part1 = knob_large
# Small (Back Center-ish)
part2 = knob_small.translate((0, 35, 0))
# Dome (Back Top)
part3 = knob_dome.translate((0, 60, 0))
# Flanged (Left)
part4 = knob_flanged.translate((-35, 15, 0))

# Combine into final result
result = part1.union(part2).union(part3).union(part4)