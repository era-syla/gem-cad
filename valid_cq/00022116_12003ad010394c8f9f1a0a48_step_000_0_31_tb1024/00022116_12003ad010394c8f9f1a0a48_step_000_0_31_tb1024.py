import cadquery as cq

# Parameters
panel_w = 180
panel_h = 120
panel_t = 3

bracket_l = 10
bracket_w = 6
bracket_h = 8
rod_r = 1.5

# Create the main rectangular panel
panel = cq.Workplane("XY").box(panel_w, panel_t, panel_h)
# Move panel so its left edge is aligned with the origin (X=0)
panel = panel.translate((panel_w / 2, 0, 0))

# Create the hinge bracket base shape
box = cq.Workplane("XY").center(-bracket_l / 2, 0).box(bracket_l, bracket_w, bracket_h)
cyl = cq.Workplane("XY").center(-bracket_l, 0).cylinder(bracket_h, bracket_w / 2)
bracket = box.union(cyl)

# Position the top and bottom brackets
top_bracket = bracket.translate((0, 0, panel_h / 2 - bracket_h / 2))
bottom_bracket = bracket.translate((0, 0, -panel_h / 2 + bracket_h / 2))

# Create the connecting hinge rod
rod = cq.Workplane("XY").center(-bracket_l, 0).cylinder(panel_h, rod_r)

# Combine all components into the final geometry
result = panel.union(top_bracket).union(bottom_bracket).union(rod)