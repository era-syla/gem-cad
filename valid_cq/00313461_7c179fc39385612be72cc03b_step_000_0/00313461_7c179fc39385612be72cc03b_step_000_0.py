import cadquery as cq

# Parametric dimensions estimated from the image
panel_length = 120.0      # Length of the main body
panel_height = 40.0       # Vertical height
panel_thickness = 8.0     # Total thickness of the main body
tongue_length = 3.0       # Length of the protrusion on the left edge
tongue_thickness = 4.0    # Thickness of the tongue (narrower than main body)

# 1. Create the main rectangular body
# We position it so the left face is at X=0, centered on Y and Z
main_body = (
    cq.Workplane("XY")
    .box(panel_length, panel_thickness, panel_height)
    .translate((panel_length / 2, 0, 0))
)

# 2. Create the tongue feature on the left side
# This creates the stepped profile ("notches") on the left edge
# Positioned to extend in the negative X direction from X=0
tongue = (
    cq.Workplane("XY")
    .box(tongue_length, tongue_thickness, panel_height)
    .translate((-tongue_length / 2, 0, 0))
)

# 3. Combine parts into the final solid geometry
result = main_body.union(tongue)