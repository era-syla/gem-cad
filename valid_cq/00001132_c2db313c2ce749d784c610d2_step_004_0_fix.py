import cadquery as cq

# Parameters
bar_length = 120
bar_width = 4
bar_height = 3

end_radius = 6
end_height = 5
hole_radius = 2.5

fork_width = 3
fork_gap = 2
fork_height = 5
fork_hole_radius = 1.5

spacer_outer_radius = 4
spacer_inner_radius = 2.5
spacer_height = 5

# --- Main connecting rod bar ---
bar = (
    cq.Workplane("XY")
    .box(bar_length, bar_width, bar_height)
)

# --- Left end (round boss with hole) ---
left_end = (
    cq.Workplane("XY")
    .center(-bar_length/2, 0)
    .cylinder(end_height, end_radius)
)

left_hole = (
    cq.Workplane("XY")
    .center(-bar_length/2, 0)
    .cylinder(end_height + 2, hole_radius)
)

left_assembly = left_end.cut(left_hole)

# --- Right end (fork/clevis with two ears) ---
# Right boss base
right_base = (
    cq.Workplane("XY")
    .center(bar_length/2, 0)
    .box(end_radius * 1.5, end_radius * 2, bar_height)
)

# Two fork ears
ear_y_offset = (fork_gap/2 + fork_width/2)

right_ear1 = (
    cq.Workplane("XY")
    .center(bar_length/2 + end_radius * 0.5, ear_y_offset)
    .cylinder(fork_height, fork_width + 1)
)

right_ear1_hole = (
    cq.Workplane("XY")
    .center(bar_length/2 + end_radius * 0.5, ear_y_offset)
    .cylinder(fork_height + 2, fork_hole_radius)
)

right_ear2 = (
    cq.Workplane("XY")
    .center(bar_length/2 + end_radius * 0.5, -ear_y_offset)
    .cylinder(fork_height, fork_width + 1)
)

right_ear2_hole = (
    cq.Workplane("XY")
    .center(bar_length/2 + end_radius * 0.5, -ear_y_offset)
    .cylinder(fork_height + 2, fork_hole_radius)
)

right_assembly = (
    right_base
    .union(right_ear1)
    .union(right_ear2)
    .cut(right_ear1_hole)
    .cut(right_ear2_hole)
)

# --- Combine bar with ends ---
rod = (
    bar
    .union(left_assembly)
    .union(right_assembly)
)

# --- Spacer/bushing (separate small cylinder with hole) ---
spacer = (
    cq.Workplane("XY")
    .center(-bar_length/2 - 25, 0)
    .cylinder(spacer_height, spacer_outer_radius)
)

spacer_hole = (
    cq.Workplane("XY")
    .center(-bar_length/2 - 25, 0)
    .cylinder(spacer_height + 2, spacer_inner_radius)
)

spacer_final = spacer.cut(spacer_hole)

# Combine all parts
result = rod.union(spacer_final)