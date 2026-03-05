import cadquery as cq

# Parameters for the model geometry
plate_width = 120.0
plate_height = 80.0
plate_thickness = 5.0

boss_width = 90.0
boss_height = 50.0
boss_thickness = 15.0
chamfer_size = 10.0

# 1. Create the base rectangular plate
# Centered at the origin on the XY plane
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Create the central rectangular protrusion (boss)
# Select the front face (highest Z), draw a rectangle, and extrude
result = (
    result.faces(">Z")
    .workplane()
    .rect(boss_width, boss_height)
    .extrude(boss_thickness)
)

# 3. Apply the chamfer to the top edge of the protrusion
# We select the edges on the front face (>Z) and filter for the top one (>Y)
result = result.edges(">Z").edges(">Y").chamfer(chamfer_size)