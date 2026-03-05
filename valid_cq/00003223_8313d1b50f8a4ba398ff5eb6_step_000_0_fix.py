import cadquery as cq

# Main mounting bracket assembly
# This appears to be a DIN rail or panel mounting bracket with hooks

# Parameters
plate_width = 120
plate_height = 80
plate_thick = 3

side_height = 100
side_width = 20
side_thick = 3

hook_width = 15
hook_depth = 10
hook_thick = 3

# Create the main horizontal backplate
backplate = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thick)
)

# Add rectangular cutout in center of backplate
backplate = (
    backplate
    .faces(">Z")
    .workplane()
    .rect(30, 25)
    .cutThruAll()
)

# Add mounting holes to backplate
backplate = (
    backplate
    .faces(">Z")
    .workplane()
    .pushPoints([(-35, 20), (35, 20), (-35, -20), (35, -20),
                 (-10, 20), (10, 20), (-10, -20), (10, -20)])
    .circle(2)
    .cutThruAll()
)

# Create left side panel (vertical)
left_panel = (
    cq.Workplane("XZ")
    .transformed(offset=(-plate_width/2 - side_width/2, 0, plate_height/2 - side_height/2 + plate_thick/2))
    .rect(side_width, side_height)
    .extrude(side_thick)
)

# Create right side panel (vertical)
right_panel = (
    cq.Workplane("XZ")
    .transformed(offset=(plate_width/2 + side_width/2, 0, plate_height/2 - side_height/2 + plate_thick/2))
    .rect(side_width, side_height)
    .extrude(side_thick)
)

# Top hooks for left panel
left_top_hook = (
    cq.Workplane("XZ")
    .transformed(offset=(-plate_width/2 - side_width/2, 0, plate_height/2 + side_height/2 - hook_depth/2 + plate_thick/2))
    .rect(hook_width + side_width, hook_depth)
    .extrude(hook_thick)
)

# Bottom hooks for left panel
left_bottom_hook = (
    cq.Workplane("XZ")
    .transformed(offset=(-plate_width/2 - side_width/2 + hook_width/2, 0, plate_height/2 - side_height/2 - hook_depth/2 + plate_thick/2))
    .rect(hook_width, hook_depth)
    .extrude(hook_thick)
)

# Top hooks for right panel
right_top_hook = (
    cq.Workplane("XZ")
    .transformed(offset=(plate_width/2 + side_width/2, 0, plate_height/2 + side_height/2 - hook_depth/2 + plate_thick/2))
    .rect(hook_width + side_width, hook_depth)
    .extrude(hook_thick)
)

# Bottom hooks for right panel
right_bottom_hook = (
    cq.Workplane("XZ")
    .transformed(offset=(plate_width/2 + side_width/2 - hook_width/2, 0, plate_height/2 - side_height/2 - hook_depth/2 + plate_thick/2))
    .rect(hook_width, hook_depth)
    .extrude(hook_thick)
)

# Left slot cutout in backplate
left_slot = (
    cq.Workplane("XY")
    .transformed(offset=(-plate_width/2 + 15, 0, 0))
    .rect(8, 40)
    .extrude(plate_thick + 1)
)

right_slot = (
    cq.Workplane("XY")
    .transformed(offset=(plate_width/2 - 15, 0, 0))
    .rect(8, 40)
    .extrude(plate_thick + 1)
)

# Combine all parts
result = (
    backplate
    .union(left_panel)
    .union(right_panel)
    .union(left_top_hook)
    .union(left_bottom_hook)
    .union(right_top_hook)
    .union(right_bottom_hook)
    .cut(left_slot)
    .cut(right_slot)
)