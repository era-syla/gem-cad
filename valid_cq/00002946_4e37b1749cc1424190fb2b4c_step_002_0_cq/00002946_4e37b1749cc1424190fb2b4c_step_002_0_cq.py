import cadquery as cq

# Parametric Dimensions
# Base plate
base_width = 80.0
base_length = 150.0
base_thickness = 2.0

# Circular Disk
disk_outer_radius = 40.0
disk_inner_radius = 20.0
disk_thickness = 2.0
disk_height_offset = 30.0  # Height above the base plate

# Clamp Mechanism
clamp_block_width = 15.0
clamp_block_length = 25.0
clamp_block_height = 15.0
clamp_slot_width = 5.0
clamp_slot_depth = 10.0
clamp_pin_radius = 2.0
clamp_tab_length = 15.0
clamp_tab_thickness = 2.0

# Small holes for alignment/visuals
hole_radius = 1.0

# Create the Base Plate
# A simple rectangular plate
base_plate = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_thickness)
)

# Create the Floating Disk (Ring)
# A washer-like shape positioned above the base plate
disk = (
    cq.Workplane("XY")
    .workplane(offset=disk_height_offset)
    .circle(disk_outer_radius)
    .circle(disk_inner_radius)
    .extrude(disk_thickness)
)

# Create the Clamp Mechanism
# This is attached to the edge of the disk.
# We'll build a U-shaped block and a tab.

# 1. The main block with a slot
clamp_body = (
    cq.Workplane("XY")
    .workplane(offset=disk_height_offset + disk_thickness)
    .box(clamp_block_length, clamp_block_width, clamp_block_height, centered=(True, True, False))
)

# Cut the slot in the clamp body
clamp_body = (
    clamp_body
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(clamp_slot_width, clamp_block_width + 1) # +1 to ensure cut through
    .cutBlind(-clamp_slot_depth)
)

# 2. Add the pin going through the clamp
pin = (
    cq.Workplane("YZ")
    .workplane(offset=disk_height_offset + disk_thickness + clamp_block_height/2 + 2) # Adjust height relative to global
    .center(0, 5) # Rough positioning
    .circle(clamp_pin_radius)
    .extrude(clamp_block_length + 5) # Make it longer than the block
    .translate((- (clamp_block_length + 5)/2, 0, 0)) # Center the extrusion
    .rotate((0,0,0), (0,1,0), 90) # Reorient if needed, but YZ plane extrude creates X-axis cylinder
)
# Actually, easier to just build it in place relative to the clamp body
pin_rel = (
    cq.Workplane("YZ")
    .workplane(offset=0) # centered on X
    .center(0, disk_height_offset + disk_thickness + clamp_block_height - 5) # height Z
    .circle(clamp_pin_radius)
    .extrude(clamp_block_length + 4, both=True)
)


# 3. Add the protruding tab at the back of the clamp
tab = (
    cq.Workplane("XY")
    .workplane(offset=disk_height_offset + disk_thickness)
    .box(clamp_tab_length, clamp_block_width, clamp_tab_thickness, centered=(False, True, False))
    .translate((clamp_block_length/2, 0, 0))
)

# Assemble the Clamp parts
clamp_assembly = clamp_body.union(tab).union(pin_rel)

# Position the clamp on the edge of the disk
# Move to the right edge of the disk
clamp_assembly = clamp_assembly.translate((disk_outer_radius - 5, 0, 0))

# Add mounting holes to the base plate to mimic the image
# (3 holes in a triangle pattern roughly under the disk shadow)
base_with_holes = (
    base_plate
    .faces(">Z")
    .workplane()
    .pushPoints([(20, 0), (-10, 20), (-10, -20)])
    .circle(hole_radius)
    .cutBlind(-base_thickness)
)

# Add a hole on the disk as seen in the image (left side)
disk_with_hole = (
    disk
    .faces(">Z")
    .workplane()
    .pushPoints([(-disk_inner_radius - (disk_outer_radius-disk_inner_radius)/2, 0)])
    .circle(hole_radius)
    .cutBlind(-disk_thickness)
)

# Combine everything
result = base_with_holes.union(disk_with_hole).union(clamp_assembly)