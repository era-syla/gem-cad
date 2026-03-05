import cadquery as cq

# --- Parameters ---
# Hull Dimensions
hull_length = 320.0
hull_width = 150.0
hull_depth_center = 45.0
hull_depth_ends = 18.0
hull_flat_length = 120.0
wall_thickness = 3.0

# Mount Base Dimensions
base_length = 85.0
base_width = 45.0
base_height = 4.0

# Mount Body Dimensions
body_length = 65.0
body_width = 28.0
body_height = 20.0
chamfer_size = 6.0
pocket_length = 42.0
pocket_width = 12.0
pocket_depth = 12.0
slot_length = 28.0
slot_width = 4.0

# --- Modeling ---

# 1. Create the Hull
# Define points for the side profile (XZ plane)
# The profile creates the variable depth: shallow ends, deep flat center.
pts = [
    (hull_length / 2.0, 0),                        # Top Right
    (hull_length / 2.0, -hull_depth_ends),         # Bottom Right End
    (hull_flat_length / 2.0, -hull_depth_center),  # Bottom Flat Start Right
    (-hull_flat_length / 2.0, -hull_depth_center), # Bottom Flat Start Left
    (-hull_length / 2.0, -hull_depth_ends),        # Bottom Left End
    (-hull_length / 2.0, 0)                        # Top Left
]

# Extrude the profile to create the solid block
hull_solid = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(hull_width / 2.0, both=True)
)

# Shell the solid to create the tray shape with walls
# Selecting the top face (+Z) to be open
hull = hull_solid.faces("+Z").shell(-wall_thickness)


# 2. Create the Center Mount
# Calculate the Z-coordinate of the inner floor
floor_z = -hull_depth_center + wall_thickness

# Create the Base Plate
mount_base = (
    cq.Workplane("XY")
    .workplane(offset=floor_z)
    .rect(base_length, base_width)
    .extrude(base_height)
)

# Add mounting notches to the base (4 corners)
notch_offset_x = base_length / 2.0
notch_offset_y = base_width / 4.0
mount_base = (
    mount_base.faces(">Z").workplane()
    .pushPoints([
        (notch_offset_x, notch_offset_y),
        (notch_offset_x, -notch_offset_y),
        (-notch_offset_x, notch_offset_y),
        (-notch_offset_x, -notch_offset_y)
    ])
    .rect(5, 8)
    .cutThruAll()
)

# Create the Main Body Block on top of the base
mount_body = (
    mount_base.faces(">Z").workplane()
    .rect(body_length, body_width)
    .extrude(body_height)
)

# Add Chamfers to the top longitudinal edges to give it the sloped profile
mount_body = (
    mount_body.faces(">Z").edges("|X")
    .chamfer(chamfer_size)
)

# Cut the Top Pocket
mount_body = (
    mount_body.faces(">Z").workplane()
    .rect(pocket_length, pocket_width)
    .cutBlind(-pocket_depth)
)

# Add detailing holes on the end faces (+X and -X)
for face_dir in [">X", "<X"]:
    mount_body = (
        mount_body.faces(face_dir).workplane()
        .pushPoints([(0, -2), (4, 3), (-4, 3)])
        .circle(1.2)
        .cutBlind(-5)
    )

# 3. Assembly and Final Features
# Combine Hull and Mount structures
assembly = hull.union(mount_base).union(mount_body)

# Cut the central slot through the entire assembly (Mount + Hull Floor)
slot_cutter = (
    cq.Workplane("XY")
    .workplane(offset=floor_z + base_height + body_height + 10)
    .rect(slot_length, slot_width)
    .extrude(-100)  # Extrude downwards deep enough to cut through everything
)

result = assembly.cut(slot_cutter)