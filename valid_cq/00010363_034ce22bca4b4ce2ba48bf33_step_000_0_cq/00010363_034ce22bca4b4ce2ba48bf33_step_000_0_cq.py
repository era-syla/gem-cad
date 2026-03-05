import cadquery as cq

# Parameters for the parts
thickness = 3.0  # Thickness of all plates
hole_dia = 4.0   # Diameter of mounting holes

# --- Part 1: U-Shaped Bracket ---
u_width = 40.0
u_height = 40.0
u_arm_width = 10.0
u_fillet = 3.0

part1 = (
    cq.Workplane("XY")
    .rect(u_width, u_height)
    .rect(u_width - 2*u_arm_width, u_height - u_arm_width)
    .extrude(thickness)
    # Cut the opening to make it a U-shape
    .cut(
        cq.Workplane("XY")
        .center(0, -u_height/2 + (u_height - u_arm_width)/2)
        .rect(u_width - 2*u_arm_width, u_height - u_arm_width)
        .extrude(thickness)
    )
    # Add holes on the arms
    .faces(">Z").workplane()
    .pushPoints([
        (-u_width/2 + u_arm_width/2, u_height/2 - u_arm_width/2), # Top Left
        (u_width/2 - u_arm_width/2, u_height/2 - u_arm_width/2),  # Top Right
        (-u_width/2 + u_arm_width/2, -u_height/2 + u_arm_width/2), # Bottom Left
        (u_width/2 - u_arm_width/2, -u_height/2 + u_arm_width/2),  # Bottom Right
    ])
    .hole(hole_dia)
    .edges("|Z").fillet(u_fillet)
)

# --- Part 2: Small L-Bracket ---
l_arm_length = 30.0
l_arm_width = 10.0
l_fillet = 2.0

# Create basic L shape sketch
l_sketch = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(0, l_arm_length)
    .lineTo(l_arm_width, l_arm_length)
    .lineTo(l_arm_width, l_arm_width)
    .lineTo(l_arm_length, l_arm_width)
    .lineTo(l_arm_length, 0)
    .close()
    .extrude(thickness)
)

# Add holes
part2 = (
    l_sketch
    .faces(">Z").workplane()
    .pushPoints([
        (l_arm_width/2, l_arm_length - l_arm_width/2), # Vertical arm tip
        (l_arm_length - l_arm_width/2, l_arm_width/2),  # Horizontal arm tip
        (l_arm_width/2, l_arm_width/2)                  # Corner
    ])
    .hole(hole_dia)
    .edges("|Z").fillet(l_fillet)
)

# --- Part 3: Square Motor Mount Plate ---
sq_size = 40.0
sq_center_hole = 22.0
sq_fillet = 3.0
sq_mount_hole_spacing = 31.0 # NEMA 17 style spacing often

part3 = (
    cq.Workplane("XY")
    .rect(sq_size, sq_size)
    .extrude(thickness)
    .faces(">Z").workplane()
    .hole(sq_center_hole)
    .faces(">Z").workplane()
    .rect(sq_mount_hole_spacing, sq_mount_hole_spacing, forConstruction=True)
    .vertices()
    .hole(hole_dia)
    .edges("|Z").fillet(sq_fillet)
)

# --- Part 4: Large V-Bracket (90 degree) ---
v_arm_length = 40.0 # From corner
v_arm_width = 10.0
v_angle = 90.0

# We'll construct this by rotating two rectangles and unioning
leg1 = cq.Workplane("XY").rect(v_arm_width, v_arm_length).extrude(thickness)
leg2 = cq.Workplane("XY").rect(v_arm_length, v_arm_width).extrude(thickness)

# Align them to form a corner
leg1 = leg1.translate((-v_arm_length/2 + v_arm_width/2, v_arm_length/2 - v_arm_width/2, 0))
leg2 = leg2.translate((0, 0, 0)) # Centered

# Rough approximation of the V-shape in the image
part4_raw = (
    cq.Workplane("XY")
    .moveTo(0,0)
    .lineTo(0, v_arm_length)
    .lineTo(v_arm_width, v_arm_length)
    .lineTo(v_arm_width, v_arm_width) # Inner corner
    .lineTo(v_arm_length, v_arm_width)
    .lineTo(v_arm_length, 0)
    .close()
    .extrude(thickness)
)

part4 = (
    part4_raw
    .faces(">Z").workplane()
    .pushPoints([
        (v_arm_width/2, v_arm_length - v_arm_width/2),
        (v_arm_length - v_arm_width/2, v_arm_width/2),
        (v_arm_width/2, v_arm_width/2)
    ])
    .hole(hole_dia)
    .edges("|Z").fillet(2.0)
)

# --- Assembly / Layout ---
# Arrange parts in a line as seen in the image
spacing = 60.0

final_part1 = part1.translate((-1.5 * spacing, 0, 0))
final_part2 = part2.translate((-0.5 * spacing, -l_arm_width/2, 0)) # Slight adjust for visual center
final_part3 = part3.translate((0.5 * spacing, 0, 0))
final_part4 = part4.translate((1.5 * spacing, -v_arm_width/2, 0))

# Combine into one object for the 'result' variable
result = final_part1.union(final_part2).union(final_part3).union(final_part4)