import cadquery as cq

# Dimensions
total_width = 80
total_depth = 70
total_height = 60
wall_thickness = 15
slot_width = 14
hole_radius = 12
hole_center_x = 0  # centered on each lug
hole_height = 38  # height of hole center from base

# Create the base block - trapezoidal profile (wedge shape)
# The back is tall, front slopes down
base = (
    cq.Workplane("XZ")
    .moveTo(-total_width/2, 0)
    .lineTo(total_width/2, 0)
    .lineTo(total_width/2, total_height)
    .lineTo(-total_width/2, total_height)
    .close()
    .extrude(total_depth)
)

# Create the sloped front face by cutting a wedge from the front
# The slope goes from full height at back to lower height at front
slope_cut = (
    cq.Workplane("XZ")
    .moveTo(-total_width/2 - 1, total_height * 0.4)
    .lineTo(total_width/2 + 1, total_height * 0.4)
    .lineTo(total_width/2 + 1, total_height + 1)
    .lineTo(-total_width/2 - 1, total_height + 1)
    .close()
    .extrude(total_depth * 0.55)
)

base = base.cut(slope_cut)

# Create the center slot (gap between the two lugs)
slot = (
    cq.Workplane("XY")
    .moveTo(0, total_depth * 0.3)
    .rect(slot_width, total_depth * 0.8)
    .extrude(total_height + 1)
)

base = base.cut(slot)

# Add arched tops to the lugs
# Cut rectangular corners to make arched profile on each lug
# Left lug arch
arch_center_x_left = -(slot_width/2 + wall_thickness/2)
arch_center_x_right = (slot_width/2 + wall_thickness/2)

lug_half_width = wall_thickness / 2
arch_radius = wall_thickness / 2

# Round the top of each lug using a cylinder cut approach
# Cut away sharp corners at top of each lug to create arch
for x_pos in [arch_center_x_left, arch_center_x_right]:
    # Create arch by cutting a profile
    arch_cut = (
        cq.Workplane("XZ")
        .moveTo(x_pos - lug_half_width - 1, total_height * 0.7)
        .lineTo(x_pos + lug_half_width + 1, total_height * 0.7)
        .lineTo(x_pos + lug_half_width + 1, total_height + 5)
        .lineTo(x_pos - lug_half_width - 1, total_height + 5)
        .close()
        .extrude(total_depth + 2)
        .translate((0, -1, 0))
    )
    
    arch_keep = (
        cq.Workplane("XZ")
        .moveTo(x_pos, total_height * 0.7 + lug_half_width)
        .circle(lug_half_width)
        .extrude(total_depth + 2)
        .translate((0, -1, 0))
    )
    
    arch_cut = arch_cut.cut(arch_keep)
    base = base.cut(arch_cut)

# Drill holes through each lug
for x_pos in [arch_center_x_left, arch_center_x_right]:
    hole = (
        cq.Workplane("XZ")
        .moveTo(x_pos, total_height * 0.7 + lug_half_width)
        .circle(hole_radius)
        .extrude(total_depth + 2)
        .translate((0, -1, 0))
    )
    base = base.cut(hole)

result = base