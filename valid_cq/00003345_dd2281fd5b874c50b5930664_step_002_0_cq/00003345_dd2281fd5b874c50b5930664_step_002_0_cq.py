import cadquery as cq

# --- Parameters ---

# Base dimensions
base_length = 150.0
base_width = 30.0
base_height = 8.0

# Cavity (pocket) dimensions
pocket_length = 100.0
pocket_width = 20.0
pocket_depth = 4.0
pocket_offset_x = -15.0 # Shifts the pocket relative to center to leave space at one end

# Switch/Button unit parameters
num_switches = 5
switch_pitch = pocket_length / num_switches  # Distance between switch centers
switch_width = 16.0
switch_length = 14.0
switch_base_height = 2.0  # Height from bottom of pocket
ramp_height = 4.0
hole_diameter = 1.5

# --- Geometry Construction ---

# 1. Create the main base block
base = cq.Workplane("XY").box(base_length, base_width, base_height)

# 2. Cut the main pocket
# The pocket is centered on Y, but offset on X
pocket = (
    base.faces(">Z")
    .workplane()
    .center(pocket_offset_x, 0)
    .rect(pocket_length, pocket_width)
    .cutBlind(-pocket_depth)
)

# 3. Define the single switch geometry
def create_switch():
    # Base square of the switch
    sw = (
        cq.Workplane("XY")
        .box(switch_length, switch_width, switch_base_height)
    )
    
    # Add the ramped part
    # We'll create a wedge or sketch profile to extrude
    # Let's use a side profile extrusion for the ramp shape
    
    # Profile points for the ramp (side view)
    # Origin is at the center of the switch base
    half_len = switch_length / 2.0
    half_wid = switch_width / 2.0
    
    # The ramp starts halfway along the length and goes up
    # Let's model the upper "rocker" part
    rocker_len = switch_length * 0.9
    
    # Create the stepped shape on top
    # A block for the flat part
    flat_part_len = rocker_len * 0.4
    flat_part = (
        cq.Workplane("XY")
        .workplane(offset=switch_base_height/2)
        .center(-rocker_len/2 + flat_part_len/2, 0)
        .box(flat_part_len, switch_width, ramp_height)
    )
    
    # A wedge for the sloped part
    wedge_len = rocker_len * 0.6
    wedge = (
        cq.Workplane("XY")
        .workplane(offset=switch_base_height/2)
        .center(rocker_len/2 - wedge_len/2, 0)
        .box(wedge_len, switch_width, ramp_height)
    )
    
    # Slice the wedge to make the slope
    # We cut a triangle off the top of the wedge box
    cutter = (
        cq.Workplane("XZ")
        .workplane(offset=switch_width/2 + 1) # Move outside
        .moveTo(rocker_len/2 - wedge_len, switch_base_height/2 + ramp_height) # Top left of wedge
        .lineTo(rocker_len/2, switch_base_height/2 + ramp_height) # Top right
        .lineTo(rocker_len/2, switch_base_height/2) # Bottom right
        .close()
        .extrude(-switch_width - 2)
    )
    
    # Add the small hole in the center of the flat part
    # Recalculate center relative to origin
    hole_center_x = -rocker_len/2 + flat_part_len/2
    
    switch_assy = sw.union(flat_part).union(wedge).cut(cutter)
    
    switch_assy = (
        switch_assy.faces(">Z").workplane()
        .center(hole_center_x, 0)
        .hole(hole_diameter, depth=2.0)
    )
    
    return switch_assy

# Generate one switch instance
switch_geo = create_switch()

# 4. Place the switches into the pocket
# Calculate starting position
start_x = pocket_offset_x - (pocket_length / 2) + (switch_pitch / 2)
z_level = (base_height / 2) - pocket_depth + (switch_base_height / 2)

final_body = pocket

for i in range(num_switches):
    pos_x = start_x + (i * switch_pitch)
    
    # Move the switch geometry to the correct location
    current_switch = (
        switch_geo
        .translate((pos_x, 0, z_level))
    )
    
    # Union with the main body
    final_body = final_body.union(current_switch)

# 5. Add the small side rails/guides inside the pocket (detail from image)
# There appear to be thin rails between the switches and the pocket wall
rail_thickness = 1.0
rail_height = pocket_depth * 0.6
rail_y_offset = (pocket_width / 2) - (rail_thickness / 2)

# Create rails on both sides
rail_left = (
    cq.Workplane("XY")
    .box(pocket_length, rail_thickness, rail_height)
    .translate((pocket_offset_x, rail_y_offset, z_level + (rail_height/2) - (switch_base_height/2)))
)

rail_right = (
    cq.Workplane("XY")
    .box(pocket_length, rail_thickness, rail_height)
    .translate((pocket_offset_x, -rail_y_offset, z_level + (rail_height/2) - (switch_base_height/2)))
)

final_body = final_body.union(rail_left).union(rail_right)

result = final_body