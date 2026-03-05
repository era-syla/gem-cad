import cadquery as cq

def create_clamp_half(side='L'):
    # Dimensions
    rod_diam = 8.0
    mount_hole_diam = 3.6
    mount_cb_diam = 7.0
    mount_cb_depth = 2.0
    
    # Body dimensions
    block_width = 15.0
    block_length = 24.0
    block_height = 18.0
    tab_width = 10.0
    tab_height = 5.0
    
    # Orientation direction: -1 for L (extends -X), 1 for R (extends +X)
    direction = -1 if side == 'L' else 1
    
    # 1. Base Profile on XZ Plane
    # Points defined relative to origin (Inner Bottom Corner)
    pts = [
        (0, 0),
        (0, block_height),
        (direction * block_width, block_height),
        (direction * block_width, tab_height),
        (direction * (block_width + tab_width), tab_height),
        (direction * (block_width + tab_width), 0)
    ]
    
    # Extrude the profile along Y axis
    part = cq.Workplane("XZ").polyline(pts).close().extrude(block_length)
    
    # 2. Fillet the top edges of the main block
    # Select edges parallel to Y, at the top (Z approx block_height)
    part = part.edges("|Y and >Z").fillet(4.0)
    
    # 3. Create the Main Rod Hole (Through Y)
    # Centered in the block section
    rod_x = direction * block_width / 2.0
    rod_z = 11.0 # Slightly above center to account for base
    part = part.faces(">Y").workplane().moveTo(rod_x, rod_z).circle(rod_diam/2.0).cutThruAll()
    
    # 4. Mounting Hole on the Tab
    # Select the top face of the tab (lowest >Z face)
    part = (part.faces(">Z").filter(lambda f: f.BoundingBox().center.z < block_height/2.0)
            .workplane(centerOption="CenterOfBoundBox")
            .cboreHole(mount_hole_diam, mount_cb_diam, mount_cb_depth))
            
    # 5. Embossed Text ("L" or "R")
    # Select top face of the block
    part = (part.faces(">Z").filter(lambda f: f.BoundingBox().center.z > tab_height)
            .workplane(centerOption="CenterOfBoundBox")
            .text(side, 10.0, -0.6))
            
    # 6. Interface Features (Inner Face at X=0)
    if side == 'L':
        # Create two screw holes on the inner face
        # Face is >X (Normal points +X, though material is in -X)
        part = (part.faces(">X").workplane()
                .moveTo(5, 0).circle(1.5).cutBlind(-8.0)  # Hole 1
                .moveTo(-5, 0).circle(1.5).cutBlind(-8.0) # Hole 2
               )
        
        # Add alignment tab (Bottom Front)
        # Position: X=0, Y=Start, Z=Bottom
        # Union a small box centered relative to the placement
        tab_geo = (cq.Workplane("XY")
                   .translate((0.5, 2.0, 1.5)) # X=0.5 makes it protrude 1.5mm (assuming 2mm width centered? No, box is centered)
                   .box(3.0, 4.0, 3.0))        # Box is 3mm wide, centered -> -1.5 to 1.5. Protrudes 1.5mm.
        part = part.union(tab_geo)
        
    else: # side == 'R'
        # Create a rectangular pocket on the inner face
        # Face is <X (Normal points -X)
        part = (part.faces("<X").workplane()
                .rect(14.0, 6.0).cutBlind(-2.0))
        
        # Add alignment tab (Bottom Back)
        # Position: X=0, Y=End, Z=Bottom
        tab_geo = (cq.Workplane("XY")
                   .translate((-0.5, block_length - 2.0, 1.5))
                   .box(3.0, 4.0, 3.0))
        part = part.union(tab_geo)
        
    return part

# Generate the two parts
part_l = create_clamp_half('L').translate((-2, 0, 0)) # Shift Left
part_r = create_clamp_half('R').translate((2, 0, 0))  # Shift Right

# Combine into result
result = part_l.union(part_r)