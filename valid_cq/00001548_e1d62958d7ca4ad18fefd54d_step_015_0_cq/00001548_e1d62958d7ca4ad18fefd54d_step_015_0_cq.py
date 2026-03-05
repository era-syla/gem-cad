import cadquery as cq

# --- Parameters ---

# Spoked Wheel Parameters
wheel_outer_dia = 30.0
wheel_rim_width = 3.0
wheel_hub_dia = 6.0
wheel_thickness = 3.0
wheel_axle_hole = 2.0
num_spokes = 6
spoke_width = 2.0

# Slotted Disk Parameters
slot_disk_dia = 35.0
slot_disk_thick = 3.0
slot_length = 15.0
slot_width = 2.0
slot_offset_from_center = 5.0 # Start of slot relative to center

# Solid Disk Parameters
solid_disk_dia = 30.0
solid_disk_thick = 4.0
solid_disk_hole = 3.0

# Bracket/Holder Parameters
bracket_length = 30.0
bracket_width = 15.0
bracket_height = 12.0
bracket_wall_thick = 3.0
bracket_tab_length = 10.0
bracket_tab_hole = 2.0

# --- Geometry Generation ---

# 1. Spoked Wheel
def create_spoked_wheel():
    # Create the main disk
    wheel = cq.Workplane("XY").circle(wheel_outer_dia / 2).extrude(wheel_thickness)
    
    # Create the cutout for spokes (pie wedge shape concept, but simpler to cut sectors)
    # We will cut out sectors between the rim and hub
    
    # Inner and outer radii for the "void" area
    r_inner = wheel_hub_dia / 2
    r_outer = (wheel_outer_dia / 2) - wheel_rim_width
    
    # Create a single cutter shape (a sector)
    # Actually, it's easier to make the rim and hub, then add spokes
    
    # Method 2: Rim + Hub + Spokes
    rim = cq.Workplane("XY").circle(wheel_outer_dia/2).circle(wheel_outer_dia/2 - wheel_rim_width).extrude(wheel_thickness)
    hub = cq.Workplane("XY").circle(wheel_hub_dia/2).extrude(wheel_thickness)
    
    spokes = cq.Workplane("XY")
    for i in range(num_spokes):
        angle = i * (360.0 / num_spokes)
        # Create a rectangular spoke rotated
        s = (cq.Workplane("XY")
             .rect(wheel_outer_dia/2, spoke_width, centered=False) # Start from center outward
             .translate((-wheel_hub_dia/4, -spoke_width/2, 0)) # Slight overlap adjustment
             .rotate((0,0,0), (0,0,1), angle)
             .extrude(wheel_thickness))
        spokes = spokes.union(s)
        
    final_wheel = rim.union(hub).union(spokes)
    
    # Cut axle hole
    final_wheel = final_wheel.faces(">Z").workplane().circle(wheel_axle_hole/2).cutThruAll()
    
    return final_wheel

# 2. Slotted Disk (Top Right)
def create_slotted_disk():
    disk = cq.Workplane("XY").circle(slot_disk_dia/2).extrude(slot_disk_thick)
    
    # Cut the slot
    # Slot position seems radial
    slot = (cq.Workplane("XY")
            .center(slot_offset_from_center + slot_length/2, 0)
            .rect(slot_length, slot_width)
            .extrude(slot_disk_thick, combine=False))
            
    final_disk = disk.cut(slot)
    return final_disk

# 3. Solid Disk with Hole (Bottom Left)
def create_solid_disk():
    disk = (cq.Workplane("XY")
            .circle(solid_disk_dia/2)
            .extrude(solid_disk_thick))
    
    # Cut center hole
    final_disk = disk.faces(">Z").workplane().circle(solid_disk_hole/2).cutThruAll()
    return final_disk

# 4. U-Bracket with Tab (Center)
def create_bracket():
    # U-shape profile
    profile = (cq.Workplane("YZ")
               .rect(bracket_width, bracket_height)
               .rect(bracket_width - 2*bracket_wall_thick, bracket_height - bracket_wall_thick) # Inner cut
               .translate((0, bracket_wall_thick/2, 0)) # Shift up so bottom is solid
    )
    
    # This creates a hollow rect, we need a U shape. 
    # Let's do it by drawing the U-shape points explicitly or cutting a block.
    
    # Block method
    block = cq.Workplane("XY").box(bracket_length, bracket_width, bracket_height)
    
    # Cut the U-channel
    cutter = (cq.Workplane("XY")
              .box(bracket_length, bracket_width - 2*bracket_wall_thick, bracket_height - bracket_wall_thick)
              .translate((0, 0, bracket_wall_thick/2))) # Shift up
              
    u_channel = block.cut(cutter)
    
    # Add the tab
    tab = (cq.Workplane("XY")
           .box(bracket_tab_length, bracket_width, bracket_wall_thick)
           .translate((-bracket_length/2 - bracket_tab_length/2, 0, -bracket_height/2 + bracket_wall_thick/2)))
           
    combined = u_channel.union(tab)
    
    # Hole in tab
    final_bracket = (combined.faces(">Z").workplane()
                     .center(-bracket_length/2 - bracket_tab_length/2, 0)
                     .circle(bracket_tab_hole/2)
                     .cutThruAll())
                     
    return final_bracket

# --- Assembly / Positioning ---

part1 = create_spoked_wheel().translate((-20, 30, 0))
part2 = create_slotted_disk().translate((30, 20, 0))
part3 = create_solid_disk().translate((-25, -25, 0))
part4 = create_bracket().translate((10, -10, bracket_height/2)) # Lift bracket to sit on XY plane

# Combine all parts into one result
result = part1.union(part2).union(part3).union(part4)
