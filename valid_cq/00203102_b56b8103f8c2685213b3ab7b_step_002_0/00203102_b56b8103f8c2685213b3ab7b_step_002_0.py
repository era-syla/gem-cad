import cadquery as cq

# Parametric dimensions
length = 100.0        # Total length (distance between straight ends)
end_width = 60.0      # Width of the straight edges
waist_width = 30.0    # Narrowest width at the center
thickness = 8.0       # Thickness of the plate

# Half dimensions for coordinate calculations
dx = length / 2.0
dy_outer = end_width / 2.0
dy_inner = waist_width / 2.0

# Create the 3D model
# 1. Start a sketch on the XY plane
# 2. Draw the perimeter using straight lines for ends and three-point arcs for the concave sides
# 3. Extrude to create the solid
result = (
    cq.Workplane("XY")
    .moveTo(dx, -dy_outer)                  # Start at Bottom-Right corner
    .lineTo(dx, dy_outer)                   # Straight line to Top-Right corner
    .threePointArc((0, dy_inner), (-dx, dy_outer))  # Concave arc to Top-Left corner
    .lineTo(-dx, -dy_outer)                 # Straight line to Bottom-Left corner
    .threePointArc((0, -dy_inner), (dx, -dy_outer)) # Concave arc to Bottom-Right corner
    .close()
    .extrude(thickness)
)