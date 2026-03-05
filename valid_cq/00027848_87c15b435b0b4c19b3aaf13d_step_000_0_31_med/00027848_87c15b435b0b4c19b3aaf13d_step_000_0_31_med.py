import cadquery as cq

# Parameters
handle_length = 150.0
handle_width = 20.0
handle_thickness = 4.0

main_body_length = 100.0
main_body_width = 30.0
main_body_thickness = 10.0

pivot_radius = 12.0
pivot_height = 15.0

bolt_radius = 4.0
bolt_head_radius = 7.0
bolt_head_height = 4.0

block_width = 15.0
block_length = 20.0
block_height = 12.0

flange_width = 40.0
flange_length = 15.0
flange_thickness = 5.0

# 1. Handle
handle = (
    cq.Workplane("XY")
    .box(handle_length, handle_width, handle_thickness)
    .edges("|Z")
    .fillet(2.0)
)

# 2. Main Body (attached to handle)
main_body = (
    cq.Workplane("XY")
    .transformed(offset=(handle_length / 2 + main_body_length / 2, 0, 0))
    .box(main_body_length, main_body_width, main_body_thickness)
)

# 3. Pivot Cylinder
pivot = (
    cq.Workplane("XY")
    .transformed(offset=(handle_length / 2 + main_body_length - pivot_radius, 0, main_body_thickness / 2))
    .circle(pivot_radius)
    .extrude(pivot_height)
)

# 4. Top Block (sliding mechanism part)
top_block = (
    cq.Workplane("XY")
    .transformed(offset=(handle_length / 2 + main_body_length, 0, main_body_thickness / 2 + pivot_height))
    .box(block_length, block_width, block_height)
)

# 5. Side Flange with holes
flange = (
    cq.Workplane("XY")
    .transformed(offset=(handle_length / 2 + 20, handle_width / 2 + flange_width / 2, 0))
    .box(flange_length, flange_width, flange_thickness)
)

# 6. Bolt/Fastener
bolt = (
    cq.Workplane("XY")
    .transformed(offset=(handle_length / 2 + main_body_length / 2, -main_body_width / 2 - bolt_head_radius, 0))
    .polygon(6, bolt_head_radius)
    .extrude(bolt_head_height)
    .faces(">Z")
    .workplane()
    .circle(bolt_radius)
    .extrude(10.0)
)

# Combine all parts
result = (
    handle
    .union(main_body)
    .union(pivot)
    .union(top_block)
    .union(flange)
    .union(bolt)
)
