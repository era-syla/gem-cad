import cadquery as cq

# --- Parametric Dimensions ---
# Based on a standard 37mm diameter gear motor

# Main body (motor)
motor_diameter = 34.0
motor_length = 50.0

# Gearbox
gearbox_diameter = 37.0
gearbox_length = 35.0

# Output Shaft Collar/Boss
boss_diameter = 12.0
boss_length = 6.0

# Output Shaft
shaft_diameter = 6.0
shaft_length = 15.0
shaft_d_cut_depth = 0.5  # Depth of the D-cut

# Mounting Holes
hole_circle_diameter = 31.0
hole_diameter = 3.0
num_holes = 6

# --- Modeling ---

# 1. Create the Gearbox Housing (Front part)
gearbox = cq.Workplane("XY").circle(gearbox_diameter / 2).extrude(gearbox_length)

# 2. Create the Motor Body (Rear part)
# Attached to the back face of the gearbox
motor_body = (
    gearbox.faces("<Z")
    .workplane()
    .circle(motor_diameter / 2)
    .extrude(motor_length)
)

# 3. Create the Shaft Boss
# Attached to the front face of the gearbox
boss = (
    gearbox.faces(">Z")
    .workplane()
    .circle(boss_diameter / 2)
    .extrude(boss_length)
)

# 4. Create the Output Shaft with D-Cut
# Start with a full cylinder
shaft_base = (
    boss.faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
)

# Create the D-cut profile to subtract
# We calculate a rectangle that slices off the top part of the shaft
cut_height = (shaft_diameter / 2) - shaft_d_cut_depth
cut_box_width = shaft_diameter * 1.5 # Make sure it covers the width
cut_box_height = shaft_diameter # Arbitrary height, just needs to clear the top

shaft_d_cut = (
    shaft_base.faces(">Z")
    .workplane()
    .transformed(offset=(0, cut_height + cut_box_height/2, -shaft_length/2))
    .box(cut_box_width, cut_box_height, shaft_length, combine=False)
)

# Apply the cut
result_shaft = shaft_base.cut(shaft_d_cut)

# 5. Add Mounting Holes to the Gearbox face
# We select the front face of the gearbox again
mounting_holes = (
    gearbox.faces(">Z")
    .workplane()
    .polarArray(hole_circle_diameter/2, 0, 360, num_holes)
    .circle(hole_diameter / 2)
    .cutThruAll() # Cut through the gearbox length
)

# --- Assembly/Union ---
# Combine all solid parts (CadQuery operations often combine automatically if chained,
# but we need to ensure the logic flows correctly).

# Re-assembling the main flow because we branched for specific features
final_assembly = mounting_holes.union(motor_body).union(boss).union(result_shaft)

# Rotate for better isometric view similar to image
result = final_assembly.rotate((0,0,0), (1,0,0), -90).rotate((0,0,0), (0,0,1), -45)