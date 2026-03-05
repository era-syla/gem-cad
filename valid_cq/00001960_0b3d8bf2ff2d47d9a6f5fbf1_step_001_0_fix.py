import cadquery as cq

# Connecting rod (biela) - simplified but recognizable model
# Main components: small end (top), rod/shank, big end (bottom ring)

# Dimensions (mm)
small_end_od = 14
small_end_id = 7
small_end_thickness = 16

big_end_od = 40
big_end_id = 28
big_end_thickness = 20

rod_width = 12
rod_height = 8
rod_length = 70

# Overall connecting rod length (center to center)
center_distance = 80

# Build the big end ring (bottom)
big_end = (
    cq.Workplane("XY")
    .circle(big_end_od / 2)
    .extrude(big_end_thickness)
)

big_end = (
    big_end
    .faces(">Z")
    .workplane()
    .circle(big_end_id / 2)
    .cutThruAll()
)

# Build the small end (top)
small_end = (
    cq.Workplane("XY")
    .workplane(offset=center_distance)
    .circle(small_end_od / 2)
    .extrude(small_end_thickness)
)

small_end = (
    small_end
    .faces(">Z")
    .workplane()
    .circle(small_end_id / 2)
    .cutThruAll()
)

# Build the connecting rod shank
shank = (
    cq.Workplane("XY")
    .workplane(offset=big_end_thickness / 2 - rod_height / 2)
    .rect(rod_width, rod_length)
    .extrude(rod_height)
)

# Position shank: centered horizontally, connecting big end to small end
# The shank goes from center of big end to center of small end
shank = (
    cq.Workplane("XZ")
    .workplane(offset=big_end_thickness / 2)
    .center(0, center_distance / 2)
    .rect(rod_width, rod_length)
    .extrude(rod_height)
)

# Rebuild more carefully using union
# Big end centered at Z=0, thickness along Z
big_end_solid = (
    cq.Workplane("XY")
    .circle(big_end_od / 2)
    .extrude(big_end_thickness)
)

# Small end centered at Z = center_distance
small_end_solid = (
    cq.Workplane("XY")
    .workplane(offset=center_distance)
    .circle(small_end_od / 2)
    .extrude(small_end_thickness)
)

# Shank connecting them - along Z axis
shank_solid = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .rect(rod_width, rod_width)
    .extrude(center_distance + small_end_thickness)
)

# Add bosses on each side of big end for bolts
boss_r = 5
boss_h = 4

boss_left = (
    cq.Workplane("XY")
    .workplane(offset=big_end_thickness)
    .center(-big_end_od / 2 - 2, 0)
    .circle(boss_r)
    .extrude(boss_h)
)

boss_right = (
    cq.Workplane("XY")
    .workplane(offset=big_end_thickness)
    .center(big_end_od / 2 + 2, 0)
    .circle(boss_r)
    .extrude(boss_h)
)

# Combine all parts
result = (
    big_end_solid
    .union(small_end_solid)
    .union(shank_solid)
)

# Cut the holes
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(small_end_id / 2)
    .cutThruAll()
)

# Cut big end hole
result = (
    result
    .workplane(offset=0)
    .moveTo(0, 0)
    .circle(big_end_id / 2)
    .cutBlind(-big_end_thickness - 1)
)

# Add connecting flanges/ribs on sides of shank near big end
rib_left = (
    cq.Workplane("XY")
    .workplane(offset=big_end_thickness / 2 - 3)
    .center(-rod_width / 2 - 6, center_distance / 3)
    .rect(8, center_distance * 0.5)
    .extrude(6)
)

rib_right = (
    cq.Workplane("XY")
    .workplane(offset=big_end_thickness / 2 - 3)
    .center(rod_width / 2 + 6, center_distance / 3)
    .rect(8, center_distance * 0.5)
    .extrude(6)
)

result = result.union(rib_left).union(rib_right)

# Final cleanup - ensure valid solid
result = result.clean()