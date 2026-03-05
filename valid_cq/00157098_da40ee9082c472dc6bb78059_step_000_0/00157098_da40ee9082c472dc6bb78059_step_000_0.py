import cadquery as cq

# -- Parametric Dimensions --
strut_height = 80.0
strut_chord = 40.0
strut_thickness = 12.0
top_angle = 25.0       # Angle of the top surface in degrees
sphere_radius = 10.0

plate_length = 55.0
plate_width = 22.0
plate_thickness = 2.0
recess_offset = 4.0    # Margin for the top recess
recess_depth = 0.5

# -- 1. Create the Main Vertical Strut --
# We start with a symmetric airfoil-like profile (ellipse) extruded vertically
# We extrude extra length to ensure we can cut it cleanly at an angle later
strut_raw = (
    cq.Workplane("XY")
    .ellipse(strut_chord / 2.0, strut_thickness / 2.0)
    .extrude(strut_height + 20)
)

# Define a cutting plane for the angled top
# The plane originates at the desired height and is rotated around the Y-axis
cutting_plane = (
    cq.Workplane("XY")
    .workplane(offset=strut_height)
    .transformed(rotate=(0, -top_angle, 0))
)

# Create a large block oriented to the cutting plane to remove material "above" it
cutter = cutting_plane.rect(200, 200).extrude(50)

# Cut the raw strut
strut = strut_raw.cut(cutter)

# -- 2. Create the Top Plate --
# We select the newly created angled face at the top of the strut
top_face = strut.faces(">Z").val()
plate_workplane = cq.Workplane(obj=top_face)

# Create the main plate solid
plate = (
    plate_workplane
    .ellipse(plate_length / 2.0, plate_width / 2.0)
    .extrude(plate_thickness)
)

# Create the recess detail on top of the plate
plate_top = plate.faces(">Z").workplane()
plate_with_recess = (
    plate_top
    .ellipse((plate_length / 2.0) - recess_offset, (plate_width / 2.0) - recess_offset)
    .cutBlind(-recess_depth)
)

# -- 3. Create the Side Sphere --
# Positioned halfway up the strut and slightly embedded in the side face
sphere_center_z = strut_height / 2.0
sphere_center_y = strut_thickness / 2.0  # Align with surface
sphere_center_x = 5.0  # Slight horizontal offset

sphere = (
    cq.Workplane("XY")
    .workplane(offset=sphere_center_z)
    .center(sphere_center_x, sphere_center_y)
    .sphere(sphere_radius)
)

# -- 4. Create the Detached Bottom Plate --
# A similar elliptical shape lying on the ground plane nearby
floor_plate = (
    cq.Workplane("XY")
    .center(strut_chord * 1.2, strut_thickness * 3)
    .ellipse(plate_length / 2.0, plate_width / 2.0)
    .extrude(1.0)
)

# -- 5. Combine and Finalize --
# Union the connected parts (Strut + Top Plate + Sphere)
main_assembly = strut.union(plate_with_recess).union(sphere)

# Add the detached floor plate to the result (creates a multi-solid compound)
result = main_assembly.add(floor_plate)

# If running in an environment that auto-displays 'result' (like CQ-Editor), this is sufficient.