import cadquery as cq

# Parametric dimensions based on the visual aspect ratio
height = 150.0       # Total height of the tube
width = 15.0         # Outer width (shorter side of the profile)
depth = 30.0         # Outer depth (longer side of the profile)
wall_thickness = 2.0 # Thickness of the material

# Create the hollow rectangular tube geometry
# 1. Start on the XY plane
# 2. Draw the outer rectangle
# 3. Draw the inner rectangle (offset by wall thickness) to define the profile wall
# 4. Extrude the profile vertically to the specified height
result = (
    cq.Workplane("XY")
    .rect(width, depth)
    .rect(width - 2 * wall_thickness, depth - 2 * wall_thickness)
    .extrude(height)
)