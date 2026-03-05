import cadquery as cq

# Parameters
shell_outer_od = 20
shell_inner_od = 16
shell_height = 40
slot_width = 4
slot_depth = 8

# Create one shell
base_shell = cq.Workplane("XY").circle(shell_outer_od/2).extrude(shell_height)
inner_cut = cq.Workplane("XY").circle(shell_inner_od/2).extrude(shell_height)
slot_cut = (
    cq.Workplane("XY")
    .rect(slot_width, shell_height, centered=[True, False])
    .extrude(slot_depth)
    .translate((shell_outer_od/2 - slot_depth/2, 0, 0))
)
shell = base_shell.cut(inner_cut).cut(slot_cut)

# Duplicate shells left and right
left_shell = shell.translate((-shell_outer_od * 1.5, 0, 0))
right_shell = shell.translate(( shell_outer_od * 1.5, 0, 0))

# Create assembly: pin head, shaft, hex nut, and bar
pin_head = cq.Workplane("XY").circle(8/2).extrude(2)
pin_shaft = cq.Workplane("XY").circle(3/2).extrude(30).translate((0, 0, 2))
hex_nut = cq.Workplane("XY").polygon(6, 10).extrude(5).translate((0, 0, 32))
bar = cq.Workplane("XY").rect(4, 4).extrude(20).translate((0, 0, 37))

assembly = pin_head.union(pin_shaft).union(hex_nut).union(bar)

# Combine everything
result = left_shell.union(right_shell).union(assembly)