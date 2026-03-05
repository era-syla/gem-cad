import cadquery as cq

# Main cabinet body
cabinet_width = 200
cabinet_height = 100
cabinet_depth = 40

# Main body
body = cq.Workplane("XY").box(cabinet_width, cabinet_depth, cabinet_height)

# Top cap - slightly wider and deeper, positioned at top
top_cap_height = 8
top_cap = (cq.Workplane("XY")
           .box(cabinet_width + 4, cabinet_depth + 4, top_cap_height)
           .translate((0, 0, (cabinet_height / 2) + (top_cap_height / 2))))

# Mid rail - a horizontal strip across the front, roughly at mid height
rail_height = 6
rail_depth = cabinet_depth + 6
rail_width = cabinet_width + 2
rail_z = 5  # slightly below center

mid_rail = (cq.Workplane("XY")
            .box(rail_width, rail_depth, rail_height)
            .translate((0, 0, rail_z)))

# Combine body with top cap and mid rail
result_solid = body.union(top_cap).union(mid_rail)

# Add vertical dividers on the front face to create panel effect
# 4 vertical dividers creating 5 panels across the width
panel_count = 5
divider_width = 3
divider_depth = 3
divider_height = cabinet_height - top_cap_height - 2

panel_width = cabinet_width / panel_count

for i in range(1, panel_count):
    x_pos = -cabinet_width / 2 + i * panel_width
    divider = (cq.Workplane("XY")
               .box(divider_width, divider_depth, divider_height)
               .translate((x_pos, cabinet_depth / 2 - divider_depth / 2 + 1, 
                          -(top_cap_height / 2))))
    result_solid = result_solid.union(divider)

# Add horizontal divider at mid rail level on front face
h_divider = (cq.Workplane("XY")
             .box(cabinet_width, divider_depth, divider_width)
             .translate((0, cabinet_depth / 2 - divider_depth / 2 + 1, rail_z)))
result_solid = result_solid.union(h_divider)

result = result_solid