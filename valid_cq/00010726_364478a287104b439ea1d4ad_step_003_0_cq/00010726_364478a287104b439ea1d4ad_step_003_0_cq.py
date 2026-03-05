import cadquery as cq

# --- Parametric Dimensions ---
# Main Body
body_length = 60.0
body_width = 30.0
body_height = 55.0
fillet_radius = 2.0

# Mounting Flanges
flange_thickness = 3.0
flange_width = 8.0  # How much it sticks out from the side
flange_length = body_length
flange_z_offset_top = 10.0 # Distance from top face down
flange_z_offset_bottom = 10.0 # Distance from bottom face up
hole_dia = 3.2
hole_spacing_x = 45.0  # Spacing along length

# Output Gear/Horn
horn_dia = 25.0
horn_height = 3.0
horn_center_offset = 12.0 # Offset from center of body along length
horn_hole_pcd = 18.0 # Pitch Circle Diameter for small holes
horn_hole_dia = 2.0
num_horn_holes = 8
shaft_boss_dia = 10.0
shaft_boss_height = 3.0
shaft_dia = 6.0
shaft_height = 4.0

# Side Protrusion (Connector housing)
prot_width = 15.0
prot_height = 20.0
prot_depth = 5.0
prot_pos_z = -10.0 # Relative to center
prot_pos_x = -15.0 # Relative to center

# Top Indentation
top_indent_width = 15.0
top_indent_length = 25.0
top_indent_depth = 0.5
top_indent_offset = -12.0 # Offset towards back

# --- Modeling ---

# 1. Main Body
main_body = (
    cq.Workplane("XY")
    .box(body_length, body_width, body_height)
    .edges("|Z")
    .fillet(fillet_radius)
)

# 2. Side Mounting Flanges
# We will create one flange profile and extrude/mirror it
flange_sketch = (
    cq.Workplane("XY")
    .rect(body_length, body_width + 2 * flange_width) # Overall dimensions including flanges
    .rect(body_length, body_width) # Cutout for body
    .extrude(flange_thickness)
)

# Position Top Flange
top_flange = flange_sketch.translate((0, 0, body_height/2 - flange_z_offset_top - flange_thickness/2))

# Position Bottom Flange
bottom_flange = flange_sketch.translate((0, 0, -body_height/2 + flange_z_offset_bottom + flange_thickness/2))

# Add mounting holes to flanges
def add_flange_holes(workplane):
    return (
        workplane
        .faces(">Z")
        .workplane()
        .rect(hole_spacing_x, body_width + flange_width, forConstruction=True) # Construction rect for hole centers
        .vertices()
        .hole(hole_dia)
    )

# Since the rect logic above puts holes on the corners of the construction rect, 
# we need to be careful. The construction rect centers the holes.
# Let's drill specifically.
top_flange = (
    top_flange
    .faces(">Z")
    .workplane()
    .pushPoints([
        (hole_spacing_x/2, (body_width + flange_width)/2),
        (hole_spacing_x/2, -(body_width + flange_width)/2),
        (-hole_spacing_x/2, (body_width + flange_width)/2),
        (-hole_spacing_x/2, -(body_width + flange_width)/2),
    ])
    .hole(hole_dia)
)

bottom_flange = (
    bottom_flange
    .faces(">Z")
    .workplane()
    .pushPoints([
        (hole_spacing_x/2, (body_width + flange_width)/2),
        (hole_spacing_x/2, -(body_width + flange_width)/2),
        (-hole_spacing_x/2, (body_width + flange_width)/2),
        (-hole_spacing_x/2, -(body_width + flange_width)/2),
    ])
    .hole(hole_dia)
)

# 3. Output Assembly (Top Horn)
horn_center = (horn_center_offset, 0, body_height/2)

output_horn = (
    cq.Workplane("XY")
    .workplane(offset=body_height/2)
    .center(horn_center_offset, 0)
    .circle(horn_dia/2).extrude(horn_height)
    .faces(">Z").workplane()
    .circle(shaft_boss_dia/2).extrude(shaft_boss_height)
    .faces(">Z").workplane()
    .circle(shaft_dia/2).extrude(shaft_height)
)

# Add holes to the horn
output_horn = (
    output_horn
    .faces(">Z").workplane(offset=-shaft_height-shaft_boss_height) # Go back to horn face
    .center(horn_center_offset, 0) # Re-center on global coord
    .polygon(num_horn_holes, horn_hole_pcd) # Use polygon vertices for hole locations
    .vertices()
    .hole(horn_hole_dia, depth=horn_height)
)

# 4. Side Protrusion (Connector)
side_prot = (
    cq.Workplane("YZ")
    .workplane(offset=-body_length/2) # Start at negative X face
    .center(0, prot_pos_z)
    .rect(prot_width, prot_height)
    .extrude(-prot_depth) # Extrude outwards (negative X direction relative to local plane)
)
# Move it to the correct X position on the side of the box
side_prot = side_prot.translate((-body_length/2 + prot_depth + prot_pos_x, body_width/2, 0))

# Actually, looking at the image, the protrusion is on the side face (XZ plane or YZ plane depending on orientation). 
# Let's assume Length is X, Width is Y. The protrusion is on the +Y face.
side_prot = (
    cq.Workplane("XZ")
    .workplane(offset=body_width/2)
    .center(prot_pos_x, prot_pos_z)
    .rect(prot_width, prot_height)
    .extrude(prot_depth)
)


# 5. Top Indentation (Label area)
# Create a tool to cut the indentation
indent_cut = (
    cq.Workplane("XY")
    .workplane(offset=body_height/2)
    .center(top_indent_offset, 0)
    .rect(top_indent_length, top_indent_width)
    .extrude(-top_indent_depth)
    .edges("|Z").fillet(1.0) # Small fillet on the indent corners
)

# 6. Combine all parts
result = (
    main_body
    .union(top_flange)
    .union(bottom_flange)
    .union(output_horn)
    .union(side_prot)
    .cut(indent_cut)
)

# Optional: Add small fillets to the connection of the flanges to the body for realism
# This can be computationally expensive, so it's often omitted in basic models, 
# but adds to the "molded" look.
# result = result.edges("(>Z or <Z) and (not |Z)").fillet(0.5)

# Export or visualization
if 'show_object' in globals():
    show_object(result)