import cadquery as cq

# Main vertical column/upright structure
# Dimensions based on image analysis - tall narrow column with flanges

height = 200
width = 40
depth = 15
flange_width = 50
flange_depth = 8
wall_thickness = 4

# Create the main I-beam/column profile
# Web (vertical center plate)
web = (
    cq.Workplane("XY")
    .rect(width, depth)
    .extrude(height)
)

# Front flange
front_flange = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, (depth + flange_depth) / 2, 0))
    .rect(flange_width, flange_depth)
    .extrude(height)
)

# Back flange
back_flange = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, -(depth + flange_depth) / 2, 0))
    .rect(flange_width, flange_depth)
    .extrude(height)
)

# Combine into column
column = web.union(front_flange).union(back_flange)

# Add top cap plate
top_cap = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0, height))
    .rect(flange_width, depth + 2 * flange_depth + 2)
    .extrude(8)
)

# Add bottom cap plate
bottom_cap = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0, -8))
    .rect(flange_width, depth + 2 * flange_depth + 2)
    .extrude(8)
)

column = column.union(top_cap).union(bottom_cap)

# Cut diagonal braces/openings in the web
# Upper diagonal cutout
diag_cut1 = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(0, 0, 0))
    .workplane(offset=-(depth + 2) / 2)
    .moveTo(-width / 2 + wall_thickness, height * 0.55)
    .lineTo(width / 2 - wall_thickness, height * 0.85)
    .lineTo(width / 2 - wall_thickness, height * 0.55 + wall_thickness * 2)
    .lineTo(-width / 2 + wall_thickness, height * 0.25 + wall_thickness * 2)
    .close()
    .extrude(depth + 4)
)

# Lower diagonal cutout
diag_cut2 = (
    cq.Workplane("XZ")
    .workplane(offset=-(depth + 2) / 2)
    .moveTo(-width / 2 + wall_thickness, height * 0.15)
    .lineTo(width / 2 - wall_thickness, height * 0.45)
    .lineTo(width / 2 - wall_thickness, height * 0.15 + wall_thickness * 2)
    .lineTo(-width / 2 + wall_thickness, height * 0.08)
    .close()
    .extrude(depth + 4)
)

# Middle horizontal shelf
shelf = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0, height * 0.5))
    .rect(width, depth + 2)
    .extrude(wall_thickness)
)

column = column.union(shelf)
column = column.cut(diag_cut1).cut(diag_cut2)

# Add bolt holes on flanges
# Top area holes on front flange
hole_positions_top = [(10, height + 4), (-10, height + 4), (0, height + 4)]
for x_pos, z_pos in [(-12, height + 5), (12, height + 5)]:
    hole = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(x_pos, (depth + flange_depth) / 2, z_pos))
        .circle(1.5)
        .extrude(10)
    )
    column = column.cut(hole)

# Bottom area holes on front flange
for x_pos in [-12, 12]:
    hole = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(x_pos, (depth + flange_depth) / 2, -5))
        .circle(1.5)
        .extrude(10)
    )
    column = column.cut(hole)

# Side holes on back flange
for z_offset in [height * 0.25, height * 0.5, height * 0.75]:
    hole = (
        cq.Workplane("XZ")
        .transformed(offset=cq.Vector(flange_width / 2 - 3, z_offset, 0))
        .workplane(offset=-(depth + 2 * flange_depth + 4) / 2)
        .circle(1.5)
        .extrude(flange_depth + 2)
    )
    column = column.cut(hole)

result = column