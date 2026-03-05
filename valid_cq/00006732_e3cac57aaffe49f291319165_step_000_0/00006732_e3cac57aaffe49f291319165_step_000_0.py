import cadquery as cq

# Parametric dimensions based on the visual aspect ratio of the image
rod_length = 200.0
rod_diameter = 12.0

# Create the solid cylindrical rod
# We start on the YZ plane to orient the rod horizontally along the X-axis
# to match the approximate perspective of the image.
result = (
    cq.Workplane("YZ")
    .circle(rod_diameter / 2.0)
    .extrude(rod_length)
)