import cadquery as cq

# --- Parameter Definitions ---
# Main body dimensions
main_body_width = 30.0
main_body_height = 30.0
main_body_length = 25.0
chamfer_size = 5.0

# Rear face detail (rectangular protrusion)
rear_plate_width = 24.0
rear_plate_height = 24.0
rear_plate_thickness = 2.0
rear_tab_width = 5.0
rear_tab_height = 5.0
rear_tab_thickness = 4.0 # sticks out further than plate
rear_tab_y_offset = -6.0

# Side circular features (hinge/pivot points)
side_boss_radius = 4.0
side_boss_length = main_body_width + 6.0 # Extends slightly past the main width
side_boss_y_pos = -5.0 # Lower down on the body

# Front cylindrical nozzle/lens assembly
front_cylinder_radius_base = 10.0
front_cylinder_radius_mid = 8.0
front_cylinder_radius_tip = 11.0
front_cylinder_length_base = 5.0
front_cylinder_length_mid = 10.0
front_cylinder_length_tip = 5.0
total_cylinder_length = front_cylinder_length_base + front_cylinder_length_mid + front_cylinder_length_tip

# --- Geometry Construction ---

# 1. Main Body Block
# Start with a simple box
main_body = cq.Workplane("XY").box(main_body_width, main_body_height, main_body_length)

# Apply chamfers to the top edges to create the "house" roof shape
# We select edges that are on the top (Z max) and run along the Y axis
main_body = (
    main_body.faces(">Z")
    .edges("|Y")
    .chamfer(chamfer_size)
)

# 2. Side Bosses (The cylindrical protrusions on the sides)
# We orient a cylinder along the X axis at a specific Y and Z offset relative to center
side_bosses = (
    cq.Workplane("YZ")
    .center(0, side_boss_y_pos) # Adjust position (Y axis in local plane corresponds to global Z, X to Y)
    # Wait, Workplane YZ: X_local=Y_global, Y_local=Z_global. 
    # Let's align explicitly.
    .workplane(offset=-side_boss_length/2.0)
    .circle(side_boss_radius)
    .extrude(side_boss_length)
)

# Rotate side bosses to correct orientation if needed, or create directly on faces.
# Easier method: Create cylinder on X axis and translate.
side_boss_solid = cq.Solid.makeCylinder(side_boss_radius, side_boss_length, pnt=cq.Vector(-side_boss_length/2, side_boss_y_pos, -5), dir=cq.Vector(1, 0, 0))
# The image shows these bosses are lower down. Let's adjust Z.
# Let's recreate using the Workplane logic properly.
side_bosses = (
    cq.Workplane("YZ")
    .workplane(offset=-side_boss_length/2)
    .center(side_boss_y_pos, -5) # Move in Y (global Y) and Z (global Z)
    .circle(side_boss_radius)
    .extrude(side_boss_length)
)

# 3. Rear Plate Detail
# Select the rear face (-X direction in this orientation, assuming length is X)
# Actually, let's assume the "Front" is +X. So rear is -X.
# The main body was box(width(X), height(Y), length(Z)). Wait, box arguments are x, y, z.
# Let's standardise: X=Length (axis of nozzle), Y=Width, Z=Height.
# Re-building main body with this orientation preference.

# --- RESTARTING WITH DEFINED ORIENTATION ---
# X axis: Front (+X) to Back (-X)
# Y axis: Left/Right
# Z axis: Up/Down

main_body = cq.Workplane("YZ").box(main_body_width, main_body_height, main_body_length)
# Length is along X (extruded from YZ). Wait, box creates centered at origin.
# Let's use simple box and rotate/chamfer.
main_body = cq.Workplane("XY").box(main_body_length, main_body_width, main_body_height)

# Chamfer top edges (Z max, running along X)
main_body = main_body.faces(">Z").edges("|X").chamfer(chamfer_size)

# Rear Plate (on -X face)
rear_plate = (
    main_body.faces("<X")
    .workplane()
    .rect(rear_plate_width, rear_plate_height)
    .extrude(rear_plate_thickness)
)

# Small tab on rear plate
rear_tab = (
    rear_plate.faces("<X")
    .workplane()
    .center(0, rear_tab_y_offset)
    .rect(rear_tab_width, rear_tab_height)
    .extrude(rear_tab_thickness) # Small additional protrusion
)

# Side Bosses (Along Y axis)
# Located on the lower part of the body
side_bosses = (
    cq.Workplane("XZ")
    .center(0, -5) # Center X (relative to origin), Lower Z
    .workplane(offset=-side_boss_length/2)
    .circle(side_boss_radius)
    .extrude(side_boss_length)
)

# Front Nozzle Assembly (on +X face)
# We build this as a revolution or a stack of cylinders
front_face = main_body.faces(">X").workplane()

# 1. Base ring (widest part touching body, or slightly inset? Image shows step)
# The image shows a base, then a groove/narrow section, then the tip.
# Let's model it as a stack.

# Cylinder 1: Base attached to body
cyl_1 = (
    main_body.faces(">X")
    .workplane()
    .circle(front_cylinder_radius_base)
    .extrude(front_cylinder_length_base)
)

# Cylinder 2: Narrower middle section
cyl_2 = (
    cyl_1.faces(">X")
    .workplane()
    .circle(front_cylinder_radius_mid)
    .extrude(front_cylinder_length_mid)
)

# Cylinder 3: Tip (slightly wider than mid, creating the rim)
cyl_3 = (
    cyl_2.faces(">X")
    .workplane()
    .circle(front_cylinder_radius_tip)
    .extrude(front_cylinder_length_tip)
)

# Combine everything
result = main_body.union(rear_plate).union(rear_tab).union(side_bosses).union(cyl_1).union(cyl_2).union(cyl_3)

# Fillet the transition between the side bosses and the main body slightly if desired,
# but the image looks fairly sharp there. However, the side bosses look like they might 
# be "half" cylinders merged into the side, or full cylinders passing through. 
# The image shows a "bump" on the side. 
# Let's refine the result variable to be cleaner.

result = (
    main_body
    .union(side_bosses)
    .union(rear_plate)
    .union(rear_tab)
    .union(cyl_1)
    .union(cyl_2)
    .union(cyl_3)
)