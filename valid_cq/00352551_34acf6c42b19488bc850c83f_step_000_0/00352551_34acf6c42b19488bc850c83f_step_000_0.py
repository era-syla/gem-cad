import cadquery as cq

# -- Parametric Dimensions --
length = 280.0
width = 60.0
thickness = 6.0
corner_radius = 4.0

# Feature Dimensions
hole_diameter = 5.0
hole_spacing_y = 32.0  # Transverse distance between hole pairs

slot_width = 16.0
slot_total_length = 45.0
# CadQuery slot2D uses center-to-center distance
slot_length_c2c = slot_total_length - slot_width

# Feature Positioning
# Coordinate system centered on the plate
# Left end holes
left_margin = 25.0
x_left = -length/2 + left_margin

# Right cluster (Holes -- Slot -- Holes)
# Center of the slot relative to the right edge
right_cluster_margin = 70.0
x_slot_center = length/2 - right_cluster_margin

# Distance from slot center to the flanking hole pairs
cluster_hole_offset_x = 40.0

# -- Geometry Generation --

# 1. Base Plate with Filleted Corners
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Define Hole Locations
hole_points = []

# Far left pair
hole_points.append((x_left, hole_spacing_y/2))
hole_points.append((x_left, -hole_spacing_y/2))

# Right cluster - Left side pair
hole_points.append((x_slot_center - cluster_hole_offset_x, hole_spacing_y/2))
hole_points.append((x_slot_center - cluster_hole_offset_x, -hole_spacing_y/2))

# Right cluster - Right side pair
hole_points.append((x_slot_center + cluster_hole_offset_x, hole_spacing_y/2))
hole_points.append((x_slot_center + cluster_hole_offset_x, -hole_spacing_y/2))

# 3. Cut Circular Holes
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .hole(hole_diameter)
)

# 4. Cut Central Slot
result = (
    result
    .faces(">Z")
    .workplane()
    .center(x_slot_center, 0)
    .slot2D(slot_length_c2c, slot_width)
    .cutThruAll()
)