import cadquery as cq

# Parametric dimensions
outer_diameter = 100.0  # Diameter of the outer circle
inner_diameter = 40.0   # Diameter of the central hole
thickness = 2.0         # Thickness of the disk
slot_width = 5.0        # Width of the outer notch
slot_depth = 5.0        # Depth of the outer notch from the edge inwards

# Create the base disk
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
)

# Create the cutting tool for the slot
# The slot is located at the top (positive Y direction relative to center)
# We position a rectangle such that it cuts into the outer edge
slot_cutter = (
    cq.Workplane("XY")
    .rect(slot_width, slot_depth * 2)  # Make it deep enough to ensure a clean cut
    .extrude(thickness)
    .translate((0, outer_diameter / 2.0, 0)) # Move to the top edge
)

# Cut the slot from the disk
result = result.cut(slot_cutter)