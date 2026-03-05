import cadquery as cq

# --- Parameters ---
# Main body dimensions
total_width = 80.0
total_depth = 40.0
thickness = 10.0

# Central bridge dimensions
bridge_width = 40.0 # The width of the connecting section
bridge_depth = 15.0 # The depth (Y) of the connecting section

# Side mounting block dimensions
side_block_width = (total_width - bridge_width) / 2
side_block_depth = total_depth

# Feature dimensions
fillet_radius = 5.0
chamfer_size = 1.0

# Vertical holes (side blocks)
side_hole_dia = 4.0
side_hole_offset_y = 10.0 # From the front edge

# Clamp/Split features
split_gap_width = 1.0
clamp_hole_dia = 5.0
clamp_hole_center_offset = 12.0 # From center of bridge outwards

# Horizontal holes (for clamping screws)
horiz_screw_dia = 2.5
horiz_screw_depth = 20.0

# Text parameters
text_string = "B"
text_size = 10.0
text_depth = 1.0

# --- Geometry Construction ---

# 1. Base Shape
# We'll create the basic U-shape first. 
# We can do this by sketching on the XY plane.
base = (
    cq.Workplane("XY")
    .moveTo(-total_width/2, 0)
    .lineTo(-total_width/2, -total_depth)
    .lineTo(-total_width/2 + side_block_width, -total_depth)
    .lineTo(-total_width/2 + side_block_width, -bridge_depth)
    .lineTo(total_width/2 - side_block_width, -bridge_depth)
    .lineTo(total_width/2 - side_block_width, -total_depth)
    .lineTo(total_width/2, -total_depth)
    .lineTo(total_width/2, 0)
    .close()
    .extrude(thickness)
)

# 2. Add Fillets to the outer corners of the "legs"
# Select vertical edges at the max Y (which is 0 in our sketch) and min Y
# Based on the image, the outer corners of the U-shape legs are rounded.
# Let's target the edges at Y = -total_depth
base = base.edges(f"|Z and <Y").fillet(fillet_radius)


# 3. Side Mounting Holes (Vertical)
# Holes in the "legs" of the U-shape
hole_y_pos = -total_depth + side_hole_offset_y
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints([
        (-(total_width/2 - side_block_width/2), hole_y_pos),
        ((total_width/2 - side_block_width/2), hole_y_pos)
    ])
    .hole(side_hole_dia)
)

# 4. Clamp Mechanism (Central Bridge)
# The image shows vertical holes with slits going to the back edge

# 4a. Vertical Clamp Holes
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints([
        (-clamp_hole_center_offset, -bridge_depth/2),
        (clamp_hole_center_offset, -bridge_depth/2)
    ])
    .hole(clamp_hole_dia)
)

# 4b. Slits
# Create a slot from the back edge (Y=0) into the holes
# We can do this by cutting a rectangular profile
slit_cutter = (
    cq.Workplane("XY")
    .rect(split_gap_width, bridge_depth) # Make it deep enough to reach holes
    .extrude(thickness)
    .translate((-clamp_hole_center_offset, -bridge_depth/2, 0)) # Position left
)
slit_cutter_right = (
    cq.Workplane("XY")
    .rect(split_gap_width, bridge_depth)
    .extrude(thickness)
    .translate((clamp_hole_center_offset, -bridge_depth/2, 0)) # Position right
)

base = base.cut(slit_cutter).cut(slit_cutter_right)

# 5. Horizontal Clamping Screw Holes
# These go through the side face into the clamp area.
# Based on the image, they are on the front face of the bridge section.
# Looking at the image, there are small holes on the front vertical face of the bridge.

base = (
    base.faces(">Y").workplane(centerOption="CenterOfBoundBox")
    .pushPoints([
        (-clamp_hole_center_offset, -thickness/2),
        (clamp_hole_center_offset, -thickness/2)
    ])
    .hole(horiz_screw_dia, depth=bridge_depth) # Drill inwards
)

# 6. Embossed/Cut Text "B"
# Located on the top face, center of the bridge
base = (
    base.faces(">Z").workplane()
    .text(text_string, text_size, -text_depth) # Negative depth for cut
)

# 7. Final assignment
result = base