import cadquery as cq

# Parametric dimensions based on visual aspect ratio
cylinder_radius = 10.0
cylinder_height = 60.0

# Create the cylinder by sketching a circle on the XY plane and extruding it
result = (
    cq.Workplane("XY")
    .circle(cylinder_radius)
    .extrude(cylinder_height)
)