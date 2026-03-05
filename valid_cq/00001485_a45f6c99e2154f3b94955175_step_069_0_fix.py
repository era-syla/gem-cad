import cadquery as cq

def make_connector_piece():
    # Main body block
    body = (
        cq.Workplane("XY")
        .box(20, 12, 10)
    )
    
    # Add side flanges (top and bottom ears)
    left_flange = (
        cq.Workplane("XY")
        .center(-10, 0)
        .box(4, 16, 4)
        .translate((-8, 0, 3))
    )
    
    right_flange = (
        cq.Workplane("XY")
        .center(10, 0)
        .box(4, 16, 4)
        .translate((8, 0, 3))
    )
    
    # Circular disk/wheel on the side
    disk = (
        cq.Workplane("YZ")
        .center(0, 0)
        .circle(5)
        .extrude(3)
        .translate((-13, 0, 0))
    )
    
    # Rectangular tab/arm extending out
    tab = (
        cq.Workplane("XY")
        .box(18, 6, 4)
        .translate((-19, 0, -3))
    )
    
    # Small rectangular connector slot
    slot_cut = (
        cq.Workplane("XY")
        .box(6, 4, 6)
        .translate((-19, 0, -3))
    )
    
    # Build the main piece
    piece = (
        cq.Workplane("XY")
        .box(20, 12, 10)
    )
    
    # Add top flanges
    top_flange = (
        cq.Workplane("XY")
        .workplane(offset=3)
        .center(-8, 0)
        .box(4, 16, 4)
    )
    
    # Simpler approach - build piece from scratch
    # Main rectangular body
    main_body = cq.Workplane("XY").box(22, 14, 10)
    
    # Cut slot in body top
    main_body = (
        main_body
        .faces(">Z")
        .workplane()
        .center(0, 0)
        .rect(10, 6)
        .cutBlind(-6)
    )
    
    # Add circular disk on left side
    disk_part = (
        cq.Workplane("YZ")
        .circle(5.5)
        .extrude(4)
        .translate((-15, 0, 0))
    )
    
    # Hole through disk
    disk_hole = (
        cq.Workplane("YZ")
        .circle(2)
        .extrude(4)
        .translate((-15, 0, 0))
    )
    
    # Extending arm/tab
    arm = (
        cq.Workplane("XY")
        .box(16, 5, 3)
        .translate((-19, 0, -3.5))
    )
    
    # Combine all parts
    result_piece = (
        main_body
        .union(disk_part)
        .cut(disk_hole)
        .union(arm)
    )
    
    # Add side guide flanges
    flange_l = (
        cq.Workplane("XY")
        .box(3, 18, 5)
        .translate((-9.5, 0, 2.5))
    )
    flange_r = (
        cq.Workplane("XY")
        .box(3, 18, 5)
        .translate((9.5, 0, 2.5))
    )
    
    result_piece = result_piece.union(flange_l).union(flange_r)
    
    return result_piece

# Create two connector pieces - one normal, one mirrored
piece1 = make_connector_piece()

# Second piece - mirror of first
piece2 = (
    make_connector_piece()
    .mirror("YZ", basePointVector=(0, 0, 0))
    .translate((50, 8, 0))
)

# Translate first piece
piece1 = piece1.translate((-5, -8, 0))

# Combine both pieces
result = piece1.union(piece2)