import cadquery as cq

# Parametric dimensions
body_diameter = 18.0
body_height = 80.0
terminal_offset = 4.5
terminal_diameter = 3.5
terminal_height = 2.5
fillet_radius = 1.0  # For the rounded terminal

# 1. Create the main cylindrical body
# Aligned along the Z-axis, centered on XY
result = cq.Workplane("XY").circle(body_diameter / 2.0).extrude(body_height)

# 2. Create the flat terminal (Right side)
# We create a new workplane at the top of the body
flat_terminal = (
    cq.Workplane("XY")
    .workplane(offset=body_height)
    .center(terminal_offset, 0)
    .circle(terminal_diameter / 2.0)
    .extrude(terminal_height)
)

# 3. Create the rounded terminal (Left side)
# Modeled as a cylinder with a filleted top edge to match the "nipple" look
rounded_terminal = (
    cq.Workplane("XY")
    .workplane(offset=body_height)
    .center(-terminal_offset, 0)
    .circle(terminal_diameter / 2.0)
    .extrude(terminal_height)
    # Select the top face and fillet its edges
    .faces(">Z").edges().fillet(fillet_radius)
)

# 4. Combine all components into the final result
result = result.union(flat_terminal).union(rounded_terminal)