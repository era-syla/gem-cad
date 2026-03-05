import cadquery as cq

# T-slot aluminum extrusion profile (20x20 style)
# Main dimensions
width = 40
height = 40
length = 40

# Create the main rectangular body
result = cq.Workplane("XY").box(length, width, height)

# Define the T-slot profile cut on front and back faces (along Y axis)
def make_tslot_profile():
    """Create a T-slot cross section wire"""
    slot_width = 8.2
    slot_depth = 6
    head_width = 14
    head_depth = 3.5
    
    pts = [
        (-slot_width/2, 0),
        (-slot_width/2, -slot_depth + head_depth),
        (-head_width/2, -slot_depth + head_depth),
        (-head_width/2, -slot_depth),
        (head_width/2, -slot_depth),
        (head_width/2, -slot_depth + head_depth),
        (slot_width/2, -slot_depth + head_depth),
        (slot_width/2, 0),
    ]
    return pts

slot_pts = make_tslot_profile()

# Cut T-slots on all 4 sides
# Front face (Y+ direction) - slot goes in -Y direction
result = (result
    .faces(">Y")
    .workplane()
    .center(0, 0)
    .polyline(slot_pts)
    .close()
    .cutBlind(-6)
)

# Back face (Y- direction)
result = (result
    .faces("<Y")
    .workplane()
    .center(0, 0)
    .polyline(slot_pts)
    .close()
    .cutBlind(-6)
)

# Right face (X+ direction)
result = (result
    .faces(">X")
    .workplane()
    .center(0, 0)
    .polyline(slot_pts)
    .close()
    .cutBlind(-6)
)

# Left face (X- direction)
result = (result
    .faces("<X")
    .workplane()
    .center(0, 0)
    .polyline(slot_pts)
    .close()
    .cutBlind(-6)
)

# Now create the extrusion as a swept profile along Z
# Actually let's rebuild this as a proper extruded profile

# Build the cross-section profile
def build_tslot_extrusion():
    w = 40  # total width
    h = 40  # total height
    l = 40  # length (extrusion direction)
    
    # Slot parameters
    sw = 8.2   # slot opening width
    sd = 6.0   # slot depth
    hw = 14.0  # T-head width
    hd = 3.5   # T-head recess depth from surface (head portion height)
    
    # Corner radius
    cr = 1.5
    
    # Start with main box
    profile = cq.Workplane("XZ").rect(w, h)
    
    # Extrude along Y
    solid = profile.extrude(l)
    
    # Cut slots on +Y face
    slot_profile = [
        (-sw/2, 0),
        (-sw/2, -(sd - hd)),
        (-hw/2, -(sd - hd)),
        (-hw/2, -sd),
        (hw/2, -sd),
        (hw/2, -(sd - hd)),
        (sw/2, -(sd - hd)),
        (sw/2, 0),
    ]
    
    # +Y slot
    solid = (solid.faces(">Y").workplane()
             .polyline(slot_profile).close().cutBlind(-sd))
    
    # -Y slot  
    solid = (solid.faces("<Y").workplane()
             .polyline(slot_profile).close().cutBlind(-sd))
    
    # +X slot
    solid = (solid.faces(">X").workplane()
             .polyline(slot_profile).close().cutBlind(-sd))
    
    # -X slot
    solid = (solid.faces("<X").workplane()
             .polyline(slot_profile).close().cutBlind(-sd))
    
    # Add corner chamfers on the long edges (Z direction edges)
    solid = (solid.edges("|Z").chamfer(cr))
    
    return solid

result = build_tslot_extrusion()