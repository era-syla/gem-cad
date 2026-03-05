import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
disk_diameter = 100.0
disk_thickness = 15.0

# Central Hub/Boss dimensions
boss_diameter = 25.0
boss_height_extra = 2.0  # Height above the disk surface
center_bore_diameter = 12.0
counterbore_diameter = 18.0
counterbore_depth = 5.0

# Bolt Hole Pattern Dimensions
# It appears there are two concentric circles of holes.
# Outer circle: 8 holes
outer_bolt_circle_diameter = 75.0
outer_hole_diameter = 6.0
num_outer_holes = 8

# Inner circle: 8 holes (offset/staggered relative to outer holes)
inner_bolt_circle_diameter = 45.0
inner_hole_diameter = 6.0
num_inner_holes = 8

# --- Modeling ---

# 1. Create the main disk
# We start by drawing a circle on the XY plane and extruding it.
main_disk = (
    cq.Workplane("XY")
    .circle(disk_diameter / 2.0)
    .extrude(disk_thickness)
)

# 2. Create the central hub/boss
# This sits on top of the main disk.
hub = (
    main_disk.faces(">Z")
    .workplane()
    .circle(boss_diameter / 2.0)
    .extrude(boss_height_extra)
)

# 3. Create the central through-hole and counterbore
# Cut the through hole first
part_with_center_hole = (
    hub.faces(">Z")
    .workplane()
    .hole(center_bore_diameter)  # Cuts through everything
)

# Cut the counterbore
# Since the simple .hole() cuts through, let's target the top face for a blind cut
result_central = (
    part_with_center_hole.faces(">Z")
    .workplane()
    .cboreHole(center_bore_diameter, counterbore_diameter, counterbore_depth)
)

# Note: The cboreHole effectively re-cuts the center hole, but ensures the counterbore geometry is correct.
# Alternatively, one could use simple cut operations.

# 4. Create the outer ring of holes
# These are spaced evenly around the outer bolt circle diameter.
result_with_outer_holes = (
    result_central.faces(">Z")
    .workplane()  # Workplane is now on top of the hub, need to be careful with depths or reference the disk face
)

# To make it cleaner, let's reference the main disk face for the pattern holes, 
# although referencing the hub top works if the cut depth is sufficient.
# Let's reference the main disk top face (Z = disk_thickness)
result_with_outer_holes = (
    result_central.faces(">Z").workplane(offset=-boss_height_extra) 
    .polarArray(outer_bolt_circle_diameter / 2.0, 0, 360, num_outer_holes)
    .circle(outer_hole_diameter / 2.0)
    .cutBlind(-disk_thickness)
)

# 5. Create the inner ring of holes
# These appear to be staggered (rotated) relative to the outer holes.
# 360 / 8 holes = 45 degrees per hole. The offset looks like half that pitch = 22.5 degrees.
result = (
    result_with_outer_holes.faces(">Z").workplane(offset=-boss_height_extra)
    .polarArray(inner_bolt_circle_diameter / 2.0, 22.5, 360, num_inner_holes)
    .circle(inner_hole_diameter / 2.0)
    .cutBlind(-disk_thickness)
)