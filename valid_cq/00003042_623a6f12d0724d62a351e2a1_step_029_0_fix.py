import cadquery as cq

# 20x20 T-slot aluminum extrusion profile
# Standard 20x20 profile with T-slots on all 4 sides

width = 20
height = 300  # length of the extrusion

def make_20x20_profile():
    # Start with a 20x20 square
    profile = cq.Workplane("XY")
    
    # Create the main square
    result = profile.rect(width, width).extrude(height)
    
    # Cut corner chamfers/rounds - the 4 corners have small chamfers
    # Chamfer the vertical edges (corners)
    result = result.edges("|Z").chamfer(1.5)
    
    # Now cut the T-slots on all 4 faces
    # Each face has a T-slot groove running the full length
    
    slot_width = 6.2      # outer slot opening
    slot_depth = 4.3      # depth of T-slot
    inner_width = 11.0    # inner T width
    inner_height = 2.5    # inner T height
    
    # Cut T-slot on +X face
    result = (result
        .faces(">X")
        .workplane()
        .center(0, height/2)
        .rect(slot_width, height)
        .cutBlind(-slot_depth)
    )
    
    # Inner part of T-slot on +X face (wider cut)
    result = (result
        .faces(">X")
        .workplane()
        .center(0, height/2)
        .rect(inner_width, height)
        .cutBlind(-(slot_depth - inner_height))
    )
    
    # Cut T-slot on -X face
    result = (result
        .faces("<X")
        .workplane()
        .center(0, height/2)
        .rect(slot_width, height)
        .cutBlind(-slot_depth)
    )
    
    result = (result
        .faces("<X")
        .workplane()
        .center(0, height/2)
        .rect(inner_width, height)
        .cutBlind(-(slot_depth - inner_height))
    )
    
    # Cut T-slot on +Y face
    result = (result
        .faces(">Y")
        .workplane()
        .center(0, height/2)
        .rect(slot_width, height)
        .cutBlind(-slot_depth)
    )
    
    result = (result
        .faces(">Y")
        .workplane()
        .center(0, height/2)
        .rect(inner_width, height)
        .cutBlind(-(slot_depth - inner_height))
    )
    
    # Cut T-slot on -Y face
    result = (result
        .faces("<Y")
        .workplane()
        .center(0, height/2)
        .rect(slot_width, height)
        .cutBlind(-slot_depth)
    )
    
    result = (result
        .faces("<Y")
        .workplane()
        .center(0, height/2)
        .rect(inner_width, height)
        .cutBlind(-(slot_depth - inner_height))
    )
    
    # Cut center hole running full length
    result = (result
        .faces(">Z")
        .workplane()
        .circle(2.0)
        .cutThruAll()
    )
    
    # Cut small corner grooves (the concave corners typical of 20x20 extrusion)
    corner_r = 1.5
    corner_offset = width/2 - 0.5
    
    for x_sign in [1, -1]:
        for y_sign in [1, -1]:
            result = (result
                .faces(">Z")
                .workplane()
                .center(x_sign * corner_offset, y_sign * corner_offset)
                .circle(corner_r)
                .cutThruAll()
            )
    
    return result

result = make_20x20_profile()