import cadquery as cq

# --- Parameter Definitions ---
# Base Plate parameters
bp_length = 140
bp_width = 50
bp_thick = 8
bp_hole_dia = 15
bp_cb_dia = 20
bp_cb_depth = 4

# General block parameters
block_size = 35
hole_mount_dia = 3.5

# --- Part Generation Functions ---

def create_base_plate():
    """Creates the long rectangular base plate with holes."""
    wp = cq.Workplane("XY").box(bp_length, bp_width, bp_thick)
    
    # Main counterbored holes
    wp = (wp.faces(">Z").workplane()
          .pushPoints([(-40, 0), (0, 0), (40, 0)])
          .cboreHole(bp_hole_dia, bp_cb_dia, bp_cb_depth))
    
    # Mounting holes pattern
    mount_pts = [
        (-60, 18), (-60, -18), (-20, 18), (-20, -18),
        (20, 18), (20, -18), (60, 18), (60, -18)
    ]
    wp = wp.faces(">Z").workplane().pushPoints(mount_pts).hole(4.5)
    return wp

def create_u_block():
    """Creates the U-shaped bearing blocks."""
    wp = cq.Workplane("XY").box(30, 30, 15)
    # Cut arch/tunnel on bottom
    wp = (wp.faces(">Y").workplane()
          .center(0, -7.5) # Offset to bottom
          .circle(8)
          .cutThruAll())
    # Mounting holes on corners
    wp = (wp.faces(">Z").workplane()
          .pushPoints([(-10, 10), (10, 10), (-10, -10), (10, -10)])
          .hole(3))
    return wp

def create_housing_tall():
    """Creates the taller central housing block."""
    wp = cq.Workplane("XY").box(36, 36, 30)
    # Central bore
    wp = wp.faces(">Z").workplane().hole(18)
    # Corner mounting holes
    wp = (wp.faces(">Z").workplane()
          .pushPoints([(-13, 13), (13, 13), (-13, -13), (13, -13)])
          .hole(3))
    return wp

def create_housing_short():
    """Creates the shorter housing block with bottom cutout."""
    wp = cq.Workplane("XY").box(36, 36, 20)
    wp = wp.faces(">Z").workplane().hole(18)
    # Rectangular cutout at bottom face
    wp = (wp.faces("<Y").workplane()
          .center(0, -10)
          .rect(20, 15)
          .cutThruAll())
    return wp

def create_cover_plate():
    """Creates the plate with a central boss."""
    wp = cq.Workplane("XY").box(36, 36, 4)
    # Boss
    wp = wp.faces(">Z").workplane().circle(12).extrude(8)
    # Detail on boss (pin)
    wp = wp.faces(">Z").workplane().circle(4).extrude(2)
    return wp

def create_key():
    """Creates small rectangular key."""
    return cq.Workplane("XY").box(10, 30, 10)

def create_bearing_support():
    """Creates the rectangular block with central hole."""
    wp = cq.Workplane("XY").box(36, 25, 12)
    wp = wp.faces(">Z").workplane().hole(14)
    wp = wp.faces(">Z").workplane().pushPoints([(-13, 0), (13, 0)]).hole(3)
    return wp

def create_c_clip():
    """Creates the small C-shaped part."""
    wp = cq.Workplane("XY").box(25, 25, 8)
    wp = wp.faces(">Z").workplane().hole(10)
    # Cut side to open it
    wp = wp.faces(">Y").workplane().rect(12, 25).cutThruAll()
    return wp

def create_frame():
    """Creates the double-window frame."""
    wp = cq.Workplane("XY").box(80, 60, 2)
    wp = (wp.faces(">Z").workplane()
          .pushPoints([(-20, 0), (20, 0)])
          .rect(30, 50)
          .cutThruAll())
    return wp

def create_pin():
    """Creates a small pin/plug."""
    return cq.Workplane("XY").circle(6).extrude(12).faces(">Z").fillet(1)

# --- Assembly Construction ---

# Create individual parts
part_base = create_base_plate()
part_u1 = create_u_block()
part_u2 = create_u_block()
part_cover = create_cover_plate()
part_housing_tall = create_housing_tall()
part_housing_short = create_housing_short()
part_key1 = create_key()
part_key2 = create_key()
part_support = create_bearing_support()
part_clip = create_c_clip()
part_frame = create_frame()
part_pin = create_pin()

# Assemble them into a single compound result, arranged as per the exploded view image
# Coordinates approximate the visual layout
result = part_base.translate((0, -80, 0))
result = result.union(part_u1.translate((-95, -30, 0)))
result = result.union(part_u2.translate((-115, 10, 0))) # Rotated or just offset
result = result.union(part_cover.translate((-65, 20, 0)))
result = result.union(part_pin.translate((-45, 50, 0)))
result = result.union(part_housing_tall.translate((-20, 20, 0)))
result = result.union(part_housing_short.translate((25, 20, 0)))
result = result.union(part_key1.translate((55, 30, 0)))
result = result.union(part_key2.translate((70, 30, 0)))
result = result.union(part_support.translate((100, 20, 0)))
result = result.union(part_clip.translate((130, 30, 0)))
result = result.union(part_frame.translate((170, 0, 0)))
