import cadquery as cq

# --- Parameters ---
# Dimensions estimated from the image
base_size = 20.0
upright_width = 30.0
upright_height = 90.0
upright_thickness = 4.0
rod_length = 70.0
rod_radius = 1.5
plate_dim = (50.0, 25.0, 1.5)

# --- Right Assembly (Vertical Structure) ---

# 1. Base Block (Grey Cube)
base = (
    cq.Workplane("XY")
    .box(base_size, base_size, base_size)
    .translate((0, 0, base_size / 2))
)

# 2. Vertical Upright with Diagonal Brace (Black Structure)
# Create the main vertical plate
upright_raw = (
    cq.Workplane("XY")
    .box(upright_thickness, upright_width, upright_height)
    .translate((-base_size/2 + upright_thickness/2, 0, base_size + upright_height/2))
)

# Cut pockets to simulate the truss/diagonal bracing
# Cut lower triangle
upright_cut1 = (
    upright_raw.faces(">X").workplane()
    .polyline([
        (-upright_width/2 + 4, -upright_height/2 + 4),
        (upright_width/2 - 4, -upright_height/2 + 4),
        (-upright_width/2 + 4, upright_height/2 - 4)
    ])
    .close()
    .cutThruAll()
)

# Cut upper triangle (leaving a diagonal rib)
upright = (
    upright_cut1.faces(">X").workplane()
    .polyline([
        (upright_width/2 - 4, upright_height/2 - 4),
        (-upright_width/2 + 4, upright_height/2 - 4),
        (upright_width/2 - 4, -upright_height/2 + 4)
    ])
    .close()
    .cutThruAll()
)

# 3. Horizontal Rod
# Extending from the upright towards -X (left in the image)
rod_z_pos = base_size + upright_height * 0.4
rod = (
    cq.Workplane("YZ")
    .workplane(offset=0) # Center plane
    .center(0, rod_z_pos)
    .circle(rod_radius)
    .extrude(-rod_length - base_size/2) # Extrude backwards in X
)

# 4. T-Handle / Crossbar at the end of the rod
handle = (
    cq.Workplane("YZ")
    .workplane(offset=-rod_length - base_size/2)
    .center(0, rod_z_pos)
    .box(2, 20, 2) # Cross bar on the rod tip
)

# Group Right Assembly and position it
right_assembly = base.union(upright).union(rod).union(handle)
right_assembly = right_assembly.translate((100, 0, 0))


# --- Left Assembly (Scattered Plates) ---

# Plate 1
plate1 = (
    cq.Workplane("XY")
    .box(*plate_dim)
    .faces(">Z").workplane().circle(2.0).cutThruAll() # Mounting hole
    .translate((-50, 0, plate_dim[2] / 2))
)

# Plate 2 (Offset position)
plate2 = (
    cq.Workplane("XY")
    .box(*plate_dim)
    .faces(">Z").workplane().circle(2.0).cutThruAll() # Mounting hole
    .translate((-80, 40, plate_dim[2] / 2))
)

# Small floating elements (fasteners/debris shown in image)
screw1 = cq.Workplane("XY").box(3, 3, 3).translate((-45, 10, 5))
screw2 = cq.Workplane("XY").box(3, 3, 3).translate((-75, 50, 5))

# --- Final Result ---
# Combine all disconnected parts into one object for the result
result = right_assembly.union(plate1).union(plate2).union(screw1).union(screw2)