import cadquery as cq

# --- Parameters ---
# Overall dimensions
length = 180.0
width = 32.0
thickness = 2.5

# Central Ribs parameters
rib_width = 4.0
rib_length = 20.0
rib_height = 6.0
rib_spacing = 14.0  # Gap between the two ribs
rib_y_shift = 3.0   # Shift ribs towards the back edge slightly

# Notch parameters
notch_back_width = 6.0
notch_back_depth = 5.0
notch_front_width = 40.0 # Wide shallow cutout on the front
notch_front_depth = 3.0

# Hole parameters
hole_dist_from_end = 8.0
hole_spacing = 12.0
dia_mount = 3.5
dia_cbore = 6.0
depth_cbore = 0.6
dia_pin = 2.5

# --- Geometry Construction ---

# 1. Base Plate
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Cut Back Notches
# Located on the +Y edge, flanking the central rib area
notch_x_pos = (rib_spacing / 2.0) + rib_width + (notch_back_width / 2.0) - 1.0
result = (
    result.faces(">Z").workplane()
    .pushPoints([(notch_x_pos, width/2.0), (-notch_x_pos, width/2.0)])
    .rect(notch_back_width, notch_back_depth * 2.0)
    .cutThruAll()
)

# 3. Cut Front Relief Notch
# Located on the -Y edge, centered
result = (
    result.faces(">Z").workplane()
    .pushPoints([(0, -width/2.0)])
    .rect(notch_front_width, notch_front_depth * 2.0)
    .cutThruAll()
)

# 4. Add Central Ribs
# Create the ribs as separate solids and union them
# Ribs are shifted slightly to the back (+Y) to match the visual alignment with back notches
rib_x_pos = (rib_spacing + rib_width) / 2.0
rib_center_y = rib_y_shift

ribs = (
    cq.Workplane("XY")
    .workplane(offset=thickness/2.0)
    .pushPoints([(rib_x_pos, rib_center_y), (-rib_x_pos, rib_center_y)])
    .rect(rib_width, rib_length)
    .extrude(rib_height)
)

result = result.union(ribs)

# 5. Add Mounting Holes
# Left and Right ends have a similar pattern: 
# Outer hole is counterbored/embossed, Inner hole is a simple hole
pts_outer = [
    (-length/2.0 + hole_dist_from_end, 0), 
    (length/2.0 - hole_dist_from_end, 0)
]
pts_inner = [
    (-length/2.0 + hole_dist_from_end + hole_spacing, 0), 
    (length/2.0 - hole_dist_from_end - hole_spacing, 0)
]

result = (
    result.faces(">Z").workplane()
    .pushPoints(pts_outer)
    .cboreHole(dia_mount, dia_cbore, depth_cbore)
    .pushPoints(pts_inner)
    .hole(dia_pin)
)

# Final Result is stored in 'result'