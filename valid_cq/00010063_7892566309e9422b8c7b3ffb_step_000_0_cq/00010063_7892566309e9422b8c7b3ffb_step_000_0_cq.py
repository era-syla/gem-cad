import cadquery as cq

# --- Parameter Definitions ---
# Main body dimensions
main_cyl_radius = 8.0
main_cyl_height = 25.0
hinge_offset = 12.0

# Flange/Eyelet dimensions
flange_width = 8.0
flange_height = 20.0
flange_thickness = 6.0
eyelet_radius = 5.0
eyelet_hole_radius = 3.0

# Top dome section
dome_radius = 8.0
dome_cyl_height = 15.0

# Side Hinge dimensions
side_hinge_radius = 6.0
side_hinge_height = 18.0

# Pin dimensions (separate part on the left)
pin_head_radius = 6.0
pin_head_height = 5.0
pin_shaft_radius = 1.5
pin_shaft_length = 15.0
pin_inner_recess_radius = 4.0
pin_inner_recess_depth = 2.0

# --- Geometry Construction ---

# 1. Main Central Body (Vertical Cylinder)
# This forms the core vertical axis
main_body = (
    cq.Workplane("XY")
    .circle(main_cyl_radius)
    .extrude(main_cyl_height)
)

# 2. Add bottom eyelet to main body
# We create a shape on the bottom side looking sideways
main_bottom_eyelet = (
    cq.Workplane("XZ")
    .center(0, eyelet_radius) # Lift slightly so bottom isn't at 0
    .circle(eyelet_radius)
    .extrude(flange_thickness, both=True)
)
# Cut hole through eyelet
main_bottom_hole = (
    cq.Workplane("XZ")
    .center(0, eyelet_radius)
    .circle(eyelet_hole_radius)
    .extrude(flange_thickness * 1.5, both=True)
)
main_bottom_eyelet = main_bottom_eyelet.cut(main_bottom_hole)

# Move the main body up so the eyelet hangs below
main_body = main_body.translate((0, 0, eyelet_radius * 2))
# Attach the bottom eyelet
main_body = main_body.union(main_bottom_eyelet.translate((0, 0, eyelet_radius)))


# 3. Top Domed Section (Swivel Head)
# This is the capsule-like shape on the top right
dome_part = (
    cq.Workplane("XY")
    .circle(dome_radius)
    .extrude(dome_cyl_height)
)
# Create the spherical cap
sphere_cap = (
    cq.Workplane("XY")
    .sphere(dome_radius)
    .cut(cq.Workplane("XY").rect(dome_radius*3, dome_radius*3).extrude(-dome_radius*2)) # Cut bottom half
    .translate((0, 0, dome_cyl_height))
)
dome_part = dome_part.union(sphere_cap)

# Create the cutout/clevis for the hinge on the dome part
clevis_gap = 6.0
clevis_cut = (
    cq.Workplane("YZ")
    .center(0, 0)
    .rect(clevis_gap, dome_cyl_height * 1.5)
    .extrude(dome_radius * 2.5) # Cut through sideways
    .translate((-dome_radius, 0, dome_cyl_height/2))
)
dome_part = dome_part.cut(clevis_cut)

# Add Pin holes to the dome clevis
dome_pin_hole = (
    cq.Workplane("XZ")
    .center(0, dome_cyl_height/2)
    .circle(2.0)
    .extrude(dome_radius * 3, both=True)
)
dome_part = dome_part.cut(dome_pin_hole)

# Position the dome relative to the main body (offset to the right/front)
dome_offset_x = 0
dome_offset_y = 12.0
dome_offset_z = main_cyl_height + eyelet_radius * 2 - 5.0 # Slight overlap
dome_part = dome_part.translate((dome_offset_x, dome_offset_y, dome_offset_z))


# 4. Side Structure (The double eyelet part on the left)
side_mount = (
    cq.Workplane("XY")
    .circle(side_hinge_radius)
    .extrude(side_hinge_height)
)

# Top Eyelet on side mount
top_eyelet = (
    cq.Workplane("YZ")
    .circle(eyelet_radius)
    .extrude(flange_thickness, both=True)
    .translate((0, 0, side_hinge_height + eyelet_radius))
)
top_eyelet_hole = (
    cq.Workplane("YZ")
    .circle(eyelet_hole_radius)
    .extrude(flange_thickness * 1.5, both=True)
    .translate((0, 0, side_hinge_height + eyelet_radius))
)
top_eyelet = top_eyelet.cut(top_eyelet_hole)

# Bottom Eyelet on side mount
btm_eyelet = (
    cq.Workplane("YZ")
    .circle(eyelet_radius)
    .extrude(flange_thickness, both=True)
    .translate((0, 0, -eyelet_radius))
)
btm_eyelet_hole = (
    cq.Workplane("YZ")
    .circle(eyelet_hole_radius)
    .extrude(flange_thickness * 1.5, both=True)
    .translate((0, 0, -eyelet_radius))
)
btm_eyelet = btm_eyelet.cut(btm_eyelet_hole)

side_assembly = side_mount.union(top_eyelet).union(btm_eyelet)

# Position Side Assembly relative to Main Body
side_offset_x = -14.0
side_offset_z = 10.0
side_assembly = side_assembly.translate((side_offset_x, 0, side_offset_z))

# 5. Connecting Block/Bridge
# Connects the main vertical body and the side assembly
bridge = (
    cq.Workplane("XY")
    .rect(abs(side_offset_x), 8.0) # Width spans the gap
    .extrude(15.0)
    .translate((side_offset_x/2, 0, side_offset_z + 2.0))
)

# 6. Separate Pin Component (Left side of image)
pin_head = (
    cq.Workplane("YZ")
    .circle(pin_head_radius)
    .extrude(pin_head_height)
)
# Recess in the head
pin_recess = (
    cq.Workplane("YZ")
    .circle(pin_inner_recess_radius)
    .extrude(pin_inner_recess_depth)
    .translate((pin_head_height - pin_inner_recess_depth, 0, 0)) # Push to front face
)
# Center hole in pin head
pin_thru_hole = (
    cq.Workplane("YZ")
    .circle(pin_shaft_radius)
    .extrude(pin_head_height * 2, both=True)
)

pin_head_final = pin_head.cut(pin_recess).cut(pin_thru_hole)

# The shaft extending from the side
pin_shaft = (
    cq.Workplane("XY") # Perpendicular to the head face
    .circle(pin_shaft_radius)
    .extrude(pin_shaft_length)
    .rotate((0,0,0), (0,1,0), -90) # Orient correctly
    .translate((-pin_shaft_length/2, 0, 0)) # Position relative to head center
    .translate((0, 0, pin_head_radius - 1.0)) # Offset to tangent like image
)

pin_assembly = pin_head_final.union(pin_shaft)
# Move pin assembly away from main assembly
pin_assembly = pin_assembly.translate((-40, 0, 10))


# --- Combine Final Assembly ---
main_assembly = main_body.union(dome_part).union(side_assembly).union(bridge)

# Add fillets to smooth transitions (optional but makes it look realistic)
try:
    main_assembly = main_assembly.edges("|Z").fillet(1.0)
except:
    pass # Fillets can fail on complex unions

# Combine the main assembly and the separate pin
result = main_assembly.union(pin_assembly)