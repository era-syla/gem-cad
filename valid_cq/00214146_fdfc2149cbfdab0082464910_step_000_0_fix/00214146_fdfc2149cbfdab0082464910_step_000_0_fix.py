import cadquery as cq

# Parameters
base_thickness_y = 15  # width in Y direction
wall_height_z = 45     # total height of vertical wall above base
slot_depth_z = 10      # how far the slot cuts down from the top
wall_thickness_y = 4   # thickness of each side wall in Y
slot_width_y = base_thickness_y - 2 * wall_thickness_y

# Base + sloped arm profile in X-Z plane
pts_base = [
    (0, 0),
    (60, 0),
    (65, 5),
    (0, 5)
]

# Vertical wall + top overhang profile in X-Z plane
pts_vert = [
    (65, 5),
    (65, wall_height_z),
    (70, wall_height_z),
    (70, 10)
]

# Build base and arm
base = (
    cq.Workplane("XZ")
    .polyline(pts_base)
    .close()
    .extrude(base_thickness_y)
)

# Build vertical wall
vert = (
    cq.Workplane("XZ")
    .polyline(pts_vert)
    .close()
    .extrude(base_thickness_y)
)

# Combine parts
result = base.union(vert)

# Create slot cut as a rectangular prism
slot_length_x = 5
slot_center_x = 65 + slot_length_x / 2
slot_center_z = wall_height_z - slot_depth_z / 2
slot_center_y = base_thickness_y / 2

slot_cut = (
    cq.Workplane("XZ")
    .box(slot_length_x, slot_depth_z, slot_width_y)
    .translate((slot_center_x, slot_center_y, slot_center_z))
)

# Subtract slot from the combined shape
result = result.cut(slot_cut)