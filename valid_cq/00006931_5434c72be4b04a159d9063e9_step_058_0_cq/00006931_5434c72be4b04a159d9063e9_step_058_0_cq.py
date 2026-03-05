import cadquery as cq

# Parametric dimensions
height = 100.0   # Length of the tube
outer_diameter = 20.0
wall_thickness = 2.0
inner_diameter = outer_diameter - (2 * wall_thickness)

# Create the hollow cylinder (tube)
# Method: Create a solid cylinder and cut a smaller cylinder from it
# Alternatively, use 2D sketch and extrude

result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(height)
)

# Alternative simpler method specifically for tubes if preferred:
# result = cq.Workplane("XY").circle(outer_diameter/2).extrude(height).faces(">Z").hole(inner_diameter)