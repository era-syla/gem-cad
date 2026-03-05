import cadquery as cq

# Parametric dimensions
base_diameter = 50.0
base_thickness = 4.0
shaft_diameter = 8.0
shaft_height = 60.0  # Height from the top of the base
tip_chamfer = 1.5    # Size of the conical tip

# Create the base
base = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_thickness)

# Create the shaft
# We start from the top face of the base
shaft = (
    base.faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2)
    .extrude(shaft_height)
)

# Create the conical tip
# We select the top edge of the shaft and apply a chamfer
# The chamfer distance should be less than the radius to leave a small flat top,
# or equal to radius for a pointy top. The image shows a small flat top.
# Let's target a small flat spot on top, so chamfer < radius.
radius = shaft_diameter / 2
actual_chamfer = min(tip_chamfer, radius - 0.5) # Ensure we don't chamfer the whole face away entirely

result = shaft.edges(">Z").chamfer(actual_chamfer)

# If you want to export or visualize:
# show_object(result)