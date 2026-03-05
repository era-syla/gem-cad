import cadquery as cq

# --- Parameters ---

# Common mounting and bore sizes
bearing_bore_diam = 15.0  # Linear bearing diameter (LM8UU style usually, scaling slightly larger for look)
rod_bore_diam = 8.1       # Smooth rod diameter (8mm + tolerance)
screw_hole_diam = 3.2     # M3 screw clearance
nut_trap_width = 5.6      # M3 nut width
wall_thickness = 3.0      # General wall thickness

# Vertical carriage dimensions
carriage_height = 45.0
bearing_block_length = 24.0 # Approximate length for LM8UU
bearing_spacing_center = 18.0 # Distance between rod center and belt clamp area

# Endstop/Belt clamp section
clamp_slot_width = 1.5
clamp_screw_offset = 6.0

# Motor/Idler mount dimensions
mount_plate_thickness = 4.0
motor_hole_spacing = 31.0 # NEMA 17 spacing
motor_pilot_diam = 22.0
mount_extension_length = 40.0

# --- Helper Functions ---

def create_vertical_carriage(is_motor_mount=False, is_idler_mount=False):
    """
    Creates the main vertical carriage block holding linear bearings.
    Optionally adds motor or idler mounting plates.
    """
    
    # 1. Main Body Profile (extruded vertically)
    # The shape is roughly a figure-8 or a block with two major bores
    
    # Base block for bearings
    main_body = (
        cq.Workplane("XY")
        .circle(bearing_bore_diam/2 + wall_thickness) # Outer shell for bearing
        .extrude(carriage_height)
    )
    
    # The clamp/tensioner block attached to the side
    tensioner_block = (
        cq.Workplane("XY")
        .center(bearing_spacing_center, 0)
        .rect(15, 20)
        .extrude(carriage_height)
    )
    
    # Fuse them
    main_body = main_body.union(tensioner_block)
    
    # Fillet the join
    main_body = main_body.edges("|Z").fillet(2.0)
    
    # 2. Cut Bores and Slots
    
    # Cut main bearing bore
    main_body = (
        main_body.faces(">Z").workplane()
        .center(0, 0)
        .hole(bearing_bore_diam)
    )
    
    # Cut tensioner bore/feature
    main_body = (
        main_body.faces(">Z").workplane()
        .center(bearing_spacing_center, 0)
        .hole(6.0) # Screw/rod hole
    )
    
    # Slit for clamping tension
    slit = (
        cq.Workplane("XY")
        .center(bearing_spacing_center/2, 0)
        .rect(bearing_spacing_center + 10, clamp_slot_width)
        .extrude(carriage_height)
    )
    
    # We create a zig-zag slit often seen in these parts for flexibility
    # For simplicity, we'll do a straight cut through the "neck" connecting the two lobes
    neck_cut = (
        cq.Workplane("XY")
        .center(bearing_spacing_center/2, 0)
        .rect(10, 1.0)
        .extrude(carriage_height)
    )
    
    # Add screw holes for clamping the linear bearings
    # Side holes
    for z_pos in [10, carriage_height - 10]:
        main_body = (
            main_body.faces(">X").workplane(centerOption="CenterOfBoundBox")
            .center(0, z_pos - carriage_height/2)
            .hole(screw_hole_diam, depth=20)
        )

    # 3. Add Mounting Plate (if applicable)
    if is_motor_mount or is_idler_mount:
        plate_z = carriage_height - 5.0 # Position near top
        
        # Define the triangular/trapezoidal bracket shape
        pts = [
            (0, 0),
            (mount_extension_length, 20),
            (mount_extension_length, -20),
        ]
        
        bracket = (
            cq.Workplane("YZ")
            .workplane(offset=-bearing_bore_diam/2) # Start from side of bearing shell
            .polyline(pts).close()
            .extrude(mount_plate_thickness)
        )
        
        # Rotate to align correctly (pointing away from center usually)
        # This is an approximation of the angled bracket in the image
        bracket = bracket.rotate((0,0,0), (0,0,1), 45)
        bracket = bracket.translate((0, 0, carriage_height - 15))

        # Main horizontal plate for NEMA 17
        motor_plate = (
            cq.Workplane("XY")
            .workplane(offset=carriage_height - mount_plate_thickness)
            .center(-25, 25) # Offset relative to bearing
            .rect(42, 42)
            .extrude(mount_plate_thickness)
        )
        
        # Support gusset
        gusset = (
            cq.Workplane("YZ")
            .center(25, carriage_height/2)
            .polyline([(0,0), (20, 0), (0, -20)]).close()
            .extrude(4)
            .translate((-25, 0, 0))
        )
        
        full_mount = motor_plate.union(gusset)
        
        # Cut motor hole
        full_mount = (
            full_mount.faces(">Z").workplane()
            .center(-25, 25) # Match center
            .hole(motor_pilot_diam)
        )
        
        # Cut mounting screw holes (NEMA 17 pattern)
        full_mount = (
            full_mount.faces(">Z").workplane()
            .center(-25, 25)
            .rect(31, 31, forConstruction=True)
            .vertices()
            .hole(3.5)
        )
        
        main_body = main_body.union(full_mount)

    return main_body

def create_end_effector():
    """
    Creates the center piece (looks like a tool head or fan duct mount base).
    """
    w = 40
    d = 40
    h = 15
    
    base = cq.Workplane("XY").rect(w, d).extrude(h)
    
    # Fillet corners
    base = base.edges("|Z").fillet(4.0)
    
    # Hollow out the center
    cutout = (
        cq.Workplane("XY")
        .rect(w - wall_thickness*2, d - wall_thickness*2)
        .extrude(h)
        .translate((0,0, wall_thickness))
    )
    
    base = base.cut(cutout)
    
    # Cut front U-shape
    u_cut = (
        cq.Workplane("XZ")
        .center(0, h)
        .circle(8)
        .extrude(d + 10)
        .translate((0, -d/2, 0))
    )
    base = base.cut(u_cut)
    
    # Add mounting holes on sides
    base = (
        base.faces(">Y").workplane()
        .rect(w - 10, h - 6, forConstruction=True)
        .vertices()
        .hole(screw_hole_diam)
    )
    
    # Add vertical feature on back
    vertical_mount = (
        cq.Workplane("XY")
        .center(0, d/2)
        .rect(20, 10)
        .extrude(35)
    )
    
    # Bearing holes in vertical mount
    vertical_mount = (
        vertical_mount.faces(">Y").workplane()
        .center(0, 10)
        .hole(bearing_bore_diam) # Top bearing
        .center(0, -15) # Spacing
        .hole(bearing_bore_diam) # Bottom bearing
    )
    
    result = base.union(vertical_mount)
    
    return result

def create_tensioner_clip():
    """
    Creates the small clip-like part shown in the center/bottom.
    """
    length = 25
    width = 12
    height = 15
    
    body = cq.Workplane("XY").rect(length, width).extrude(height)
    
    # Slot cut
    slot = (
        cq.Workplane("XY")
        .rect(length - 8, 2)
        .extrude(height)
    )
    
    # Screw holes
    body = (
        body.faces(">Y").workplane()
        .center(0, 0)
        .rect(10, 0, forConstruction=True) # spacing
        .vertices()
        .hole(screw_hole_diam)
    )
    
    # Make it wavy/flexible profile (simplified)
    cut_prof = (
        cq.Workplane("XY")
        .move(-5, 0)
        .lineTo(5, 5)
        .lineTo(5, -5)
        .close()
        .extrude(height)
    )
    
    # Add adjustment tab
    tab = (
        cq.Workplane("XY")
        .rect(10, 20)
        .extrude(2)
        .translate((-length/2 - 5, 0, 0))
    )
    
    # Slot in tab
    tab = (
        tab.faces(">Z").workplane()
        .center(-length/2 - 5, 0)
        .slot2D(8, 3.2, 0)
        .cutThruAll()
    )
    
    return body.cut(slot).union(tab)

# --- Assembly Construction ---

# 1. Left Vertical Carriage (Motor Mount style)
part1 = create_vertical_carriage(is_motor_mount=True).translate((50, 50, 0))

# 2. Right Vertical Carriage (Idler/Mirror style)
part2 = create_vertical_carriage(is_motor_mount=True).mirror("YZ").translate((-50, 50, 0))

# 3. Bottom Left End Effector / Tool Head base
part3 = create_end_effector().translate((-60, -50, 0))

# 4. Small tensioner clip
part4 = create_tensioner_clip().translate((0, -20, 0))

# 5. Simple block (idler mount spacer)
part5 = (
    cq.Workplane("XY")
    .rect(20, 10)
    .extrude(15)
    .faces(">Y").workplane().rect(10, 0, forConstruction=True).vertices().hole(3.2)
    .translate((20, -20, 0))
)

# 6. Another vertical tower variant (simpler)
part6 = create_vertical_carriage().translate((-80, 0, 0))


# Combine into one result for display (though physically separate parts)
result = (
    part1
    .union(part2)
    .union(part3)
    .union(part4)
    .union(part5)
    .union(part6)
)