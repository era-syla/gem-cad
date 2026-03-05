import cadquery as cq

# Base plate
base = (
    cq.Workplane("XY")
    .rect(60, 60)
    .extrude(8)
)

# Round corners of base
base = base.edges("|Z").fillet(6)

# Center post / column rising from base
post = (
    cq.Workplane("XY")
    .rect(16, 16)
    .extrude(30)
)

# Main body - a larger block on top of base center
main_block = (
    cq.Workplane("XY")
    .workplane(offset=8)
    .rect(40, 20)
    .extrude(20)
)

# Left upright arm
left_arm = (
    cq.Workplane("XY")
    .workplane(offset=8)
    .center(-14, 0)
    .rect(12, 20)
    .extrude(30)
)

# Right upright arm
right_arm = (
    cq.Workplane("XY")
    .workplane(offset=8)
    .center(14, 0)
    .rect(12, 20)
    .extrude(30)
)

# Top horizontal bar connecting left and right arms
top_bar = (
    cq.Workplane("XY")
    .workplane(offset=30)
    .rect(40, 20)
    .extrude(8)
)

# Combine main structure
structure = base.union(main_block).union(left_arm).union(right_arm).union(top_bar)

# Cut arch through left arm (arch opening)
left_arch_cut = (
    cq.Workplane("XZ")
    .workplane(offset=10)
    .center(-14, 20)
    .rect(8, 16)
    .extrude(6)
)

# Actually, let's cut rectangular openings through the arms
# Cut through left upright (front-back direction)
left_cut = (
    cq.Workplane("YZ")
    .workplane(offset=-20)
    .center(0, 22)
    .rect(12, 12)
    .extrude(40)
)

# Cut through right upright
right_cut = (
    cq.Workplane("YZ")
    .workplane(offset=-20)
    .center(0, 22)
    .rect(12, 12)
    .extrude(40)
)

# Cut arch in top bar - left side
top_left_cut = (
    cq.Workplane("XY")
    .workplane(offset=30)
    .center(-14, 0)
    .rect(8, 20)
    .extrude(8)
)

# Cut arch in top bar - center opening
top_center_cut = (
    cq.Workplane("XY")
    .workplane(offset=32)
    .center(0, 0)
    .rect(8, 20)
    .extrude(6)
)

# Cut a slot through the main body (horizontal channel)
h_channel = (
    cq.Workplane("XY")
    .workplane(offset=14)
    .rect(40, 8)
    .extrude(6)
)

# Cut vertical slot through base
v_slot = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .rect(8, 30)
    .extrude(8)
)

# Cut circular arch on right side of main block
right_arch = (
    cq.Workplane("YZ")
    .workplane(offset=20)
    .center(4, 14)
    .circle(7)
    .extrude(15)
)

# Cut slot in base (recess)
base_recess = (
    cq.Workplane("XY")
    .rect(30, 10)
    .extrude(4)
)

# Build the final result step by step
result = structure

# Cut horizontal channel through middle
result = result.cut(
    cq.Workplane("XY").workplane(offset=14).rect(50, 8).extrude(6)
)

# Cut left arch opening
result = result.cut(
    cq.Workplane("XZ").workplane(offset=10).center(-14, 22).rect(8, 10).extrude(6)
)

# Cut right arch/circle opening  
result = result.cut(
    cq.Workplane("YZ").workplane(offset=14).center(4, 14).circle(6).extrude(12)
)

# Cut top arch opening
result = result.cut(
    cq.Workplane("XZ").workplane(offset=10).center(0, 22).rect(8, 10).extrude(5)
)

# Cut base slot
result = result.cut(
    cq.Workplane("XY").center(-10, -5).rect(10, 20).extrude(4)
)

# Cut small square recess in base
result = result.cut(
    cq.Workplane("XY").center(-8, -8).rect(8, 8).extrude(4)
)