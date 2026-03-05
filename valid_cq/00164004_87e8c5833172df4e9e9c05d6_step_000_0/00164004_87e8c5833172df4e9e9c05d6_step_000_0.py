import cadquery as cq

# Dimensions based on visual estimation of the image
inner_radius = 20.0
thickness = 15.0
outer_radius = inner_radius + thickness
height_inner = 20.0
height_outer = 12.0
angle = 90.0

# Create the 3D model
result = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, height_outer)
    # Create a concave top surface using a 3-point arc
    # The control point is chosen to create a 'dip' in the profile
    .threePointArc(
        (inner_radius + thickness * 0.4, height_outer + (height_inner - height_outer) * 0.25),
        (inner_radius, height_inner)
    )
    .close()
    .revolve(angle)
)